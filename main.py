from __future__ import annotations

import sys
from typing import Optional, Tuple

try:
    import customtkinter as ctk

    USE_CUSTOM_TK: bool = True
except ImportError:  # pragma: no cover - fallback only used when customtkinter is missing
    import tkinter as tk
    from tkinter import messagebox

    USE_CUSTOM_TK = False


class Node:
    def __init__(self, task_name: str, status: str = "pendiente") -> None:
        self.task_name: str = task_name
        self.status: str = status
        self.next: Optional[Node] = None


class SinglyLinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def add_task(self, name: str) -> None:
        if self.head is None:
            self.head = Node(name)
            return

        current_node: Optional[Node] = self.head
        while current_node is not None and current_node.next is not None:
            current_node = current_node.next

        if current_node is not None:
            current_node.next = Node(name)

    def _find_task(self, name: str) -> Optional[Node]:
        current_node: Optional[Node] = self.head
        previous_node: Optional[Node] = None

        while current_node is not None:
            if current_node.task_name == name:
                return current_node

            previous_node = current_node
            current_node = current_node.next

        return None

    def mark_task_completed(self, name: str) -> bool:
        node: Optional[Node] = self._find_task(name)
        if node is None:
            return False
        node.status = "completada"
        return True

    def mark_task_pending(self, name: str) -> bool:
        node: Optional[Node] = self._find_task(name)
        if node is None:
            return False
        node.status = "pendiente"
        return True

    def get_all_tasks(self) -> Tuple[Tuple[str, str], ...]:
        tasks: Tuple[Tuple[str, str], ...] = ()
        current_node: Optional[Node] = self.head

        while current_node is not None:
            tasks = tasks + ((current_node.task_name, current_node.status),)
            current_node = current_node.next

        return tasks


