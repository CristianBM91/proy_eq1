from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import rclpy
from std_msgs.msg import String
import os
import psutil
import time

app = Flask(__name__)
CORS(app)

# Inicializar los nodos
rclpy.init()

# Conectar con el servidor
@app.route('/conectar', methods=['GET'])
def conectar():
    # Ejecuta GAZEBO
    try:
        # El comando a ejecutar en una nueva terminal
        command = 'ros2 launch proy_eq1_mundo turtlebot3_my_world.launch.py'

        # Ejecutar el comando en una nueva ventana de terminal utilizando gnome-terminal
        subprocess.Popen(['gnome-terminal','--geometry=80x24+0+0', '--window', '--', 'bash', '-c', command])

    except Exception as e:
        print('Error al ejecutar el comando:', str(e))

    # Ejecuta el nodo de ROS2 movement_server
    try:
        # El comando a ejecutar en una nueva terminal
        command = 'ros2 launch proy_eq1_nav_manual movement_server_launch.launch.py'
    
        # Ejecutar el comando en una nueva ventana de terminal utilizando gnome-terminal
        subprocess.Popen(['gnome-terminal','--geometry=80x24+0+0', '--window', '--', 'bash', '-c', command])

    except Exception as e:
        print('Error al ejecutar el comando:', str(e))

    try:
       # Ejecutar proy_eq1_nav2_system
        command = 'ros2 launch proy_eq1_nav2_system proy_eq1_tb3_sim_nav2.launch.py'
        # Ejecutar el comando en una nueva ventana de terminal utilizando gnome-terminal
        subprocess.Popen(['gnome-terminal','--geometry=80x24+0+0', '--window', '--', 'bash', '-c', command])
    except Exception as e:
        print('Error al ejecutar el comando:', str(e))

    try:
        # Lanzamos el fichero que publica la posición inicial
        command = 'ros2 run proy_eq1_nav2_system initial_pose_pub'
        # Ejecutar el comando en una nueva ventana de terminal utilizando gnome-terminal
        subprocess.Popen(['gnome-terminal','--geometry=80x24+0+0', '--window', '--', 'bash', '-c', command])
    except Exception as e:
        print('Error al ejecutar el comando:', str(e))


        

    dato = "Conexion con el servidor exitosa"
    mensaje = String()
    mensaje.data = dato
    
    return jsonify({'dato': dato})

# Desconectar del servidor
@app.route('/desconectar', methods=['GET'])
def desconectar():
    # cierra GAZEBO
    try:
        # Obtener los PID de los procesos de gnome-terminal
        pids = obtener_pids_terminales()

        # Cerrar las terminales utilizando los PID
        for pid in pids:
            subprocess.run(['kill', str(pid)])
            time.sleep(0.1)  # Esperar un breve período entre cierres
    except Exception as e:
        print('Error al cerrar las terminales:', str(e))

    except Exception as e:
        print('Error al cerrar las terminales:', str(e))

    dato = "Conexion con el servidor exitosa"
    mensaje = String()
    mensaje.data = dato
    
    return jsonify({'dato': dato})

def obtener_pids_terminales():
    pids = []
    for process in psutil.process_iter():
        try:
            if process.name() == "gnome-terminal-server":
                pids.append(process.pid)
        except psutil.NoSuchProcess:
            pass
    return pids


@app.route('/mover_manual', methods=['POST'])
def mover_manual():
    try:
        # Obtener el JSON enviado desde la página web
        data = request.json
        direccionDeMovimiento = data.get('direccionDeMovimiento')  
        
        print("direccion: " + direccionDeMovimiento)
        
        
        # Ejecuta el nodo de ROS2 movement_client
        subprocess.run(['ros2', 'run', 'proy_eq1_nav_manual', 'movement_client', direccionDeMovimiento])        
        return jsonify({'dato': 'Robot movido hacia ' + direccionDeMovimiento})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)


