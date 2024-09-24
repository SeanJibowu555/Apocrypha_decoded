document.addEventListener("DOMContentLoaded", function() {
    const toggleButtons = document.querySelectorAll(".toggle-translations");
    
    toggleButtons.forEach(button => {
        button.addEventListener("click", function() {
            const dropdown = this.nextElementSibling; // Get the corresponding dropdown
            if (dropdown.style.display === "none" || dropdown.style.display === "") {
                dropdown.style.display = "block"; // Show dropdown
            } else {
                dropdown.style.display = "none"; // Hide dropdown
            }
        });
    });

    const rows = document.querySelectorAll("tbody tr");
    
    rows.forEach(row => {
        row.addEventListener("click", function() {
            const bookName = this.cells[0].innerText; // Get the book name
            alert(`You clicked on ${bookName}`);
        });
    });
});