if USE_CUSTOM_TK:

    class ToDoApp(ctk.CTk):
        def __init__(self) -> None:
            super().__init__()
            self.title("Lista de Tareas (Lista Simple)")

            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

            self.geometry("640x480")
            self.minsize(520, 380)

            self.task_list: SinglyLinkedList = SinglyLinkedList()
            self.selected_task_name: Optional[str] = None
            self._selected_label: Optional[ctk.CTkLabel] = None

            self._configure_grid()
            self._create_widgets()

        def _configure_grid(self) -> None:
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)

        def _create_widgets(self) -> None:
            input_frame: ctk.CTkFrame = ctk.CTkFrame(self)
            input_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

            input_frame.columnconfigure(0, weight=3)
            input_frame.columnconfigure(1, weight=1)
            input_frame.columnconfigure(2, weight=1)

            input_label: ctk.CTkLabel = ctk.CTkLabel(
                input_frame,
                text="Nueva tarea:",
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
            )
            input_label.grid(row=0, column=0, sticky="w", padx=(10, 10), pady=(10, 5))

            self.task_entry: ctk.CTkEntry = ctk.CTkEntry(
                input_frame,
                placeholder_text="Escribe una tarea...",
            )
            self.task_entry.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady=(0, 10))

            add_button: ctk.CTkButton = ctk.CTkButton(
                input_frame,
                text="Agregar Tarea",
                command=self._on_add_task,
            )
            add_button.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 10))

            complete_button: ctk.CTkButton = ctk.CTkButton(
                input_frame,
                text="Marcar Completada",
                fg_color="#b3261e",
                hover_color="#7f0000",
                command=self._on_delete_task,
            )
            complete_button.grid(row=1, column=2, sticky="ew", padx=(0, 10), pady=(0, 10))

            list_frame: ctk.CTkFrame = ctk.CTkFrame(self)
            list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

            list_frame.columnconfigure(0, weight=1)
            list_frame.rowconfigure(1, weight=1)

            list_label: ctk.CTkLabel = ctk.CTkLabel(
                list_frame,
                text="Tareas actuales:",
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
            )
            list_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

            self.task_scroll_frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(
                list_frame,
                label_text="",
            )
            self.task_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

            self.task_scroll_frame.columnconfigure(0, weight=1)

            status_legend: ctk.CTkLabel = ctk.CTkLabel(
                list_frame,
                text="Pendiente = ○   Completada = ✓",
                anchor="w",
                font=ctk.CTkFont(size=11),
            )
            status_legend.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))

        def _clear_task_scroll_frame(self) -> None:
            for child in self.task_scroll_frame.winfo_children():
                child.destroy()

        def _refresh_tasks_view(self) -> None:
            self._clear_task_scroll_frame()

            tasks: Tuple[Tuple[str, str], ...] = self.task_list.get_all_tasks()
            index: int = 0
            for task_name, status in tasks:
                prefix: str = "○" if status == "pendiente" else "✓"
                task_label: ctk.CTkLabel = ctk.CTkLabel(
                    self.task_scroll_frame,
                    text=f"{index + 1}. {prefix} {task_name}",
                    anchor="w",
                )
                task_label.grid(row=index, column=0, sticky="w", padx=10, pady=4)
                task_label.bind(
                    "<Button-1>",
                    lambda _event, tn=task_name, lbl=task_label: self._on_task_selected(
                        tn, lbl
                    ),
                )
                index += 1

        def _on_task_selected(self, task_name: str, label: ctk.CTkLabel) -> None:
            if self._selected_label is not None:
                self._selected_label.configure(text_color=None)

            self.selected_task_name = task_name
            self._selected_label = label
            label.configure(text_color="#00e676")

        def _on_add_task(self) -> None:
            task_name: str = self.task_entry.get().strip()
            if not task_name:
                self._show_info_message("Entrada vacía", "Por favor, escribe una tarea.")
                return

            self.task_list.add_task(task_name)
            self.task_entry.delete(0, "end")
            self._refresh_tasks_view()

        def _on_delete_task(self) -> None:
            if self.selected_task_name is None:
                self._show_info_message(
                    "Sin tarea seleccionada",
                    "Selecciona una tarea de la lista para marcarla como completada.",
                )
                return

            updated: bool = self.task_list.mark_task_completed(self.selected_task_name)
            if not updated:
                self._show_info_message(
                    "Tarea no encontrada",
                    "No se encontró una tarea con ese nombre.",
                )
                return

            self.selected_task_name = None
            self._selected_label = None
            self._refresh_tasks_view()

        def _show_info_message(self, title: str, message: str) -> None:
            info_window: ctk.CTkToplevel = ctk.CTkToplevel(self)
            info_window.title(title)
            info_window.geometry("320x140")
            info_window.resizable(False, False)

            info_window.grab_set()

            info_label: ctk.CTkLabel = ctk.CTkLabel(
                info_window,
                text=message,
                wraplength=280,
                anchor="center",
                justify="center",
            )
            info_label.pack(expand=True, fill="both", padx=20, pady=(20, 10))

            close_button: ctk.CTkButton = ctk.CTkButton(
                info_window,
                text="Cerrar",
                command=info_window.destroy,
            )
            close_button.pack(pady=(0, 15))


