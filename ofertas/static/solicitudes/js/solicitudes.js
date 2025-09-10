function cargarArchivo(tipo) {
  const div = document.getElementById(tipo);
  div.classList.add("cargado");
}

function enviarLink() {
  alert("📎 Se envió un link de descarga.");
}

function enviarArchivos() {
  alert("✅ Archivos enviados correctamente.");
}
