from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# CLASES DEL SISTEMA

# CONDUCTOR
class Conductor:
    def __init__(self, id_conductor, nombre_conductor, cantidad_excesos):
        self.id_conductor = id_conductor
        self.nombre_conductor = nombre_conductor
        self.cantidad_excesos = cantidad_excesos

# REINSTRUCTOR
class Reinstructor:
    def __init__(self, id_reinstructor, nombre_reinstructor, nivel_reinstructor, correo_reinstructor):
        self.id_reinstructor = id_reinstructor
        self.nombre_reinstructor = nombre_reinstructor
        self.nivel_reinstructor = nivel_reinstructor
        self.correo_reinstructor = correo_reinstructor

# REINSTRUCCION
class Reinstruccion:
    def __init__(self, id_reinstruccion, reinstructor, conductor, fecha_asignacion=None, realizado_bool=False):
        self.id_reinstruccion = id_reinstruccion
        self.reinstructor = reinstructor
        self.conductor = conductor
        self.fecha_asignacion = fecha_asignacion or datetime.now().strftime("%d/%m/%Y")
        self.realizado_bool = realizado_bool

    def generar_nombre(self):
        fecha_sin_barras = self.fecha_asignacion.replace("/", "")
        return f"{self.conductor.nombre_conductor}_{fecha_sin_barras}_{self.reinstructor.nombre_reinstructor}"

    def verificar_realizado(self):
        self.realizado_bool = False  # Simulación para este ejemplo

    def imprimir(self):
        print(f"Conductor: {self.conductor.nombre_conductor}")
        print(f"Cantidad de excesos: {self.conductor.cantidad_excesos}")
        print(f"Fecha: {self.fecha_asignacion}")
        print(f"A cargo de: {self.reinstructor.nombre_reinstructor}")
        print(f"Estado: {'Realizado' if self.realizado_bool else 'No realizado'}")

    def enviar_correo(self, smtp_server, smtp_port, remitente, password):
        asunto = "Reinstrucción Automática"
        cuerpo = f"""
        Estimado {self.reinstructor.nombre_reinstructor},

        Se ha detectado un total de {self.conductor.cantidad_excesos} excesos del conductor {self.conductor.nombre_conductor}
        asignado el día {self.fecha_asignacion}.

        Saludos cordiales,
        Departamento de Prevención de Riesgos
        """

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = self.reinstructor.correo_reinstructor
        msg['Subject'] = asunto

        msg.attach(MIMEText(cuerpo, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(remitente, password)
                server.send_message(msg)
            print("Correo enviado con éxito.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

# PRUEBAS UNITARIAS

import unittest

class TestReinstruccion(unittest.TestCase):
    def setUp(self):
        self.conductor = Conductor(1, "Jaime Lique Tinte", 5)
        self.reinstructor = Reinstructor(1, "Luis Trujillo", "Tipo 1", "luis.trujillo@example.com")
        self.reinstruccion = Reinstruccion(1, self.reinstructor, self.conductor)

    def test_generar_nombre(self):
        nombre = self.reinstruccion.generar_nombre()
        self.assertEqual(nombre, "Jaime Lique Tinte_26092024_Luis Trujillo")  # Cambia la fecha según sea necesario

    def test_verificar_realizado(self):
        self.reinstruccion.verificar_realizado()
        self.assertFalse(self.reinstruccion.realizado_bool)

    def test_imprimir(self):
        self.reinstruccion.imprimir()  # Verifica manualmente la salida en consola

# Ejecutar las pruebas al correr el archivo
if __name__ == "__main__":
    unittest.main()
