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
    const selectorNiveles= document.querySelector("#selector-horas");
    const selectorCursos= document.querySelector("#selector-cursos");

    fetch('/api/niveles/')
        .then(response => response.json())
        .then(data => {
            data.forEach(nivel => {
                selectorNiveles.innerHTML += `<option value="${nivel.id}">${nivel.nombre}</option>`;
            });
        });

    selectorNiveles.addEventListener('change', function() {
    const nivelId = this.value;

    selectorCursos.innerHTML = '<option value="">-- Escoge curso --</option>';

    if (!nivelId) return;

    fetch(`/api/cursos_por_nivel/${nivelId}/`)
        .then(res => res.json())
        .then(data => {
            data.forEach(curso => {
                selectorCursos.innerHTML += `<option value="${curso.id}">${curso.nombre}</option>`;
            });
        });

});
