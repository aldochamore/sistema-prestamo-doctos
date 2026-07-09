from flask import Flask, render_template, request, redirect, url_for, flash
import db  # <--- ¡MIRA! Estamos importando tu archivo anterior como si fuera una librería

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  # Necesario para enviar mensajes (Flash messages)

# --- RUTA 1: La Página de Inicio (El Menú) ---
@app.route('/')
def index():
    # 1. Pedimos la lista a la base de datos
    datos_prestamos = db.obtener_prestamos_activos()
    
    # 2. Se la enviamos al HTML usando una variable (prestamos=datos_prestamos)
    return render_template('index.html', prestamos=datos_prestamos)
# --- RUTA 2: Procesar el Préstamo ---
@app.route('/prestar', methods=['POST'])
def prestar():
    # Recibimos los datos del formulario web (no del input de consola)
    usuario = request.form['usuario']
    documento = request.form['documento']
    
    # Llamamos a tu función original. 
    # NOTA: Tendremos que modificar levemente db.py para que devuelva mensajes en vez de hacer "print"
    mensaje = db.registrar_prestamo_web(usuario, documento)
    
    flash(mensaje) # Enviamos el mensaje a la pantalla
    return redirect(url_for('index'))

# --- RUTA 3: Procesar la Devolución ---
@app.route('/devolver', methods=['POST'])
def devolver():
    documento = request.form['documento']
    mensaje = db.registrar_devolucion_web(documento)
    flash(mensaje)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # debug=True permite que si cambias código, la web se actualice sola
    app.run(debug=True, port=5000)