(() => {
    const API_BASE_URL = (window.API_BASE_URL || "").replace(/\/$/, "");

    function capitalize(word) {
        if (!word) return "";
        return word.charAt(0).toUpperCase() + word.slice(1);
    }

    async function apiFetch(path, options = {}) {
        const url = `${API_BASE_URL}${path}`;
        const response = await fetch(url, {
            credentials: "include",
            ...options,
        });

        const contentType = response.headers.get("content-type") || "";
        const isJson = contentType.includes("application/json");
        const payload = isJson ? await response.json().catch(() => null) : await response.text().catch(() => "");

        if (!response.ok) {
            const detail = payload?.detail || payload?.message || (typeof payload === "string" ? payload : "Request failed");
            const error = new Error(detail);
            error.status = response.status;
            error.payload = payload;
            throw error;
        }

        return payload;
    }

    function formEncode(data) {
        const body = new URLSearchParams();
        Object.entries(data).forEach(([key, value]) => {
            if (value === undefined || value === null) return;
            body.set(key, String(value));
        });
        return body;
    }

    function getPageName() {
        const path = window.location.pathname;
        const name = path.split("/").pop() || "";
        return name.toLowerCase();
    }

    function setRole(role) {
        if (!role) return;
        // Keep the old UI expectations (capitalized role in localStorage)
        localStorage.setItem("userRole", capitalize(role));
    }

    function applyRoleUi() {
        const role = localStorage.getItem("userRole");
        const userLabel = document.querySelector(".user-profile span");
        const userAvatar = document.querySelector(".user-profile .avatar");
        if (role) {
            if (userLabel) userLabel.textContent = role;
            if (userAvatar) userAvatar.textContent = role.charAt(0);
        }

        if (role === "Dispatcher") {
            const sidebarItems = document.querySelectorAll(".sidebar nav ul li");
            sidebarItems.forEach((item) => {
                const text = item.innerText.trim();
                const allowed = ["Command Center", "Trip Dispatcher", "Logout"];
                if (!allowed.includes(text)) item.style.display = "none";
            });
        }
    }

    const FleetApi = {
        login: (email, password) =>
            apiFetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formEncode({ email, password }),
            }),
        register: (email, password, role) =>
            apiFetch("/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formEncode({ email, password, role }),
            }),
        logout: () => apiFetch("/auth/logout", { method: "POST" }),
        me: () => apiFetch("/auth/me"),

        getVehicles: () => apiFetch("/vehicles"),
        getAvailableVehicles: () => apiFetch("/vehicles/available"),
        createVehicle: (vehicle) =>
            apiFetch("/vehicles/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(vehicle),
            }),
        retireVehicle: (vehicleId) => apiFetch(`/vehicles/${vehicleId}/retire`, { method: "PATCH" }),

        getDrivers: () => apiFetch("/drivers"),
        getAvailableDrivers: () => apiFetch("/drivers/available"),
        createDriver: (driver) =>
            apiFetch("/drivers/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(driver),
            }),
        suspendDriver: (driverId) => apiFetch(`/drivers/${driverId}/suspend`, { method: "PATCH" }),
        setDriverStatus: (driverId, status) => apiFetch(`/drivers/${driverId}/status?status=${encodeURIComponent(status)}`, { method: "PATCH" }),

        getTrips: () => apiFetch("/trips"),
        createTrip: (trip) =>
            apiFetch("/trips/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(trip),
            }),

        getMaintenance: () => apiFetch("/maintenance"),
        addMaintenance: (log) =>
            apiFetch("/maintenance/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(log),
            }),

        getFuelLogs: () => apiFetch("/fuel"),
        addFuelLog: (log) =>
            apiFetch("/fuel/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(log),
            }),

        getDashboard: () => apiFetch("/analytics/dashboard"),
        getVehicleRoi: (vehicleId) => apiFetch(`/analytics/vehicle/${vehicleId}/roi`),
    };

    window.FleetApi = FleetApi;

    async function requireSession() {
        const page = getPageName();
        if (page === "login.html" || page === "") return;
        try {
            const me = await FleetApi.me();
            setRole(me.role);
        } catch (err) {
            if (err?.status === 401) {
                localStorage.clear();
                window.location.href = "login.html";
                return;
            }
        }
    }

    function inferVehicleTypeFromPlate(plate) {
        const prefix = (plate || "").split("-")[0].toLowerCase();
        if (prefix.includes("trk") || prefix.includes("truck")) return "truck";
        if (prefix.includes("van")) return "van";
        if (prefix.includes("bike")) return "bike";
        return "unknown";
    }

    function statusToPill(status) {
        if (status === "on_trip" || status === "dispatched") return { text: "On Trip", className: "status-ontrip" };
        if (status === "in_shop") return { text: "In Shop", className: "status-inshop" };
        if (status === "available") return { text: "Idle", className: "status-idle" };
        if (status === "retired") return { text: "Retired", className: "status-inshop" };
        if (status === "completed") return { text: "Completed", className: "status-idle" };
        if (status === "cancelled") return { text: "Cancelled", className: "status-inshop" };
        return { text: status || "-", className: "status-idle" };
    }

    async function initLoginPage() {
        const form = document.getElementById("login-form");
        if (!form) return;

        const errorMsg = document.getElementById("error-msg");
        localStorage.clear();
        try {
            await FleetApi.logout();
        } catch {
            // ignore
        }

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            if (errorMsg) errorMsg.style.display = "none";

            const email = document.getElementById("email")?.value?.trim();
            const password = document.getElementById("password")?.value?.trim();

            try {
                const res = await FleetApi.login(email, password);
                setRole(res.role);
                applyRoleUi();
                window.location.href = res.role === "dispatcher" ? "dispatcher.html" : "index.html";
            } catch (err) {
                if (errorMsg) {
                    errorMsg.style.display = "block";
                    errorMsg.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> ${err.message}`;
                }
                const card = document.querySelector(".login-card");
                if (card) {
                    card.style.transform = "translateX(10px)";
                    setTimeout(() => (card.style.transform = "translateX(0)"), 100);
                }
            }
        });
    }

    async function initIndexPage() {
        const tableBody = document.getElementById("fleet-table-body");
        const filterDropdown = document.querySelector(".filter-dropdown");
        if (!tableBody) return;

        const [dashboard, vehicles, trips, drivers] = await Promise.all([
            FleetApi.getDashboard().catch(() => null),
            FleetApi.getVehicles().catch(() => []),
            FleetApi.getTrips().catch(() => []),
            FleetApi.getDrivers().catch(() => []),
        ]);

        const driverById = new Map(drivers.map((d) => [d.id, d]));

        // Update KPIs (order matches the existing HTML cards)
        const kpiCards = document.querySelectorAll(".card .big-number");
        if (dashboard && kpiCards.length >= 4) {
            kpiCards[0].textContent = String(dashboard.active_vehicles ?? "-");
            kpiCards[1].textContent = String(dashboard.in_shop ?? "-");
            kpiCards[2].textContent = `${Math.round((dashboard.utilization_rate || 0) * 100)}%`;
            kpiCards[3].textContent = String(dashboard.pending_trips ?? "-");
        }

        function renderRows(rows) {
            tableBody.innerHTML = "";
            rows.forEach((row) => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${row.plate}</strong></td>
                    <td>${row.driver}</td>
                    <td><span class="status-pill ${row.statusClass}">${row.statusText}</span></td>
                    <td>${row.destination}</td>
                    <td>${row.eta}</td>
                `;
                tableBody.appendChild(tr);
            });
        }

        const latestDispatchedTripByVehicle = new Map();
        trips
            .filter((t) => t.status === "dispatched")
            .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
            .forEach((t) => {
                if (!latestDispatchedTripByVehicle.has(t.vehicle_id)) latestDispatchedTripByVehicle.set(t.vehicle_id, t);
            });

        const rows = vehicles.map((v) => {
            const trip = latestDispatchedTripByVehicle.get(v.id);
            const driver = trip ? driverById.get(trip.driver_id) : null;
            const pill = statusToPill(v.status);
            return {
                type: (v.vehicle_type || inferVehicleTypeFromPlate(v.license_plate)).toLowerCase(),
                plate: v.license_plate,
                driver: driver?.name || "Unassigned",
                statusText: pill.text,
                statusClass: pill.className,
                destination: trip?.destination || "Depot",
                eta: "-",
            };
        });

        renderRows(rows);

        if (filterDropdown) {
            filterDropdown.addEventListener("change", (e) => {
                const selectedType = String(e.target.value || "all").toLowerCase();
                renderRows(selectedType === "all" ? rows : rows.filter((r) => r.type === selectedType));
            });
        }
    }

    async function initRegistryPage() {
        const form = document.getElementById("vehicle-form");
        const tableBody = document.getElementById("registry-data");
        if (!form || !tableBody) return;

        async function refresh() {
            const vehicles = await FleetApi.getVehicles();
            tableBody.innerHTML = "";
            vehicles.forEach((v) => {
                const tr = document.createElement("tr");
                const pill = statusToPill(v.status);
                const canRetire = v.status !== "retired";
                tr.innerHTML = `
                    <td><strong>${v.license_plate}</strong></td>
                    <td>${v.model}</td>
                    <td>${v.max_capacity} kg</td>
                    <td>${v.odometer} km</td>
                    <td><span class="status-pill ${pill.className}">${pill.text}</span></td>
                    <td>
                        ${canRetire ? `<button data-retire="${v.id}" style="padding: 5px 10px; cursor: pointer; background: #eee; border: 1px solid #ccc; border-radius: 3px;">Retire</button>` : "-"}
                    </td>
                `;
                tableBody.appendChild(tr);
            });

            tableBody.querySelectorAll("button[data-retire]").forEach((btn) => {
                btn.addEventListener("click", async () => {
                    const vehicleId = btn.getAttribute("data-retire");
                    await FleetApi.retireVehicle(vehicleId);
                    await refresh();
                });
            });
        }

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const model = document.getElementById("v-model")?.value?.trim();
            const plate = document.getElementById("v-plate")?.value?.trim()?.toUpperCase();
            const maxCap = Number(document.getElementById("v-cap")?.value);

            const vehicle = {
                name: model,
                model,
                license_plate: plate,
                max_capacity: maxCap,
                acquisition_cost: 0,
                vehicle_type: inferVehicleTypeFromPlate(plate),
                region: "default",
            };

            await FleetApi.createVehicle(vehicle);
            form.reset();
            await refresh();
        });

        await refresh();
    }

    async function initDriversPage() {
        const form = document.getElementById("driver-form");
        const tableBody = document.getElementById("drivers-data");
        if (!form || !tableBody) return;

        function formatDate(value) {
            if (!value) return "-";
            return String(value).slice(0, 10);
        }

        async function refresh() {
            const drivers = await FleetApi.getDrivers();
            tableBody.innerHTML = "";
            const today = new Date();

            drivers.forEach((d) => {
                const expiryDate = d.license_expiry ? new Date(d.license_expiry) : null;
                const isExpired = expiryDate ? expiryDate < today : false;
                const isSuspended = d.status === "suspended";
                const statusClass = isExpired || isSuspended ? "status-inshop" : "status-ontrip";
                const statusText = isExpired || isSuspended ? "Expired / Suspended" : "Valid";
                const actionLabel = isSuspended ? "Re-activate" : "Suspend";
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${d.name}</strong></td>
                    <td>${d.license_number}</td>
                    <td style="${isExpired ? 'color: var(--danger); font-weight:bold;' : ''}">${formatDate(d.license_expiry)}</td>
                    <td><span class="status-pill ${statusClass}">${statusText}</span></td>
                    <td>
                        <button data-toggle="${d.id}" data-status="${d.status}" style="padding: 5px 10px; cursor: pointer; background: #eee; border: 1px solid #ccc; border-radius: 3px;">${actionLabel}</button>
                    </td>
                `;
                tableBody.appendChild(tr);
            });

            tableBody.querySelectorAll("button[data-toggle]").forEach((btn) => {
                btn.addEventListener("click", async () => {
                    const driverId = btn.getAttribute("data-toggle");
                    const status = btn.getAttribute("data-status");
                    if (status === "suspended") {
                        await FleetApi.setDriverStatus(driverId, "available");
                    } else {
                        await FleetApi.suspendDriver(driverId);
                    }
                    await refresh();
                });
            });
        }

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("d-name")?.value?.trim();
            const license_number = document.getElementById("d-license")?.value?.trim();
            const license_expiry = document.getElementById("d-expiry")?.value;

            await FleetApi.createDriver({
                name,
                license_number,
                license_category: "LMV",
                license_expiry,
            });

            form.reset();
            await refresh();
        });

        await refresh();
    }

    async function initDispatcherPage() {
        const form = document.getElementById("dispatch-form");
        const vehicleSelect = document.getElementById("trip-vehicle");
        const driverSelect = document.getElementById("trip-driver");
        const tableBody = document.getElementById("trip-data");
        if (!form || !vehicleSelect || !driverSelect || !tableBody) return;

        const errorMsg = document.getElementById("error-msg");
        const [vehicles, drivers] = await Promise.all([FleetApi.getAvailableVehicles(), FleetApi.getAvailableDrivers()]);
        const vehicleById = new Map(vehicles.map((v) => [String(v.id), v]));
        const driverById = new Map(drivers.map((d) => [String(d.id), d]));

        vehicleSelect.innerHTML = '<option value="">-- Choose Available --</option>';
        vehicles.forEach((v) => {
            const opt = document.createElement("option");
            opt.value = String(v.id);
            opt.textContent = `${v.license_plate} - ${v.model} (Max: ${v.max_capacity}kg)`;
            vehicleSelect.appendChild(opt);
        });

        driverSelect.innerHTML = '<option value="">-- Choose Driver --</option>';
        drivers.forEach((d) => {
            const opt = document.createElement("option");
            opt.value = String(d.id);
            opt.textContent = `${d.name} (Lic exp: ${String(d.license_expiry).slice(0, 10)})`;
            driverSelect.appendChild(opt);
        });

        async function refreshTrips() {
            const trips = await FleetApi.getTrips();
            const allVehicles = await FleetApi.getVehicles().catch(() => vehicles);
            const allDrivers = await FleetApi.getDrivers().catch(() => drivers);

            const vById = new Map(allVehicles.map((v) => [v.id, v]));
            const dById = new Map(allDrivers.map((d) => [d.id, d]));

            tableBody.innerHTML = "";
            trips
                .filter((t) => t.status === "dispatched")
                .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
                .forEach((t) => {
                    const v = vById.get(t.vehicle_id);
                    const d = dById.get(t.driver_id);
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td><strong>${t.id}</strong></td>
                        <td>${v?.license_plate || t.vehicle_id}</td>
                        <td>${d?.name || t.driver_id}</td>
                        <td>${t.cargo_weight} kg</td>
                        <td>${t.destination}</td>
                        <td><span class="status-pill status-ontrip">Dispatched</span></td>
                    `;
                    tableBody.appendChild(tr);
                });
        }

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            if (errorMsg) errorMsg.style.display = "none";

            const vehicleId = vehicleSelect.value;
            const driverId = driverSelect.value;
            const weight = Number(document.getElementById("trip-weight")?.value);
            const destination = document.getElementById("trip-dest")?.value?.trim();
            const vehicle = vehicleById.get(vehicleId);
            const driver = driverById.get(driverId);
            if (!vehicle || !driver) return;

            try {
                await FleetApi.createTrip({
                    vehicle_id: Number(vehicleId),
                    driver_id: Number(driverId),
                    cargo_weight: weight,
                    origin: "Warehouse",
                    destination,
                    start_odometer: vehicle.odometer || 0,
                });
                form.reset();
                await refreshTrips();
            } catch (err) {
                if (errorMsg) {
                    errorMsg.style.display = "block";
                    errorMsg.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> <strong>Error:</strong> ${err.message}`;
                }
            }
        });

        await refreshTrips();
    }

    async function initMaintenancePage() {
        const form = document.getElementById("maint-form");
        const vehicleSelect = document.getElementById("maint-vehicle");
        const tableBody = document.getElementById("maintenance-data");
        if (!form || !vehicleSelect || !tableBody) return;

        const vehicles = await FleetApi.getVehicles();
        const vehicleById = new Map(vehicles.map((v) => [String(v.id), v]));

        vehicleSelect.innerHTML = "";
        vehicles.forEach((v) => {
            const opt = document.createElement("option");
            opt.value = String(v.id);
            opt.textContent = `${v.license_plate} (${v.model})`;
            vehicleSelect.appendChild(opt);
        });

        async function refresh() {
            const logs = await FleetApi.getMaintenance();
            const total = logs.reduce((sum, l) => sum + (Number(l.cost) || 0), 0);
            const urgent = logs.filter((l) => {
                const desc = String(l.description || "").toLowerCase();
                return desc.includes("engine") || desc.includes("body");
            }).length;

            const urgentEl = document.getElementById("urgent-count");
            const totalEl = document.getElementById("total-spend");
            if (urgentEl) urgentEl.textContent = String(urgent);
            if (totalEl) totalEl.textContent = "$" + total.toLocaleString();

            tableBody.innerHTML = "";
            logs
                .sort((a, b) => new Date(b.service_date).getTime() - new Date(a.service_date).getTime())
                .forEach((l) => {
                    const v = vehicleById.get(String(l.vehicle_id));
                    const date = l.service_date ? new Date(l.service_date).toLocaleDateString() : "-";
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td>${date}</td>
                        <td><strong>${v?.license_plate || l.vehicle_id}</strong></td>
                        <td>${l.description}</td>
                        <td>$${Number(l.cost).toFixed(2)}</td>
                        <td><span class="status-pill status-inshop">In Shop</span></td>
                    `;
                    tableBody.appendChild(tr);
                });
        }

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const vehicleId = vehicleSelect.value;
            const description = document.getElementById("maint-type")?.value;
            const cost = Number(document.getElementById("maint-cost")?.value);
            await FleetApi.addMaintenance({ vehicle_id: Number(vehicleId), description, cost });
            form.reset();
            await refresh();

            const notifyBox = document.getElementById("status-notify");
            const notifyText = document.getElementById("notify-text");
            const v = vehicleById.get(vehicleId);
            if (notifyBox && notifyText) {
                notifyBox.style.display = "block";
                notifyText.innerHTML = `<strong>${v?.license_plate || vehicleId}</strong> status changed to <span class="status-pill status-inshop">In Shop</span>. Removed from Dispatcher.`;
                setTimeout(() => {
                    notifyBox.style.display = "none";
                }, 4000);
            }
        });

        await refresh();
    }

    async function initFuelPage() {
        const form = document.getElementById("fuel-form");
        const vehicleSelect = document.getElementById("fuel-vehicle");
        const tableBody = document.getElementById("fuel-table-body");
        if (!form || !vehicleSelect || !tableBody) return;

        const vehicles = await FleetApi.getVehicles();
        const vehicleById = new Map(vehicles.map((v) => [String(v.id), v]));

        vehicleSelect.innerHTML = "";
        vehicles.forEach((v) => {
            const opt = document.createElement("option");
            opt.value = String(v.id);
            opt.textContent = v.license_plate;
            vehicleSelect.appendChild(opt);
        });

        async function refresh() {
            const logs = await FleetApi.getFuelLogs();
            const total = logs.reduce((sum, l) => sum + (Number(l.total_cost) || 0), 0);
            const totalDisplay = document.getElementById("total-fuel-cost");
            if (totalDisplay) totalDisplay.textContent = "$" + total.toLocaleString();

            tableBody.innerHTML = "";
            logs
                .sort((a, b) => (b.id || 0) - (a.id || 0))
                .forEach((l) => {
                    const date = new Date().toLocaleDateString();
                    const v = vehicleById.get(String(l.vehicle_id));
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td>${date}</td>
                        <td><strong>${v?.license_plate || l.vehicle_id}</strong></td>
                        <td>${l.liters} L</td>
                        <td>$${l.total_cost}</td>
                        <td>-</td>
                    `;
                    tableBody.appendChild(tr);
                });
        }

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const vehicleId = vehicleSelect.value;
            const liters = Number(document.getElementById("fuel-liters")?.value);
            const cost = Number(document.getElementById("fuel-cost")?.value);
            await FleetApi.addFuelLog({ vehicle_id: Number(vehicleId), liters, cost });
            form.reset();
            await refresh();
        });

        await refresh();
    }

    async function initAnalyticsPage() {
        const financeCanvas = document.getElementById("financeChart");
        const statusCanvas = document.getElementById("statusChart");
        if (!financeCanvas || !statusCanvas || typeof Chart === "undefined") return;

        const loader = document.getElementById("loading-spinner");
        const content = document.getElementById("analytics-content");
        if (loader) loader.style.display = "block";
        if (content) content.style.display = "none";

        const vehicles = await FleetApi.getVehicles();
        const counts = {
            on_trip: vehicles.filter((v) => v.status === "on_trip").length,
            in_shop: vehicles.filter((v) => v.status === "in_shop").length,
            available: vehicles.filter((v) => v.status === "available").length,
        };

        const rois = await Promise.all(
            vehicles.map((v) => FleetApi.getVehicleRoi(v.id).catch(() => ({ vehicle_id: v.id, total_revenue: 0, total_cost: 0, roi: 0 })))
        );

        if (loader) loader.style.display = "none";
        if (content) content.style.display = "block";

        const labels = vehicles.map((v) => v.license_plate);
        const revenue = rois.map((r) => Number(r.total_revenue) || 0);
        const costs = rois.map((r) => Number(r.total_cost) || 0);

        new Chart(financeCanvas.getContext("2d"), {
            type: "bar",
            data: {
                labels,
                datasets: [
                    { label: "Revenue", data: revenue, backgroundColor: "#27ae60" },
                    { label: "Costs", data: costs, backgroundColor: "#e74c3c" },
                ],
            },
        });

        new Chart(statusCanvas.getContext("2d"), {
            type: "doughnut",
            data: {
                labels: ["Active", "In Shop", "Idle"],
                datasets: [
                    {
                        data: [counts.on_trip, counts.in_shop, counts.available],
                        backgroundColor: ["#27ae60", "#ff6b00", "#95a5a6"],
                    },
                ],
            },
        });
    }

    document.addEventListener("DOMContentLoaded", async () => {
        await requireSession();
        applyRoleUi();

        await initLoginPage();
        await initIndexPage();
        await initRegistryPage();
        await initDriversPage();
        await initDispatcherPage();
        await initMaintenancePage();
        await initFuelPage();
        await initAnalyticsPage();
    });
})();