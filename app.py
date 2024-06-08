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


#### agregar empleado
@app.route('/empleado/agregar', methods=['GET', 'POST'])
def agregar_empleado():
    if request.method == 'POST':
        try:
            session = DBSession()
            # Obtener los valores del formulario
            
            codigo_empleado = request.form['codigoEmpleado']
            nombre = request.form['nombre']
            apellido1 = request.form['apellido1']
            apellido2 = request.form['apellido2']
            extension = request.form['extension']
            email = request.form['email']
            idoficina = request.form['idOficina']
            idempleadojefe = request.form['idEmpleadoJefe']
            puesto = request.form['puesto']
            print(request.form)
            # Validación de datos
            if not codigo_empleado or not nombre or not apellido1 or not extension or not email or not idoficina:
                # Manejo de campos obligatorios
                flash('Todos los campos son obligatorios', 'error')
                return redirect(url_for('listar_empleado'))
            print(request.form)
            # Agregar empleado a la base de datos
            Empleado.agregarEmpleado(session,
                                     codigo_empleado=codigo_empleado,
                                     nombre=nombre,
                                     apellido1=apellido1,
                                     apellido2=apellido2,
                                     extension=extension,
                                     email=email,
                                     id_oficina=idoficina,
                                     id_empleado_jefe=idempleadojefe,
                                     puesto=puesto)
            session.close()
            flash('Empleado agregado correctamente', 'success')
            return redirect(url_for('listar_empleado'))
        except IntegrityError as e:
            # Manejo de violaciones de restricciones únicas
            flash('Error: El código de empleado ya existe', 'error')
            return redirect(url_for('listar_empleado'))
        except Exception as e:
            # Manejo de otros errores
            flash(f'Error al agregar empleado {e}', 'error')
            return redirect(url_for('listar_empleado'))
    else:
        return redirect(url_for('listar_empleado'))



# Eliminar oficina
@app.route('/empleado/eliminar/<int:id_empleado>')
def eliminar_empleado(id_empleado):
    try: 

        session = DBSession()
        empleado= session.query(Empleado).filter_by(idempleado=id_empleado).first()

        session.delete(empleado)
        session.commit()
        session.close()
        flash('Se elimino el registro correctamente', 'error')
        return redirect(url_for('listar_empleado'))
    except IntegrityError as e:
        # Manejo de violaciones de restricciones únicas
        e._message
        flash(f'Error: No se puede eliminar el registro por que esta vinculado {e}' , 'error')
        return redirect(url_for('listar_empleado'))

#Editar empleado
@app.route('/empleado/editarDatos',methods=['POST'])
def editar_datos_empleado():
    try: 

        id_empleado = request.form['id_empleado']
        session = DBSession()
        empleado= session.query(Empleado).filter_by(idempleado=id_empleado).first()
        session.close()
        # Devolver los detalles del empleado como un JSON
        if empleado:
            return jsonify({
                'id_empleado': empleado.idempleado,
                'codigo_empleado': empleado.codigo_empleado,
                'nombre': empleado.nombre,
                'apellido1': empleado.apellido1,
                'apellido2': empleado.apellido2,
                'extension': empleado.extension,
                'email': empleado.email,
                'idoficina': empleado.idoficina,
                'idempleadojefe': empleado.idempleadojefe,
                'puesto': empleado.puesto
            })
        else:
            return jsonify({'error': 'No se encontró el empleado con el ID proporcionado'})
    except IntegrityError as e:
        # Manejo de violaciones de restricciones únicas
        e._message
        flash(f'Error: No se puede Obtener el registro  {e}' , 'error')
        return redirect(url_for('listar_empleado'))


if __name__=='__main__':
    app.run(debug=True)



