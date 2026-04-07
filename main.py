import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# BACKEND: ESTRUCTURA DE DATOS (LISTA DOBLE)
# ==========================================

class ForensicDossier:
    """Cada uno de estos es un registro forense (lo que sería nuestro nodo)"""
    def __init__(self, case_id, deceased_name, cause_of_death):
        self.case_id = case_id
        self.deceased_name = deceased_name
        self.cause_of_death = cause_of_death
        
        # Los punteros clave para que la lista sea doble
        self.next_dossier = None
        self.prev_dossier = None

class MorgueArchiveRegistry:
    """El gestor principal de nuestra lista doblemente enlazada"""
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    # 1. Meter el registro al final de la cola (el 'append' de las diapositivas)
    def admit_standard_case(self, case_id, deceased_name, cause_of_death):
        new_dossier = ForensicDossier(case_id, deceased_name, cause_of_death)
        if self.head is None:
            self.head = new_dossier
            self.tail = new_dossier
        else:
            new_dossier.prev_dossier = self.tail
            self.tail.next_dossier = new_dossier
            self.tail = new_dossier
        self.length += 1

    # 2. Casos urgentes que van de primeros (el 'prepend' de las diapositivas)
    def admit_urgent_case(self, case_id, deceased_name, cause_of_death):
        new_dossier = ForensicDossier(case_id, deceased_name, cause_of_death)
        if self.head is None:
            self.head = new_dossier
            self.tail = new_dossier
        else:
            new_dossier.next_dossier = self.head
            self.head.prev_dossier = new_dossier
            self.head = new_dossier
        self.length += 1

    # 3. Recorrer los nodos hasta llegar al cajón que necesitamos ('traverse_to_index')
    def traverse_to_drawer(self, index):
        current_dossier = self.head
        i = 0
        while i != index:
            current_dossier = current_dossier.next_dossier
            i += 1
        return current_dossier

    # 4. Meter un expediente en una posición exacta ('insert')
    def file_case_at_drawer(self, index, case_id, deceased_name, cause_of_death):
        if index == 0:
            self.admit_urgent_case(case_id, deceased_name, cause_of_death)
        elif index >= self.length:
            self.admit_standard_case(case_id, deceased_name, cause_of_death)
        else:
            new_dossier = ForensicDossier(case_id, deceased_name, cause_of_death)
            leader = self.traverse_to_drawer(index - 1)
            follower = leader.next_dossier
            
            # Acomodando los punteros para no romper la lista
            leader.next_dossier = new_dossier
            new_dossier.prev_dossier = leader
            new_dossier.next_dossier = follower
            follower.prev_dossier = new_dossier
            self.length += 1

    # 5. Sacar un expediente de su cajón para archivarlo ('remove')
    def dispatch_case_from_drawer(self, index):
        # Validamos que no nos pidan algo fuera de los límites
        if index < 0 or index >= self.length:
            return False

        if index == 0:
            self.head = self.head.next_dossier
            if self.head:
                self.head.prev_dossier = None
            else:
                self.tail = None
        elif index == self.length - 1:
            self.tail = self.tail.prev_dossier
            if self.tail:
                self.tail.next_dossier = None
            else:
                self.head = None
        else:
            leader = self.traverse_to_drawer(index - 1)
            dossier_to_remove = leader.next_dossier
            follower = dossier_to_remove.next_dossier
            
            # Empalmamos el anterior con el siguiente, dejando al del medio por fuera
            leader.next_dossier = follower
            follower.prev_dossier = leader
            
        self.length -= 1
        return True

    # UN PLUS: Buscar un caso iterando por los nodos
    def search_dossier_by_id(self, target_id):
        current_dossier = self.head
        drawer_index = 0
        while current_dossier is not None:
            if current_dossier.case_id == target_id:
                return current_dossier, drawer_index
            current_dossier = current_dossier.next_dossier
            drawer_index += 1
        return None, -1


# ==========================================
# FRONTEND: INTERFAZ GRÁFICA CON TKINTER
# ==========================================

