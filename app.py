from flask import Flask, render_template, request, jsonify, Response
import serial
import wlkatapython  # Importa tu módulo WLKATA personalizado
import cv2
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración del puerto y conexión inicial al WLKATA
port = 'COM16'  # Cambia esto si es necesario
robot = None
wlkata_connected = False

# Posición inicial (Home)
HOME_POSITION = {'x': 160, 'y': 0, 'z': 100, 'r': 0}  # Home para WLKATA

try:
    serial_port = serial.Serial(port, baudrate=115200, timeout=1)
    robot = wlkatapython.Wlkata_UART()
    robot.init(serial_port, adr=-1)  # adr=-1 para comunicación directa
    print("WLKATA conectado correctamente")
    wlkata_connected = True
except Exception as e:
    print(f"Error al conectar con el WLKATA: {e}")

# Inicializar la cámara
camera_index = 1
camera = cv2.VideoCapture(camera_index)

if camera.isOpened():
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    camera.set(cv2.CAP_PROP_FPS, 5)
    time.sleep(2)
else:
    print(f"Error: No se pudo abrir la cámara {camera_index}")

@app.route('/')
def index():
    return render_template('index.html', video_feed_url='/video_feed', wlkata_connected=wlkata_connected)

@app.route('/control', methods=['POST'])
def control():
    global robot
    if not wlkata_connected:
        return jsonify({'status': 'error', 'message': 'WLKATA no conectado'}), 500

    try:
        data = request.get_json()
        x = float(data.get('x'))
        y = float(data.get('y'))
        z = float(data.get('z'))
        r = float(data.get('r'))

        robot.writecoordinate(motion=0, position=0, x=x, y=y, z=z, a=r, b=0, c=0)
        return jsonify({'status': 'success', 'message': f'Movido a X: {x}, Y: {y}, Z: {z}, R: {r}'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al mover el WLKATA: {e}'}), 500

@app.route('/home', methods=['POST'])
def home():
    global robot
    if not wlkata_connected:
        return jsonify({'status': 'error', 'message': 'WLKATA no conectado'}), 500

    try:
        x, y, z, r = HOME_POSITION.values()
        robot.writecoordinate(motion=0, position=0, x=x, y=y, z=z, a=r, b=0, c=0)
        return jsonify({'status': 'success', 'message': 'Movido a posición Home'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al mover a Home: {e}'}), 500

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            print("No se pudo leer el frame de la cámara")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8065)
