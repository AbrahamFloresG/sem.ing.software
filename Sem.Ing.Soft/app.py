from flask import Flask, render_template
import pyodbc
import pytest

app = Flask(__name__)

# Conexion a la base de datos
server = 'LAPTOP-MM9H9HG1\\SQLEXPRESS'
database = 's_belleza'
username = 'soporte'
password = '123'
driver = '{ODBC Driver 17 for SQL Server}'

def obtener_datos():
    try:
        conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tu_tabla")  # Reemplaza 'tu_tabla' con el nombre real de tu tabla
        rows = cursor.fetchall()

        # Transforma los resultados en una lista de diccionarios para facilitar su uso en la plantilla HTML
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        cursor.close()
        conn.close()

        return data
    
    except Exception as e:
        print('Error al intentar conectarse a la base de datos:', e)
        return []

@app.route('/')
def index():
    datos = obtener_datos()
    return render_template('index.html', datos=datos)


@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Pruebas unitarias
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#prueva ruta principal que responda correctamente. Se realiza una solicitud HTTP
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

#prueva de la funcion de obtener datos, verifica que la lista de datos no este vacia
def test_obtener_datos():
    data = obtener_datos()
    assert len(data) > 0

if __name__ == '__main__':
    app.run(debug=True)

