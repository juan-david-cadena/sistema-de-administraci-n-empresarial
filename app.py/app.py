from flask import *  # importa todo lo que flask necesita para funcionar
from base_de_datos import conectar  # trae la funcion que conecta con la base de datos
from config import config  # trae la configuracion del proyecto

app = Flask(__name__)  # crea la aplicacion principal de flask
app.secret_key = "clave_secreta_123"  # clave para que flask pueda recordar quien esta conectado


@app.route('/')  # dice que cuando alguien entre a la pagina principal se ejecute esta funcion
def index():
    return render_template('login.html')  # muestra la pagina del inicio de sesion


@app.route('/login', methods=['POST'])  # indica que esta parte se usa cuando se manda el formulario del login
def login():
    usuario = request.form['usuario'].strip()
    contrasena = request.form['contrasena'].strip()


    # Imprime lo que recibe Flask
    print("Usuario ingresado:", usuario)
    print("Contraseña ingresada:", contrasena)

    conn = conectar()
    cur = conn.cursor()  #pregunta a la base de  datos

    tablas = [  # lista de las tablas donde se va a buscar el usuario
        ('jefe', 'panel_jefe'),
        ('gerente', 'panel_gerente'),
        ('supervisor', 'panel_supervisor'),
        ('empleado', 'panel_empleado')
    ]

    columnas_id = {
    'jefe': 'id_jefe',
    'gerente': 'id_gerente',
    'supervisor': 'id_supervisor',
    'empleado': 'id_empleado'
    }

    for tabla, panel in tablas:
        cur.execute(
            f"SELECT {columnas_id[tabla]}, nombre FROM {tabla} WHERE nombre=%s AND contrasena=%s",
            (usuario, contrasena)
            )
        persona = cur.fetchone()

        print(f"Resultado en {tabla}: {persona}")  # depuración

        if persona:  # si encontro una persona
            session['nombre'] = persona[1]
            session['rol'] = tabla
            conn.close()
            return redirect(url_for(panel))
  # envia al usuario a su pagina especial segun su rol

    conn.close()  # si no encontro a nadie cierra la puerta de la base
    return render_template('login.html', error='Usuario o contraseña incorrectos')  # vuelve a mostrar el login y avisa que los datos estaban mal



@app.route('/panel_jefe')  # si el usuario es jefe se muestra esta pagina
def panel_jefe():
    return render_template('panel_jefe.html', nombre=session.get('nombre'))  # muestra la pagina del jefe y enseña su nombre


@app.route('/panel_gerente')  # si el usuario es gerente se muestra esta pagina
def panel_gerente():
    return render_template('panel_gerente.html', nombre=session.get('nombre'))  # muestra la pagina del gerente con su nombre


@app.route('/panel_supervisor')  # si el usuario es supervisor se muestra esta pagina
def panel_supervisor():
    return render_template('panel_supervisor.html', nombre=session.get('nombre'))  # muestra la pagina del supervisor con su nombre


@app.route('/panel_empleado')  # si el usuario es empleado se muestra esta pagina
def panel_empleado():
    return render_template('panel_empleado.html', nombre=session.get('nombre'))  # muestra la pagina del empleado con su nombre


if __name__ == '__main__':  # dice que si este archivo se ejecuta directamente se corra la aplicacion
    app.config.from_object(config['development'])  # usa la configuracion de desarrollo
    app.run()  # inicia la aplicacion para que funcione en el navegador
