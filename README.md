# Lista de Tareas con Lista Simple Enlazada

Aplicación de lista de tareas desarrollada en Python utilizando exclusivamente una **lista simplemente enlazada** para gestionar las tareas (sin usar métodos de listas como `append`, `insert`, `pop` o `remove` sobre la estructura de datos principal).

## Características

- **Estructura de datos**: `Node` y `SinglyLinkedList` con manejo manual de punteros (`next`).
- **Operaciones sobre la lista simplemente enlazada**:
  - Agregar tarea al final de la lista.
  - Marcar tarea como **pendiente** o **completada** (no se eliminan nodos, solo se actualiza su estado).
  - Recorrer la lista para obtener todas las tareas y su estado actual.
- **Interfaz gráfica (GUI)**:
  - Campo de texto para escribir una nueva tarea.
  - Botón **"Agregar Tarea"** para añadir una nueva tarea con estado **pendiente**.
  - Botón **"Marcar Completada"**:
    - En el modo `customtkinter`: se selecciona la tarea haciendo clic sobre ella en la lista y luego se pulsa el botón.
    - En el modo `tkinter`: se selecciona la tarea en el `Listbox` y luego se pulsa el botón.
  - Área de lista/scroll para visualizar las tareas actuales en orden, mostrando:
    - `○` antes del nombre cuando la tarea está **pendiente**.
    - `✓` antes del nombre cuando la tarea está **completada**.
- **Tecnología**: Python puro con `customtkinter` (o `tkinter` si `customtkinter` no está disponible).

## Requisitos

```bash
pip install -r requirements.txt
```

Si `customtkinter` no está instalado o no se puede importar, la aplicación utilizará automáticamente una versión basada en `tkinter` estándar.

## Ejecución

```bash
python main.py
```

La ventana de la aplicación se abrirá mostrando:

- Entrada de texto para la nueva tarea.
- Botón **"Agregar Tarea"**.
- Botón **"Marcar Completada"**.
- Lista de tareas actualizada en tiempo real, con indicadores de estado (`○` / `✓`) y selección de tareas con el ratón.