else:

    class ToDoApp(tk.Tk):
        def __init__(self) -> None:
            super().__init__()
            self.title("Lista de Tareas (Lista Simple)")

            self.geometry("640x480")
            self.minsize(520, 380)

            self.configure(bg="#121212")

            self.task_list: SinglyLinkedList = SinglyLinkedList()

            self._configure_grid()
            self._create_widgets()

        def _configure_grid(self) -> None:
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)

        def _create_widgets(self) -> None:
            input_frame: tk.Frame = tk.Frame(self, bg="#1f1f1f")
            input_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

            input_frame.columnconfigure(0, weight=3)
            input_frame.columnconfigure(1, weight=1)
            input_frame.columnconfigure(2, weight=1)

            input_label: tk.Label = tk.Label(
                input_frame,
                text="Nueva tarea:",
                anchor="w",
                fg="#ffffff",
                bg="#1f1f1f",
                font=("Segoe UI", 11, "bold"),
            )
            input_label.grid(row=0, column=0, sticky="w", padx=(10, 10), pady=(10, 5))

            self.task_entry: tk.Entry = tk.Entry(
                input_frame,
                bg="#2b2b2b",
                fg="#ffffff",
                insertbackground="#ffffff",
                relief="flat",
            )
            self.task_entry.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady=(0, 10))

            add_button: tk.Button = tk.Button(
                input_frame,
                text="Agregar Tarea",
                command=self._on_add_task,
                bg="#1e88e5",
                fg="#ffffff",
                activebackground="#1565c0",
                activeforeground="#ffffff",
                relief="flat",
                padx=8,
                pady=4,
            )
            add_button.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 10))

            delete_button: tk.Button = tk.Button(
                input_frame,
                text="Marcar Completada",
                command=self._on_delete_task,
                bg="#b3261e",
                fg="#ffffff",
                activebackground="#7f0000",
                activeforeground="#ffffff",
                relief="flat",
                padx=8,
                pady=4,
            )
            delete_button.grid(row=1, column=2, sticky="ew", padx=(0, 10), pady=(0, 10))

            list_frame: tk.Frame = tk.Frame(self, bg="#121212")
            list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

            list_frame.columnconfigure(0, weight=1)
            list_frame.rowconfigure(1, weight=1)

            list_label: tk.Label = tk.Label(
                list_frame,
                text="Tareas actuales:",
                anchor="w",
                fg="#ffffff",
                bg="#121212",
                font=("Segoe UI", 11, "bold"),
            )
            list_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

            self.task_listbox: tk.Listbox = tk.Listbox(
                list_frame,
                bg="#1f1f1f",
                fg="#ffffff",
                selectbackground="#3949ab",
                selectforeground="#ffffff",
                activestyle="none",
                borderwidth=0,
                highlightthickness=0,
            )
            self.task_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

            scrollbar: tk.Scrollbar = tk.Scrollbar(
                list_frame,
                orient="vertical",
                command=self.task_listbox.yview,
            )
            scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 10))
            self.task_listbox.configure(yscrollcommand=scrollbar.set)

        def _refresh_tasks_view(self) -> None:
            self.task_listbox.delete(0, tk.END)

            tasks: Tuple[Tuple[str, str], ...] = self.task_list.get_all_tasks()

            index: int = 0
            for task_name, status in tasks:
                prefix: str = "○" if status == "pendiente" else "✓"
                self.task_listbox.insert(tk.END, f"{index + 1}. {prefix} {task_name}")
                index += 1

        def _on_add_task(self) -> None:
            task_name: str = self.task_entry.get().strip()
            if not task_name:
                self._show_info_message("Entrada vacía", "Por favor, escribe una tarea.")
                return

            self.task_list.add_task(task_name)
            self.task_entry.delete(0, tk.END)
            self._refresh_tasks_view()

        def _on_delete_task(self) -> None:
            task_name: str = ""

            if self.task_listbox.curselection():
                selected_index: int = int(self.task_listbox.curselection()[0])

                current_index: int = 0
                current_node = self.task_list.head
                while current_node is not None:
                    if current_index == selected_index:
                        task_name = current_node.task_name
                        break
                    current_index += 1
                    current_node = current_node.next

            if not task_name:
                self._show_info_message(
                    "Sin tarea seleccionada",
                    "Selecciona una tarea de la lista para marcarla como completada.",
                )
                return

            updated: bool = self.task_list.mark_task_completed(task_name)
            if not updated:
                self._show_info_message(
                    "Tarea no encontrada",
                    "No se encontró una tarea con ese nombre.",
                )
                return

            self.task_entry.delete(0, tk.END)
            self.task_listbox.selection_clear(0, tk.END)
            self._refresh_tasks_view()

        def _show_info_message(self, title: str, message: str) -> None:
            messagebox.showinfo(title, message)


def main() -> None:
    app: ToDoApp = ToDoApp()
    app.mainloop()


if __name__ == "__main__":
    sys.exit(main())

