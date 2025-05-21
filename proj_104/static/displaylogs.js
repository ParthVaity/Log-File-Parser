//Handles all the filtering, sorting and downloading on the logdisplay.html page

document.addEventListener('DOMContentLoaded', function () {
    //Initializing all the values
    const table = document.getElementById('logTable');
    const headers = Array.from(table.tHead.querySelectorAll('th'));
    const tbody = table.tBodies[0];
    const originalRows = Array.from(tbody.rows).map(r => r.cloneNode(true));
    const filterButton = document.getElementById('timefilter');
    const modal = document.getElementById('filterModal');
    const applyButton = document.getElementById('applyFilter');
    const cancelButton = document.getElementById('cancelFilter');
    const minInput = document.getElementById('minTime');
    const maxInput = document.getElementById('maxTime');
    const resetButton = document.getElementById('resetbutton');
    const downloadButton = document.getElementById('downloadtable');
    const eventFilter = document.getElementById('eventFilter');
    const levelFilter = document.getElementById('levelFilter');
    const headerText = headers.map(h => h.querySelector('span').textContent);
    let sortDir = {};//tracks direction of sort


    //Applying time filters
    filterButton.addEventListener('click', () => modal.style.display = 'flex');
    cancelButton.addEventListener('click', () => modal.style.display = 'none');

    applyButton.addEventListener('click', () => {
        modal.style.display = 'none';
        applyFilters();
    });


    //Sorting the columns in ascending and descending order
    headers.forEach((th, col) => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', (e) => {   
            const minT = minInput.value ? Date.parse(minInput.value) : -Infinity;
            const maxT = maxInput.value ? Date.parse(maxInput.value) : Infinity;

            let rows = Array.from(tbody.rows).filter(r => {
                const t = Date.parse(r.cells[1].textContent);
                return t >= minT && t <= maxT;
            });

            const isNum = rows.every(r => !isNaN(r.cells[col].textContent) && r.cells[col].textContent.trim() !== '');

            headers.forEach((h, i) => {
                h.querySelector('span').textContent = headerText[i];
                h.classList.remove('sorted-asc', 'sorted-desc');
            });

            sortDir[col] = sortDir[col] === 'asc' ? 'desc' : 'asc';
            th.classList.add(sortDir[col] === 'asc' ? 'sorted-asc' : 'sorted-desc');

            rows.sort((a, b) => {
                let A = a.cells[col].textContent.trim();
                let B = b.cells[col].textContent.trim();

                if (col === 1) {
                    A = Date.parse(A); B = Date.parse(B);
                } else if (isNum) {
                    A = parseFloat(A); B = parseFloat(B);
                } else {
                    A = A.toLowerCase(); B = B.toLowerCase();
                }

                return (A < B) ? (sortDir[col] === 'asc' ? -1 : 1) : (A > B ? (sortDir[col] === 'asc' ? 1 : -1) : 0);
            });

            tbody.innerHTML = '';
            rows.forEach(r => tbody.appendChild(r));
        });
    });


    //Filtering the rows based on level,event and min,max times
    function applyFilters() {
        const selectedLevel = levelFilter.value;
        const selectedEvent = eventFilter.value;
        const minT = minInput.value ? Date.parse(minInput.value) : -Infinity;
        const maxT = maxInput.value ? Date.parse(maxInput.value) : Infinity;

        Array.from(tbody.rows).forEach(row => {
            const time = Date.parse(row.cells[1].textContent.trim());
            const level = row.cells[2].textContent.trim();
            const event = row.cells[4].textContent.trim();

            const levelMatch = (selectedLevel === 'ALL' || level === selectedLevel);
            const eventMatch = (selectedEvent === 'ALL' || event === selectedEvent);
            const timeMatch = (time >= minT && time <= maxT);

            row.style.display = (levelMatch && eventMatch && timeMatch) ? '' : 'none';
        });
    }
    

    //Applying event and level filters
    eventFilter.addEventListener('change', applyFilters);
    levelFilter.addEventListener('change', applyFilters);

    
    //Reset button to revert to initial table
    resetButton.addEventListener('click', () => {
        levelFilter.value = 'ALL';
        eventFilter.value = 'ALL';
        minInput.value = '';
        maxInput.value = '';
        sortDir = {};

        headers.forEach((h, i) => {
            const s = h.querySelector('span');
            if (s) s.textContent = headerText[i];
            h.classList.remove('sorted-asc', 'sorted-desc');
        });

        tbody.innerHTML = '';
        originalRows.forEach(r => tbody.appendChild(r.cloneNode(true)));
    });


    //Converting table to csv for exporting
    function tableToCSV() {
        const rows = Array.from(tbody.rows);
        const header = ['LineId', 'Time', 'Level', 'Content', 'EventId', 'EventTemplate'];

        const csvRows = [header.join(',')];

        rows.forEach(row => {
            if (row.style.display !== 'none') {
                const rowData = Array.from(row.cells).map(cell => `"${cell.textContent.trim().replace(/"/g, '""')}"`);
                csvRows.push(rowData.join(','));
            }
        });

        return csvRows.join('\n');
    }


    //Doanloading the current version of table
    downloadButton.addEventListener('click', () => {
        const csvContent = tableToCSV();
        const filename = 'table_data.csv';
        downloadCSV(csvContent, filename);
    });

    function downloadCSV(csvContent, filename) {
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }
});
