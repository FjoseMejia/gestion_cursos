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
    const duracionSelect = document.getElementById('duracion-select');
const suggestions = document.getElementById('programa-suggestions');

// Traer duraciones de la BD y llenar el select
fetch('/ofertas/duraciones-disponibles/')
    .then(res => res.json())
    .then(data => {
        data.forEach(d => {
            const option = document.createElement('option');
            option.value = d;
            option.textContent = `${d} horas`;
            duracionSelect.appendChild(option);
        });
    });

// Cuando el usuario selecciona una duración, filtrar programas
duracionSelect.addEventListener('change', () => {
    const duracion = duracionSelect.value;
    fetch(`/ofertas/programas-sugeridos/?duracion=${duracion}`)
        .then(res => res.json())
        .then(data => {
            suggestions.innerHTML = '';
            data.forEach(p => {
                const div = document.createElement('div');
                div.textContent = `${p.nombre} - ${p.duracion} horas`;
                suggestions.appendChild(div);
            });
        });
});

});
