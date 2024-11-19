import tkinter as tk
from tkinter import ttk
from serial.tools import list_ports
import pydobot

# Configuración del puerto
port = 'COM16'  # Cambia esto si es necesario
device = pydobot.Dobot(port=port, verbose=True)

# Límites para los ejes en coordenadas cartesianas
X_MIN, X_MAX = 170, 240
Y_MIN, Y_MAX = -150, 150
Z_MIN, Z_MAX = 0, 100
R_MIN, R_MAX = -180, 180  # Rotación del efector

# Variables para la posición inicial
initial_x, initial_y, initial_z, initial_r = 200, 0, 20, 0

# Función para actualizar la posición en el espacio de trabajo
def update_position(event=None):
    new_x = int(x_slider.get())
    new_y = int(y_slider.get())
    new_z = int(z_slider.get())
    new_r = int(r_slider.get())
    
    # Actualiza las etiquetas para mostrar los valores actuales
    x_value_label.config(text=f"X: {new_x}")
    y_value_label.config(text=f"Y: {new_y}")
    z_value_label.config(text=f"Z: {new_z}")
    r_value_label.config(text=f"R: {new_r}")
    
    print(f"Moviendo a X: {new_x}, Y: {new_y}, Z: {new_z}, R: {new_r}")
    
    try:
        # Envía el comando para mover a la posición en coordenadas cartesianas
        device._set_ptp_cmd(mode=0, x=new_x, y=new_y, z=new_z, r=new_r)
    except Exception as e:
        print(f"Error al intentar mover el Dobot: {e}")

# Crea la ventana principal
root = tk.Tk()
root.title("Control de Dobot Magician en el Espacio de Trabajo")

# Sliders para controlar X, Y, Z y R
# Slider X
tk.Label(root, text="Control de X (mm)").pack()
x_slider = ttk.Scale(root, from_=X_MIN, to=X_MAX, orient="horizontal")
x_slider.set(initial_x)
x_slider.pack(padx=10, pady=5)
x_slider.bind("<ButtonRelease-1>", update_position)
x_value_label = tk.Label(root, text=f"X: {initial_x}")
x_value_label.pack()

# Slider Y
tk.Label(root, text="Control de Y (mm)").pack()
y_slider = ttk.Scale(root, from_=Y_MIN, to=Y_MAX, orient="horizontal")
y_slider.set(initial_y)
y_slider.pack(padx=10, pady=5)
y_slider.bind("<ButtonRelease-1>", update_position)
y_value_label = tk.Label(root, text=f"Y: {initial_y}")
y_value_label.pack()

# Slider Z
tk.Label(root, text="Control de Z (mm)").pack()
z_slider = ttk.Scale(root, from_=Z_MIN, to=Z_MAX, orient="horizontal")
z_slider.set(initial_z)
z_slider.pack(padx=10, pady=5)
z_slider.bind("<ButtonRelease-1>", update_position)
z_value_label = tk.Label(root, text=f"Z: {initial_z}")
z_value_label.pack()

# Slider R (rotación)
tk.Label(root, text="Control de Rotación (°)").pack()
r_slider = ttk.Scale(root, from_=R_MIN, to=R_MAX, orient="horizontal")
r_slider.set(initial_r)
r_slider.pack(padx=10, pady=5)
r_slider.bind("<ButtonRelease-1>", update_position)
r_value_label = tk.Label(root, text=f"R: {initial_r}")
r_value_label.pack()

# Botón para cerrar la conexión
def close_connection():
    device.close()
    root.quit()

close_button = ttk.Button(root, text="Cerrar conexión", command=close_connection)
close_button.pack(pady=10)

# Ejecuta la interfaz
root.mainloop()