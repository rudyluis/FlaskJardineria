// Función para cargar los datos de la oficina seleccionada en la modal de edición
function editarOficina(idOficina, codigoOficina, ciudad, pais, codigopostal, telefono, lineadireccion1, lineadireccion2, region) {
    document.getElementById('editarIdOficina').value = idOficina;
    document.getElementById('editarCodigoOficina').value = codigoOficina;
    document.getElementById('editarCiudad').value = ciudad;
    document.getElementById('editarPais').value = pais;
    document.getElementById('editarCodigopostal').value = codigopostal;
    document.getElementById('editarTelefono').value = telefono;
    document.getElementById('editarLineadireccion1').value = lineadireccion1;
    document.getElementById('editarLineadireccion2').value = lineadireccion2;
    document.getElementById('editarRegion').value = region;

    // Modificar el atributo 'action' del formulario con la URL adecuada
    var editarOficinaForm = document.getElementById('editarOficinaForm');
    editarOficinaForm.action = '/oficina/editar/' + idOficina;

    // Abrir la modal de edición
    var myModal = new bootstrap.Modal(document.getElementById('modalEditarOficina'), {
        keyboard: false
    });
    myModal.show();
}
