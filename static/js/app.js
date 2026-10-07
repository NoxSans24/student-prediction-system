// App initialization
console.log('Student Performance Analytics loaded');

// Global search in topbar
const topbarSearch = document.getElementById('topbarSearch');
if (topbarSearch) {
    topbarSearch.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = topbarSearch.value.trim();
            if (query) {
                window.location.href = `/students?search=${encodeURIComponent(query)}`;
            }
        }
    });
}
