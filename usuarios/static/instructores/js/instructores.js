// Acomodar el JS para la vista de Instructores _david
// Esperar a que cargue la página
document.addEventListener("DOMContentLoaded", function() {
    console.log("JS de Instructor cargado correctamente ✅");

    // Cambiar el color del título <h1> dinámicamente
    const titulo = document.querySelector("h1");
    if (titulo) {
        titulo.style.color = "#022549"; // azul
    }

    // Si tienes un formulario, podrías validar campos
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(e) {
            const inputs = form.querySelectorAll("input[required]");
            let valido = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valido = false;
                    input.style.border = "2px solid red";
                } else {
                    input.style.border = "1px solid #d1d5db";
                }
            });

            if (!valido) {
                e.preventDefault();
                alert("Por favor completa todos los campos obligatorios.");
            }
        });
    }
});
