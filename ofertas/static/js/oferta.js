
document.addEventListener("DOMContentLoaded", () => {
  const log = (...args) => console.info("[ofertas.js]", ...args);


  function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) { log("showModal: modal no encontrado", modalId); return; }
    modal.style.display = "block";
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }
  function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) { log("hideModal: modal no encontrado", modalId); return; }
    modal.style.display = "none";
    modal.classList.remove("active");
    document.body.style.overflow = "";
  }


  const newRequestBtn = document.getElementById("new-request-btn");
  if (newRequestBtn) {
    newRequestBtn.addEventListener("click", (e) => {
      e.preventDefault();
      showModal("request-modal"); // asegúrate que tu modal tiene id="request-modal"
    });
  } else {
    log("new-request-btn no existe (ok si no usas botón fuera del modal)");
  }


  document.querySelectorAll(".close").forEach(closeBtn => {
    closeBtn.addEventListener("click", () => {
      const modal = closeBtn.closest(".modal");
      if (modal) {
        modal.style.display = "none";
        modal.classList.remove("active");
        document.body.style.overflow = "";
      }
    });
  });


  const cancelBtn = document.getElementById("cancel-request");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", (e) => {
      e.preventDefault();
      hideModal("request-modal");
    });
  } else {
    log("cancel-request no encontrado");
  }

  document.querySelectorAll(".modal").forEach(modal => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.style.display = "none";
        modal.classList.remove("active");
        document.body.style.overflow = "";
      }
    });
  });

  const selectorDuracion = document.querySelector("#selector-duracion");
  const selectorCursos = document.querySelector("#selector-cursos");

  if (selectorDuracion && selectorCursos) {
    selectorDuracion.addEventListener('change', function () {
      const duracion = this.value;
      selectorCursos.innerHTML = '<option value="">Escoge curso</option>';
      if (!duracion) return;

      fetch(`/ofertas/api/programas_sugeridos/?duracion=${encodeURIComponent(duracion)}`)
        .then(res => {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(data => {
          selectorCursos.innerHTML = '<option value="">Escoge curso</option>';
          data.forEach(programa => {
            const option = document.createElement("option");
            option.value = programa.id;
            option.textContent = programa.nombre;
            selectorCursos.appendChild(option);
          });
        })
        .catch(err => log("error fetch programas:", err));
    });
  } else {
    log("selector-duracion o selector-cursos no encontrados (skip fetch).");
  }


  const tipoOferta = document.getElementById("id_tipo_oferta");
  const camposEmpresaIds = ["id_empresa_nit", "id_empresa_nombre", "id_empresa_subsector", "id_archivo"];
  const camposEmpresa = camposEmpresaIds.map(id => document.getElementById(id)).filter(Boolean);

function actualizarCamposEmpresa() {
    if (!tipoOferta) return;
    const mostrar = tipoOferta.value === "CERRADA";
    const collapsible = document.querySelector('.ocultar'); // todo el bloque

    if (collapsible) {
        collapsible.style.display = mostrar ? "" : "none";
    }
}

tipoOferta.addEventListener('change', actualizarCamposEmpresa);

  /* ===== Collapsibles (abrir/cerrar) ===== */
  document.querySelectorAll(".collapsible").forEach((collapsible, index) => {
    const header = collapsible.querySelector(".collapsible-header");
    const body = collapsible.querySelector(".collapsible-body");

    if (!header || !body) return;

    if (index === 0) {
      collapsible.classList.add("active");
      body.style.display = "block";
      body.style.maxHeight = body.scrollHeight + "px";
    } else {
      body.style.display = "none";
      body.style.maxHeight = null;
    }

    header.addEventListener("click", () => {
      const isActive = collapsible.classList.toggle("active");
      if (isActive) {
        body.style.display = "block";
        const h = body.scrollHeight;
        body.style.maxHeight = h + "px";
      } else {
        body.style.maxHeight = null;

        setTimeout(() => { body.style.display = "none"; }, 300);
      }
    });
  });

});
