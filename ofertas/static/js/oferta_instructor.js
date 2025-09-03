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






});
