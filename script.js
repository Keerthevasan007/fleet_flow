document.addEventListener('DOMContentLoaded', () => {
    
    // 1. MOCK DATA 
    // Simulating a backend response with vehicle types added for filtering
    const fleetData = [
        { id: "Van-05", type: "van", driver: "Alex", status: "On Trip", dest: "Warehouse B", eta: "14:30" },
        { id: "Truck-02", type: "truck", driver: "Sarah", status: "In Shop", dest: "N/A", eta: "-" },
        { id: "Bike-10", type: "bike", driver: "Mike", status: "On Trip", dest: "City Center", eta: "13:45" },
        { id: "Van-01", type: "van", driver: "Unassigned", status: "Idle", dest: "Depot", eta: "-" },
        { id: "Truck-05", type: "truck", driver: "John", status: "On Trip", dest: "North Sector", eta: "16:00" },
        { id: "Bike-22", type: "bike", driver: "Lara", status: "Idle", dest: "Depot", eta: "-" }
    ];

    // Select DOM elements
    const tableBody = document.getElementById('fleet-table-body');
    const filterDropdown = document.querySelector('.filter-dropdown');
    const activeFleetCount = document.querySelector('.kpi-card:nth-child(1) .big-number'); // Selects the "Active Fleet" number

    // 2. RENDER TABLE FUNCTION 
    function renderTable(data) {
        tableBody.innerHTML = ""; // Clear existing rows

        data.forEach(vehicle => {
            const row = document.createElement('tr');
            
            // Determine status pill class based on status text
            let statusClass = "status-idle";
            if (vehicle.status === "On Trip") statusClass = "status-ontrip";
            if (vehicle.status === "In Shop") statusClass = "status-inshop"; // 

            row.innerHTML = `
                <td><strong>${vehicle.id}</strong></td>
                <td>${vehicle.driver}</td>
                <td><span class="status-pill ${statusClass}">${vehicle.status}</span></td>
                <td>${vehicle.dest}</td>
                <td>${vehicle.eta}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    // 3. FILTER LOGIC 
    filterDropdown.addEventListener('change', (e) => {
        const selectedType = e.target.value.toLowerCase();
        
        if (selectedType === 'all') {
            renderTable(fleetData);
        } else {
            // Filter the data array based on the 'type' property
            const filteredData = fleetData.filter(vehicle => vehicle.type === selectedType);
            renderTable(filteredData);
        }
    });

    // 4. DYNAMIC KPI UPDATE 
    // Updates the "Active Fleet" number based on how many are "On Trip"
    function updateKPIs() {
        const activeCount = fleetData.filter(v => v.status === "On Trip").length;
        // Find the specific KPI card for Active Fleet and update it
        // Note: In a real app, you'd use specific IDs for these elements
        const kpiCards = document.querySelectorAll('.card .big-number');
        if(kpiCards[0]) kpiCards[0].textContent = activeCount; 
    }

    // Initial Load
    renderTable(fleetData);
    updateKPIs();
});