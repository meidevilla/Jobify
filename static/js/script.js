// function toggleNav() {
//     const sideNav = document.getElementById('sideNav');
//     sideNav.classList.toggle('toggled');
// }
// document.addEventListener('click', function (event) {
//     const sideNav = document.getElementById('sideNav');
//     if (sideNav.classList.contains('toggled') && !sideNav.contains(event.target)) {
//         sideNav.classList.remove('toggled');
//     }
// });
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

    // Add click listeners to all <th> elements
    table.querySelectorAll("th").forEach((header, index) => {
        const icon = header.querySelector("i"); // Get the Font Awesome icon
        header.addEventListener("click", () => {
            const type = header.dataset.sort; // 'string' or 'number'
            const tbody = table.querySelector("tbody");
            const rows = Array.from(tbody.querySelectorAll("tr"));

            // Toggle sorting direction
            const isAscending = header.dataset.order === "asc";
            header.dataset.order = isAscending ? "desc" : "asc";

            // Update sort icons
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

            // Append sorted rows back into the table body
            rows.forEach(row => tbody.appendChild(row));
        });
    });
});

// Function to switch sections
function toggleSections(activeLink, sectionToShow, sectionToHide) {
    // Remove 'active' class from all sidebar links
    let links = document.querySelectorAll(".sidebar a");
    links.forEach(link => link.classList.remove("active"));
    
    // Add 'active' class to the clicked link
    activeLink.classList.add("active");

    // Hide the other section and show the selected section
    document.getElementById(sectionToHide).style.display = "none";
    document.getElementById(sectionToShow).style.display = "block";
}

// Event listeners for profile and security links
document.getElementById("profile-link").addEventListener("click", function(event) {
    event.preventDefault();
    toggleSections(this, "profile-section", "security-section");
});

document.getElementById("security-link").addEventListener("click", function(event) {
    event.preventDefault();
    toggleSections(this, "security-section", "profile-section");
});

