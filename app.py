from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine,desc
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from Entity import Oficina,Empleado, Base
from sqlalchemy.exc import IntegrityError
app= Flask(__name__)

app.secret_key='123456'


# Crear conexión a la base de datos
engine = create_engine('postgresql://postgres:123456@localhost/jardineria')
Base.metadata.bind = engine

# Crear sesión de base de datos
DBSession = sessionmaker(bind=engine)

#Ruta Principal
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/oficina')
def listar_oficina():
    session= DBSession()
    oficinas =session.query(Oficina).all()
    session.close()
    return render_template('oficina.html',oficinas=oficinas)

 
# Agregar oficina
@app.route('/oficina/agregar', methods=['GET', 'POST'])
def agregar_oficina():
    if request.method == 'POST':
        session = DBSession()
        Oficina.agregarOficina(session,
                               request.form['codigooficina'],
                               request.form['ciudad'],
                               request.form['pais'],
                               request.form['codigopostal'],
                               request.form['telefono'],
                               request.form['lineadireccion1'],
                               request.form['lineadireccion2'],
                               request.form.get('region'))  # Puede ser None
        session.close()
        return redirect(url_for('listar_oficina'))
    else:
        return render_template('agregar_oficina.html')



# Editar oficina
@app.route('/oficina/editar/<int:id_oficina>', methods=['GET', 'POST'])
def editar_oficina(id_oficina):
    session = DBSession()
    if request.method == 'POST':
        # Modificar la oficina con los datos del formulario
        Oficina.modificarOficina(session, id_oficina,
                                 codigooficina=request.form['codigooficina'],
                                 ciudad=request.form['ciudad'],
                                 pais=request.form['pais'],
                                 codigopostal=request.form['codigopostal'],
                                 telefono=request.form['telefono'],
                                 lineadireccion1=request.form['lineadireccion1'],
                                 lineadireccion2=request.form['lineadireccion2'],
                                 region=request.form.get('region'))  # Puede ser None
        session.close()
        return redirect(url_for('listar_oficina'))
    else:
        # Obtener los datos de la oficina a editar
        oficina = session.query(Oficina).filter_by(idoficina=id_oficina).first()
        session.close()
        return render_template('index.html', oficina=oficina, editar=True)  # Pasar la bandera "editar" a la plantilla


# Eliminar oficina
@app.route('/oficina/eliminar/<int:id_oficina>')
def eliminar_oficina(id_oficina):
    session = DBSession()
    Oficina.eliminarOficina(session, id_oficina)
    session.close()
    return redirect(url_for('listar_oficina'))

### listar empleado
@app.route('/empleado')
def listar_empleado():
    session = DBSession()
    empleados = session.query(Empleado).all()
    oficinas = session.query(Oficina).all()
    
    return render_template('empleado.html',empleados=empleados, 
                           oficinas=oficinas,empleadoJefes=empleados)

if __name__=='__main__':
    app.run(debug=True)



