

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleEstado(id) {
    if (!id) {
        console.error("toggleEstado: id inválido", id);
        alert("Error: id inválido.");
        return;
    }

    const url = `/usuarios/instructores/activar/${id}/`;
    const csrftoken = getCookie("csrftoken");
    console.log("toggleEstado ->", url, "csrftoken:", csrftoken);

    fetch(url, {
        method: "POST",
        credentials: "same-origin",              // asegura enviar cookies
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            // muestra texto del servidor para mejores pistas
            return response.text().then(text => {
                throw new Error(`HTTP ${response.status} — ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        if (!data.success) throw new Error(data.error || "Respuesta sin success=true");

        const btn = document.getElementById(`btn-estado-${id}`);
        const estadoTd = document.getElementById(`estado-${id}`);

        if (data.new_status) {
            btn.innerHTML = "🚫";
            btn.title = "Desactivar";
            estadoTd.innerHTML = `<span class="estado activo">Activo ✓</span>`;
        } else {
            btn.innerHTML = "✅";
            btn.title = "Activar";
            estadoTd.innerHTML = `<span class="estado inactivo">Inactivo ✗</span>`;
        }
    })
    .catch(err => {
        console.error("toggleEstado error:", err);
        alert("No se pudo cambiar el estado. Revisa la consola (Network/Console) para más detalles.");
    });
}