class ModernForensicApp:
    def __init__(self, root):
        self.registry = MorgueArchiveRegistry()
        self.root = root
        self.root.title("SGAF Pro - Sistema Avanzado de Autopsias")
        self.root.geometry("950x700")
        self.root.configure(bg="#0f111a") # Fondo oscuro premium

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        """Configuración de estilos modernos para que no se vea como app de los 90s"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Paleta de colores
        bg_color = "#1a1f2e"
        fg_color = "#e2e8f0"
        accent_color = "#3b82f6"
        
        style.configure("TFrame", background="#0f111a")
        style.configure("Card.TFrame", background=bg_color, relief="flat")
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#0f111a", foreground="#38bdf8", font=("Segoe UI", 18, "bold"))
        
        style.configure("TButton", background=accent_color, foreground="white", font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        style.map("TButton", background=[("active", "#2563eb")])
        
        # Estilos para la tabla (Treeview)
        style.configure("Treeview", background=bg_color, fieldbackground=bg_color, foreground=fg_color, rowheight=30, borderwidth=0, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#0f111a", foreground="#38bdf8", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Treeview", background=[("selected", "#1e3a8a")])

    def build_ui(self):
        # --- ENCABEZADO ---
        ttk.Label(self.root, text="SISTEMA CENTRAL DE MORGUE (LISTAS DOBLES)", style="Title.TLabel").pack(pady=20)

        # --- PANEL DE ENTRADA DE DATOS ---
        card_frame = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        card_frame.pack(fill="x", padx=40, pady=10)

        # Fila 1
        ttk.Label(card_frame, text="ID Expediente:").grid(row=0, column=0, sticky="e", padx=5, pady=10)
        self.entry_id = ttk.Entry(card_frame, width=15, font=("Segoe UI", 10))
        self.entry_id.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(card_frame, text="Fallecido:").grid(row=0, column=2, sticky="e", padx=5)
        self.entry_name = ttk.Entry(card_frame, width=25, font=("Segoe UI", 10))
        self.entry_name.grid(row=0, column=3, sticky="w", padx=5)

        ttk.Label(card_frame, text="Causa deceso:").grid(row=0, column=4, sticky="e", padx=5)
        self.entry_cause = ttk.Entry(card_frame, width=20, font=("Segoe UI", 10))
        self.entry_cause.grid(row=0, column=5, sticky="w", padx=5)

        # Fila 2
        ttk.Label(card_frame, text="Gaveta (Índice):").grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.entry_index = ttk.Entry(card_frame, width=15, font=("Segoe UI", 10))
        self.entry_index.grid(row=1, column=1, sticky="w", padx=5)

        # --- PANEL DE BOTONES ---
        btn_frame = ttk.Frame(self.root, style="TFrame")
        btn_frame.pack(fill="x", padx=40, pady=10)

        # Acciones de inserción
        ttk.Button(btn_frame, text="✚ Ingreso Normal (Append)", command=self.action_append).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="⚠ Ingreso Urgente (Prepend)", command=self.action_prepend).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="➥ Insertar en Gaveta (Insert)", command=self.action_insert).pack(side="left", padx=5)
        
        # Acciones de eliminación y búsqueda
        ttk.Button(btn_frame, text="🗑 Archivar Gaveta (Remove)", command=self.action_remove).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="🔍 Buscar ID", command=self.action_search).pack(side="right", padx=5)

        # --- TABLA DE DATOS ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=40, pady=15)

        columns = ("indice", "id", "fallecido", "causa", "p_previo", "p_siguiente")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("indice", text="Gaveta [idx]")
        self.tree.heading("id", text="ID Expediente")
        self.tree.heading("fallecido", text="Nombre del Fallecido")
        self.tree.heading("causa", text="Causa de Muerte")
        self.tree.heading("p_previo", text="⬅ Puntero Anterior")
        self.tree.heading("p_siguiente", text="Puntero Siguiente ➡")

        self.tree.column("indice", width=80, anchor="center")
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("fallecido", width=200)
        self.tree.column("causa", width=150)
        self.tree.column("p_previo", width=150, anchor="center")
        self.tree.column("p_siguiente", width=150, anchor="center")

        # El scroll para cuando tengamos muchos registros
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- BARRA DE ESTADO INFERIOR ---
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema Listo. Gavetas ocupadas: 0")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bg="#0f111a", fg="#94a3b8", font=("Segoe UI", 9, "italic"), anchor="w")
        status_bar.pack(fill="x", side="bottom", padx=40, pady=10)

    # --- FUNCIONES DE LA INTERFAZ ---

    def _get_core_inputs(self):
        """Limpiamos los espacios en blanco de lo que escriba el usuario"""
        return self.entry_id.get().strip(), self.entry_name.get().strip(), self.entry_cause.get().strip()

    def _clear_inputs(self):
        """Vacía las cajas de texto tras cada operación"""
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_cause.delete(0, tk.END)
        self.entry_index.delete(0, tk.END)

    def refresh_table(self):
        """Refresca la tabla y nos muestra claramente hacia dónde apuntan los nodos"""
        # Limpiamos todo primero
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        current = self.registry.head
        idx = 0
        while current is not None:
            # Aquí es donde se nota la lista doble: vemos quién está antes y quién después
            prev_ptr = f"ID: {current.prev_dossier.case_id}" if current.prev_dossier else "[NULL]"
            next_ptr = f"ID: {current.next_dossier.case_id}" if current.next_dossier else "[NULL]"
            
            self.tree.insert("", "end", values=(
                f"[{idx}]", 
                current.case_id, 
                current.deceased_name, 
                current.cause_of_death,
                prev_ptr,
                next_ptr
            ))
            current = current.next_dossier
            idx += 1
            
        self.status_var.set(f"Gavetas ocupadas actualmente: {self.registry.length}")

    def action_append(self):
        c_id, name, cause = self._get_core_inputs()
        if not all([c_id, name, cause]):
            messagebox.showwarning("Faltan datos", "No te olvides de llenar ID, Nombre y Causa.")
            return
        self.registry.admit_standard_case(c_id, name, cause)
        self._clear_inputs()
        self.refresh_table()

    def action_prepend(self):
        c_id, name, cause = self._get_core_inputs()
        if not all([c_id, name, cause]):
            messagebox.showwarning("Faltan datos", "No te olvides de llenar ID, Nombre y Causa.")
            return
        self.registry.admit_urgent_case(c_id, name, cause)
        self._clear_inputs()
        self.refresh_table()

    def action_insert(self):
        c_id, name, cause = self._get_core_inputs()
        try:
            idx = int(self.entry_index.get())
        except ValueError:
            messagebox.showerror("Ojo ahí", "Necesitas meter un número entero en 'Gaveta (Índice)'.")
            return
            
        if not all([c_id, name, cause]):
            messagebox.showwarning("Faltan datos", "No te olvides de llenar ID, Nombre y Causa.")
            return
            
        self.registry.file_case_at_drawer(idx, c_id, name, cause)
        self._clear_inputs()
        self.refresh_table()

    def action_remove(self):
        try:
            idx = int(self.entry_index.get())
        except ValueError:
            messagebox.showerror("Ojo ahí", "Dime qué número de gaveta quieres archivar.")
            return
            
        if self.registry.dispatch_case_from_drawer(idx):
            self._clear_inputs()
            self.refresh_table()
            messagebox.showinfo("Listo", f"Expediente de la gaveta {idx} guardado en el archivo muerto.")
        else:
            messagebox.showwarning("Mmm...", "Esa gaveta no existe o está vacía.")

    def action_search(self):
        target_id = self.entry_id.get().strip()
        if not target_id:
            messagebox.showwarning("Falta el ID", "Escribe el ID del expediente que buscas.")
            return
            
        dossier, idx = self.registry.search_dossier_by_id(target_id)
        if dossier:
            messagebox.showinfo(
                "¡Lo encontramos!", 
                f"Gaveta: [{idx}]\nID: {dossier.case_id}\nFallecido: {dossier.deceased_name}\nCausa: {dossier.cause_of_death}"
            )
        else:
            messagebox.showerror("Nada de nada", f"No hay expedientes activos con el ID {target_id}.")

# ==========================================
# ARRANQUE DE LA APP
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernForensicApp(root)
    root.mainloop()