from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

CONTROL_SERVER_URL = 'http://192.168.10.112:5001/control'  # Cambia <LOCAL_IP> a la IP de tu máquina local
VIDEO_FEED_URL = 'http://192.168.10.112:5001/video_feed'  # Cambia <LOCAL_IP> a la IP de tu máquina local

@app.route('/')
def index():
    return render_template('index.html', video_feed_url=VIDEO_FEED_URL)

@app.route('/control', methods=['POST'])
def control():
    try:
        # Lee los valores desde el formulario
        data = request.get_json()
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')
        r = data.get('r')

        # Envía los datos al servidor del Dobot
        response = requests.post(CONTROL_SERVER_URL, json={
            'x': x,
            'y': y,
            'z': z,
            'r': r
        })

        if response.status_code == 200:
            return jsonify({'message': 'Comando enviado correctamente'}), 200
        else:
            return jsonify({'message': response.json().get('message')}), 500
    except Exception as e:
        return jsonify({'message': f'Error en la aplicación web: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
