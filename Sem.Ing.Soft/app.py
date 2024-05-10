from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Configuración de la base de datos
server = 'LAPTOP-MM9H9HG1\\SQLEXPRESS'
database = 's_belleza'
username = 'soporte'
password = '123'
driver = '{ODBC Driver 17 for SQL Server}'

# Función para conectar a la base de datos
def conectar_bd():
    return pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# Función para realizar el registro de usuarios
@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['mail']
        contrasena = request.form['contrasena']  # Añadido el campo de contraseña
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tbl_usuario (nombre, apellido, mail, contrasena, telefono, direccion) VALUES (?, ?, ?, ?, ?, ?)", (nombre, apellidos, email, contrasena, telefono, direccion))
            conn.commit()
            cursor.close()
            conn.close()
            return 'Registro exitoso'  # O puedes redirigir a otra página de éxito
        except Exception as e:
            return 'Error en el registro: ' + str(e)  # Maneja el error de manera adecuada

# Ruta para la página de registro
@app.route('/registro', methods=['GET'])
def mostrar_formulario_registro():
    return render_template('registro.html')

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de inicio de sesión
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
