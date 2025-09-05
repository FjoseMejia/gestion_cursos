document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("new-request-btn").addEventListener("click", () => {
        showModal("request-modal");
    });

    function showModal(modalId) {
      document.getElementById(modalId).style.display = "block";
    }

    function hideModal(modalId) {
      document.getElementById(modalId).style.display = "none";
    }

    document.querySelectorAll(".close").forEach((closeBtn) => {
        closeBtn.addEventListener("click", () => {
          const modal = closeBtn.closest(".modal");
          modal.style.display = "none";
        });
    });

    document.getElementById("cancel-request")
        .addEventListener("click", () => {
          hideModal("request-modal");
    });



    //Filtrar cursos
    const selectorDuracion = document.querySelector("#selector-duracion");
    const selectorCursos = document.querySelector("#selector-cursos");

    selectorDuracion.addEventListener('change', function() {
        const duracion = this.value;

        // limpiar cursos anteriores
        selectorCursos.innerHTML = '<option value="">Escoge curso</option>';

    if (!duracion) return;

    fetch(`/ofertas/api/programas_sugeridos/?duracion=${duracion}`)
        .then(res => res.json())
        .then(data => {

            selectorCursos.innerHTML = "";


            data.forEach(programa => {
                const option = document.createElement("option");
                option.value = Number(programa.id);
                option.textContent = programa.nombre;
                selectorCursos.appendChild(option);
            });
        });
    });

    //Mostrando inputs
    const tipoOferta = document.getElementById("id_tipo_oferta");

    // Todos los campos de empresa en un array
    const camposEmpresa = [
        document.getElementById("id_empresa_nit"),
        document.getElementById("id_empresa_nombre"),
        document.getElementById("id_empresa_subsector"),
        document.getElementById("id_archivo")
    ];

    // Función que muestra u oculta los campos
    function actualizarCamposEmpresa() {
        if (tipoOferta.value === "CERRADA") {
            camposEmpresa.forEach(c => c.parentElement.style.display = "block");
        } else {
            camposEmpresa.forEach(c => c.parentElement.style.display = "none");
        }
    }

    // Inicializar al cargar
    actualizarCamposEmpresa();

    // Escuchar cambios en el select
    tipoOferta.addEventListener("change", actualizarCamposEmpresa);

});
