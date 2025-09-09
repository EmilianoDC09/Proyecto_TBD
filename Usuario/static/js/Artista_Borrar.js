// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {
    // Seleccionar todos los formularios de eliminación
    const forms = document.querySelectorAll('.form-eliminar');

    // Añadir un evento 'submit' a cada formulario
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            // Mostrar un mensaje de confirmación
            if (!confirm('¿Estás seguro de que quieres borrar esta canción?')) {
                e.preventDefault(); // Cancelar el envío del formulario si el usuario no confirma
            }
        });
    });
});