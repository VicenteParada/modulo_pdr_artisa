#####################################################################################################
###########################           BIBLIOT DEL SISTEMA           #################################
#####################################################################################################



from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyodbc





#####################################################################################################
###########################           CLASES DEL SISTEMA           #################################
#####################################################################################################





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
    def __init__(self, id_reinstruccion, reinstructor, conductor, fecha_asignacion, realizado_bool=False):
        self.id_reinstruccion = id_reinstruccion
        self.reinstructor = reinstructor
        self.conductor = conductor
        self.fecha_asignacion = datetime.now().strftime("%d/%m/%Y")  # Mantener la fecha con "/"
        self.realizado_bool = realizado_bool
    
    # Método para generar el nombre basado en el formato especificado, eliminando las "/"
    def generar_nombre(self):
        # Reemplazar las barras "/" en la fecha para el nombre del archivo
        fecha_sin_barras = self.fecha_asignacion.replace("/", "")
        return f"{self.conductor.nombre_conductor}_{fecha_sin_barras}_{self.reinstructor.nombre_reinstructor}"
    
    # Método para verificar si el archivo existe (en esta versión siempre devuelve False)
    def verificar_realizado(self):
        # Aquí ya no se hace ninguna validación, siempre será False
        self.realizado_bool = False

    # Método para imprimir la reinstrucción
    def imprimir(self):
        print(f"conductor: {self.conductor.nombre_conductor}")
        print(f"cant excesos: {self.conductor.cantidad_excesos}")
        print(f"fecha: {self.fecha_asignacion}")  # Aquí mantendremos la fecha con "/"
        print(f"a cargo de: {self.reinstructor.nombre_reinstructor}")
        print(f"estado: {'Realizado' if self.realizado_bool else 'No realizado'}")
        print(f"correo_reinstructor: {self.correo_reinstructor}")


#####################################################################################################
###########################           FUNCIONES DE CORREO           #################################
#####################################################################################################





    def enviar_correo(self, smtp_server, smtp_port, remitente, password):
        asunto = "Reinstrucción Automática"
        cuerpo = f"""
        Estimado {self.reinstructor.nombre_reinstructor},

        Esperando que se encuentre bien. Se le escribe para informar que hemos detectado un total de 
        {self.conductor.cantidad_excesos} excesos del conductor {self.conductor.nombre_conductor}
        asignado el dia {self.fecha_asignacion}.


        Agradecemos tu comprensión y tu compromiso con la mejora continua.

        Saludos cordiales,
        Departamento de Prevencion de Riesgos ARTISA

        Correo Automatizado NO RESPONDER

        """

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = self.reinstructor.correo_reinstructor
        msg['Subject'] = asunto

        # Agregar el cuerpo del correo
        msg.attach(MIMEText(cuerpo, 'plain'))

        try:
            # Conectar al servidor SMTP
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Iniciar conexión segura
                server.login(remitente, password)  # Iniciar sesión
                server.send_message(msg)  # Enviar el mensaje

            print("Correo enviado con éxito.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")



