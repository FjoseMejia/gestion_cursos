    // Filtrado en tiempo real de la tabla de solicitudes
    const searchInput = document.getElementById("request-search");
    const tableBody = document.getElementById("all-requests-table-body");

    if (searchInput && tableBody) {
        searchInput.addEventListener("input", function () {
            const searchText = this.value.toLowerCase();
            const rows = tableBody.getElementsByTagName("tr");

            for (let row of rows) {
                const cells = row.getElementsByTagName("td");
                let match = false;

                for (let cell of cells) {
                    if (cell.textContent.toLowerCase().includes(searchText)) {
                        match = true;
                        break;
                    }
                }

                row.style.display = match ? "" : "none";
            }
        });
    }
