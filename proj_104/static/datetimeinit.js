//Initialises date and time for input in the graph pages

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('mintime').value = '1950-01-01T00:00';
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');
    const second = String(now.getSeconds()).padStart(2, '0');
    const formatted = `${year}-${month}-${day}T${hour}:${minute}:${second}`;
    document.getElementById('maxtime').value = formatted;
});