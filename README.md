# Lista de Tareas con Lista Simple Enlazada

Aplicación de lista de tareas desarrollada en Python utilizando exclusivamente una **lista simplemente enlazada** para gestionar las tareas (sin usar métodos de listas como `append`, `insert`, `pop` o `remove` sobre la estructura de datos principal).

## Características

- **Estructura de datos**: `Node` y `SinglyLinkedList` con manejo manual de punteros (`next`).
- **Operaciones**:
  - Agregar tarea al final de la lista.
  - Eliminar tarea por nombre (se elimina la primera coincidencia).
  - Recorrer la lista para mostrar todas las tareas en orden.
- **Interfaz gráfica (GUI)**:
  - Campo de texto para escribir una nueva tarea.
  - Botón **"Agregar Tarea"**.
  - Botón **"Eliminar Tarea"** (por nombre; en el modo Tkinter también se puede seleccionar desde la lista).
  - Área de lista/scroll para visualizar las tareas actuales.
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
- Botón **"Eliminar Tarea"**.
- Lista de tareas actualizada en tiempo real.

