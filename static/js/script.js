document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth'
    });
    calendar.render();
  });

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("applications-table");

    table.querySelectorAll("th").forEach((header, index) => {
        const icon = header.querySelector("i");
        header.addEventListener("click", () => {
            const type = header.dataset.sort;
            const tbody = table.querySelector("tbody");
            const rows = Array.from(tbody.querySelectorAll("tr"));

            const isAscending = header.dataset.order === "asc";
            header.dataset.order = isAscending ? "desc" : "asc";


            table.querySelectorAll("i").forEach(i => i.className = "fa-solid fa-sort");
            icon.className = isAscending
                ? "fa-solid fa-sort-up"
                : "fa-solid fa-sort-down";

            // Sort rows
            rows.sort((rowA, rowB) => {
                const cellA = rowA.cells[index].innerText.trim().toLowerCase();
                const cellB = rowB.cells[index].innerText.trim().toLowerCase();

                if (type === "number") {
                    return isAscending
                        ? parseFloat(cellA) - parseFloat(cellB)
                        : parseFloat(cellB) - parseFloat(cellA);
                } else {
                    return isAscending
                        ? cellA.localeCompare(cellB)
                        : cellB.localeCompare(cellA);
                }
            });
            rows.forEach(row => tbody.appendChild(row));
        });
    });
});

function toggleSections(activeLink, sectionToShow, sectionToHide) {
    let links = document.querySelectorAll(".sidebar a");
    links.forEach(link => link.classList.remove("active"));
    activeLink.classList.add("active");
    document.getElementById(sectionToHide).style.display = "none";
    document.getElementById(sectionToShow).style.display = "block";
}

document.getElementById("profile-link").addEventListener("click", function(event) {
    event.preventDefault();
    toggleSections(this, "profile-section", "security-section");
});

document.getElementById("security-link").addEventListener("click", function(event) {
    event.preventDefault();
    toggleSections(this, "security-section", "profile-section");
});

