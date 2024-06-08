
function editarEmpleado(idEmpleado) {
    // Lógica para cargar los datos del empleado en la modal de edición
    $.ajax({
        type: 'POST',
        url: '/empleado/editarDatos', // La URL no necesita incluir el ID del empleado en este caso
        data: { id_empleado: idEmpleado },
        success: function(response) {
            document.getElementById('editarIdEmpleado').value = response.id_empleado;
            document.getElementById('editarCodigoEmpleado').value = response.codigo_empleado;
            document.getElementById('editarNombre').value = response.nombre;
            document.getElementById('editarApellido1').value = response.apellido1;
            document.getElementById('editarApellido2').value = response.apellido2;
            document.getElementById('editarExtension').value = response.extension;
            document.getElementById('editarEmail').value = response.email;
            document.getElementById('editarIdOficina').value = response.idoficina;
            document.getElementById('editarIdEmpleadoJefe').value = response.idempleadojefe;
            document.getElementById('editarPuesto').value = response.puesto;
        },
        error: function(xhr, status, error) {
            // Manejar cualquier error que ocurra durante la solicitud AJAX
            console.error(error);
            alert('Error al cargar los datos del empleado');
        }
    });

    // Modificar el atributo 'action' del formulario con la URL adecuada
    var editarEmpleadoForm = document.getElementById('editarEmpleadoForm');
    editarEmpleadoForm.action = '/empleado/editar/' + idEmpleado;

    // Abrir la modal de edición
    var myModal = new bootstrap.Modal(document.getElementById('modalEditarEmpleado'), {
        keyboard: false
    });
    myModal.show();
}
