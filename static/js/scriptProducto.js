$(document).ready(function() {
    $('#agregarProducto').click(function() {
        const productoSelect = $('#producto');
        const cantidadInput = $('#cantidad');
        const productoId = productoSelect.val();
        const productoNombre = productoSelect.find('option:selected').text();
        const precioUnitario = parseFloat(productoSelect.find('option:selected').data('precio'));
        const cantidad = parseInt(cantidadInput.val());
        const total = (precioUnitario * cantidad).toFixed(2);

        if (productoId && cantidad > 0) {
            const newRow = `
                <tr>
                    <td>${productoNombre}</td>
                    <td>${cantidad}</td>
                    <td>${precioUnitario.toFixed(2)}</td>
                    <td class="totalProducto">${total}</td>
                    <td><button type="button" class="btn btn-danger btn-sm eliminarProducto">Eliminar</button></td>
                    <input type="hidden" name="productos[]" value="${productoId}">
                    <input type="hidden" name="cantidades[]" value="${cantidad}">
                </tr>
            `;
            $('#productosSeleccionados tbody').append(newRow);
            actualizarTotalPedido();
        } else {
            alert('Por favor, selecciona un producto y especifica una cantidad válida.');
        }
    });

    $(document).on('click', '.eliminarProducto', function() {
        $(this).closest('tr').remove();
        actualizarTotalPedido();
    });

    function actualizarTotalPedido() {
        let totalPedido = 0;
        $('#productosSeleccionados tbody tr').each(function() {
            const totalProducto = parseFloat($(this).find('.totalProducto').text());
            totalPedido += totalProducto;
        });
        $('#totalPedido').text(totalPedido.toFixed(2));
    }
});