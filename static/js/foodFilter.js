const filterBtn = document.getElementById('filterBtn');
const filterPopup = document.getElementById('filterPopup');
const closePopup = document.querySelector('.close-popup');
const searchInput = document.getElementById('searchInput');
const searchForm = document.getElementById('searchForm');

// Open the filter popup
filterBtn.addEventListener('click', () => {
    filterPopup.style.display = 'block';
});

// Close the filter popup
closePopup.addEventListener('click', () => {
    filterPopup.style.display = 'none';
});

// Close the popup when clicking outside of it
window.addEventListener('click', event => {
    if (event.target == filterPopup) {
        filterPopup.style.display = 'none';
    }
});

// Real-time search functionality
let timeout = null;
if (searchInput && searchForm) {
    searchInput.addEventListener('input', () => {
        clearTimeout(timeout); // Clear any existing timeout
        timeout = setTimeout(() => {
            searchForm.submit(); // Submit the form
        }, 300); // Delay to prevent excessive submissions
    });
}
