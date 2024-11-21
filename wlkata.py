import tkinter as tk
from tkinter import ttk
from wlkatapython import Wlkata_UART
import serial

# Configuración del puerto serie
PORT = 'COM14'  # Cambia esto según tu configuración
BAUD_RATE = 115200

try:
    # Conexión al puerto serie usando Wlkata_UART
    device = serial.Serial(PORT, BAUD_RATE, timeout=1)
    robot = Wlkata_UART()
    robot.init(device, -1)  # Inicializar el robot con la dirección -1
except Exception as e:
    print(f"Error al conectar con el puerto {PORT}: {e}")
    exit()

# Ángulos iniciales para Home
HOME_J1, HOME_J2, HOME_J3, HOME_J4, HOME_J5, HOME_J6 = 0, 0, 0, 0, 0, 0

# Límites de las juntas
J1_MIN, J1_MAX = -180, 180
J2_MIN, J2_MAX = -90, 90
J3_MIN, J3_MAX = -90, 90
J4_MIN, J4_MAX = -180, 180
J5_MIN, J5_MAX = -90, 90
J6_MIN, J6_MAX = -180, 180

# Función para mover a Home
def move_home():
    try:
        robot.homing()  # Usamos la función homing del archivo wlkatapython.py
        j1_slider.set(HOME_J1)
        j2_slider.set(HOME_J2)
        j3_slider.set(HOME_J3)
        j4_slider.set(HOME_J4)
        j5_slider.set(HOME_J5)
        j6_slider.set(HOME_J6)
        update_labels()
    except Exception as e:
        print(f"Error al mover a Home: {e}")

# Función para mover un joint específico
def update_joint(joint, value):
    try:
        # Obtener los ángulos actuales
        status = robot.getStatus()
        angles = {
            "J1": float(status["angle_A"]),
            "J2": float(status["angle_B"]),
            "J3": float(status["angle_C"]),
            "J4": float(status["angle_D"]),
            "J5": float(status["angle_X"]),
            "J6": float(status["angle_Y"]),
        }
        # Actualizar el ángulo correspondiente
        angles[joint] = value
        robot.writeangle(0, angles["J1"], angles["J2"], angles["J3"], angles["J4"], angles["J5"], angles["J6"])
    except Exception as e:
        print(f"Error al mover {joint}: {e}")

def update_j1(event=None):
    new_j1 = int(j1_slider.get())
    update_joint("J1", new_j1)
    j1_value_label.config(text=f"J1: {new_j1}")

def update_j2(event=None):
    new_j2 = int(j2_slider.get())
    update_joint("J2", new_j2)
    j2_value_label.config(text=f"J2: {new_j2}")

def update_j3(event=None):
    new_j3 = int(j3_slider.get())
    update_joint("J3", new_j3)
    j3_value_label.config(text=f"J3: {new_j3}")

def update_j4(event=None):
    new_j4 = int(j4_slider.get())
    update_joint("J4", new_j4)
    j4_value_label.config(text=f"J4: {new_j4}")

def update_j5(event=None):
    new_j5 = int(j5_slider.get())
    update_joint("J5", new_j5)
    j5_value_label.config(text=f"J5: {new_j5}")

def update_j6(event=None):
    new_j6 = int(j6_slider.get())
    update_joint("J6", new_j6)
    j6_value_label.config(text=f"J6: {new_j6}")

# Actualiza las etiquetas de los valores actuales
def update_labels():
    try:
        status = robot.getStatus()
        j1_value_label.config(text=f"J1: {status['angle_A']}")
        j2_value_label.config(text=f"J2: {status['angle_B']}")
        j3_value_label.config(text=f"J3: {status['angle_C']}")
        j4_value_label.config(text=f"J4: {status['angle_D']}")
        j5_value_label.config(text=f"J5: {status['angle_X']}")
        j6_value_label.config(text=f"J6: {status['angle_Y']}")
    except Exception as e:
        print(f"Error al actualizar etiquetas: {e}")

# Crea la ventana principal
root = tk.Tk()
root.title("Control de WLKATA Mirobot - Joints")

# Sliders para cada joint
tk.Label(root, text="Control de J1 (°)").pack()
j1_slider = ttk.Scale(root, from_=J1_MIN, to_=J1_MAX, orient="horizontal")
j1_slider.set(HOME_J1)
j1_slider.pack(padx=10, pady=5)
j1_slider.bind("<ButtonRelease-1>", update_j1)
j1_value_label = tk.Label(root, text=f"J1: {HOME_J1}")
j1_value_label.pack()

tk.Label(root, text="Control de J2 (°)").pack()
j2_slider = ttk.Scale(root, from_=J2_MIN, to_=J2_MAX, orient="horizontal")
j2_slider.set(HOME_J2)
j2_slider.pack(padx=10, pady=5)
j2_slider.bind("<ButtonRelease-1>", update_j2)
j2_value_label = tk.Label(root, text=f"J2: {HOME_J2}")
j2_value_label.pack()

tk.Label(root, text="Control de J3 (°)").pack()
j3_slider = ttk.Scale(root, from_=J3_MIN, to_=J3_MAX, orient="horizontal")
j3_slider.set(HOME_J3)
j3_slider.pack(padx=10, pady=5)
j3_slider.bind("<ButtonRelease-1>", update_j3)
j3_value_label = tk.Label(root, text=f"J3: {HOME_J3}")
j3_value_label.pack()

tk.Label(root, text="Control de J4 (°)").pack()
j4_slider = ttk.Scale(root, from_=J4_MIN, to_=J4_MAX, orient="horizontal")
j4_slider.set(HOME_J4)
j4_slider.pack(padx=10, pady=5)
j4_slider.bind("<ButtonRelease-1>", update_j4)
j4_value_label = tk.Label(root, text=f"J4: {HOME_J4}")
j4_value_label.pack()

tk.Label(root, text="Control de J5 (°)").pack()
j5_slider = ttk.Scale(root, from_=J5_MIN, to_=J5_MAX, orient="horizontal")
j5_slider.set(HOME_J5)
j5_slider.pack(padx=10, pady=5)
j5_slider.bind("<ButtonRelease-1>", update_j5)
j5_value_label = tk.Label(root, text=f"J5: {HOME_J5}")
j5_value_label.pack()

tk.Label(root, text="Control de J6 (°)").pack()
j6_slider = ttk.Scale(root, from_=J6_MIN, to_=J6_MAX, orient="horizontal")
j6_slider.set(HOME_J6)
j6_slider.pack(padx=10, pady=5)
j6_slider.bind("<ButtonRelease-1>", update_j6)
j6_value_label = tk.Label(root, text=f"J6: {HOME_J6}")
j6_value_label.pack()

# Botón para mover a Home
home_button = ttk.Button(root, text="Mover a Home", command=move_home)
home_button.pack(pady=10)

# Botón para cerrar la conexión
def close_connection():
    try:
        robot.cancellation()  # Cancelar cualquier movimiento actual
        device.close()
        print("Conexión cerrada.")
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")
    root.quit()

close_button = ttk.Button(root, text="Cerrar conexión", command=close_connection)
close_button.pack(pady=10)

# Ejecuta la interfaz
root.mainloop()
