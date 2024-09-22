function toggleSearchButton() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    if (searchInput.value.trim() !== '') {
        searchButton.disabled = false;
        searchButton.classList.remove('bg-gray-500', 'text-gray-300', 'cursor-not-allowed');
        searchButton.classList.add('bg-blue-600', 'text-white', 'cursor-pointer');
    } else {
        searchButton.disabled = true;
        searchButton.classList.remove('bg-blue-600', 'text-white', 'cursor-pointer');
        searchButton.classList.add('bg-gray-500', 'text-gray-300', 'cursor-not-allowed');
    }
}

// Initial check to disable the button if the page is loaded with empty input
document.addEventListener('DOMContentLoaded', () => {
    toggleSearchButton();
});