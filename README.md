<<<<<<< HEAD
# 🚛 FleetFlow
### Rule-Based Fleet Lifecycle & Operational Intelligence System

FleetFlow is a centralized digital fleet management platform designed to replace inefficient manual logbooks with a structured, rule-based operational hub.

The system optimizes vehicle lifecycle management, enforces dispatch validation rules, monitors driver compliance, and tracks financial performance in real time.

---

# 🎯 Objective

To build a centralized management system that:

- Optimizes the lifecycle of delivery vehicles
- Prevents operational rule violations
- Monitors driver compliance
- Tracks fuel and maintenance expenses
- Provides data-driven fleet analytics

---

# 👥 User Roles (Authentication Design)

The system supports two primary login roles:

| Role | Access Scope |
|------|--------------|
| **Manager** | Full system access (vehicles, drivers, maintenance, analytics, financial metrics) |
| **Dispatcher** | Trip creation and operational assignment only |

> Safety monitoring and financial analysis features are accessible under the Manager role.

---

# 🏗 Folder Architecture 
fleet_flow/
│
├── backend/
│   ├── FastAPI
│   ├── SQLModel ORM
│   ├── PostgreSQL
│   └── Modular route structure
│
├── frontend/
│   ├── HTML
│   ├── CSS
│   └── JavaScript (Fetch API)

---

# ⚙️ Technology Stack

## Backend
- FastAPI
- SQLModel
- PostgreSQL
- Uvicorn

## Frontend
- HTML
- CSS
- JavaScript

---

# 🔄 Core System Modules

---

## 🚗 Vehicle Registry (Asset Management)

- Add / update / retire vehicles
- Track:
  - License plate (unique)
  - Capacity
  - Odometer
  - Status
- Lifecycle states:
    available → on_trip → available
    available → in_shop → available
    available → retired

Vehicles in maintenance are automatically removed from dispatch availability.

---

## 👨‍✈️ Driver Management & Compliance

- License expiry validation
- Suspension control
- Duty status toggle
- Trip completion tracking

The system blocks trip assignment if:

- License expired
- Driver suspended
- Driver not available

---

## 🚚 Trip Dispatcher & Validation Engine

Before creating a trip, the system validates:

- Vehicle exists
- Driver exists
- Vehicle is available
- Driver is available
- License is valid
- Cargo weight ≤ vehicle capacity

Trip lifecycle:
  draft → dispatched → completed → cancelled

Upon completion:
- Vehicle returns to available state
- Driver returns to available state
- Odometer updates
- Revenue is recorded

---

## 🔧 Maintenance & Service Logs

- Log maintenance events
- Automatically set vehicle status to `in_shop`
- Track maintenance cost
- Contribute to total operational expense

---

## ⛽ Fuel & Expense Tracking

- Record liters and fuel cost
- Link fuel logs to vehicle
- Compute total operational cost

---

# 📊 Analytics & Financial Intelligence

FleetFlow provides real-time KPIs:

- Active Fleet Count
- Vehicles in Maintenance
- Utilization Rate
- Pending Trips
- Fuel Efficiency (km/L)
- Total Operational Cost
- Vehicle ROI

---

## ROI Formula
  ROI = (Revenue - (Fuel + Maintenance)) / Acquisition Cost

---

# 🗃 Database Design

Relational data model linking:

- Vehicles
- Drivers
- Trips
- Maintenance Logs
- Fuel Logs

Foreign keys ensure data integrity across operational and financial data.

---






# 🚀 Local Setup Instructions
```
## 1️⃣ Clone Repository

git clone https://github.com/Keerthevasan007/fleet_flow.git
cd fleet_flow/backend

2️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate


3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup PostgreSQL

Create database:
CREATE DATABASE fleet_db;
Ensure user has schema privileges if required.

5️⃣ Run Backend Server
uvicorn main:app --reload

API Documentation available at:
http://127.0.0.1:8000/docs


Development Note :

For rapid development, automatic schema generation is used.

In production, schema migrations would be managed using Alembic for version control and safe database evolution.

```
=======
# 🚛 FleetFlow: Intelligent Logistics Command Center

> **Hackathon Project:** Optimizing fleet operations with role-based security and real-time analytics.

## 📖 Project Overview
FleetFlow is a comprehensive dashboard designed to streamline logistics management. It solves the chaos of manual fleet tracking by providing a unified interface for **Trip Dispatching**, **Vehicle Maintenance**, and **Driver Management**.

Unlike standard dashboards, FleetFlow features a **Secure Role-Based Access Control (RBAC)** system. The interface dynamically adapts based on who is logged in—giving Managers full control while restricting Dispatchers to operational tasks only.

---

## 🚀 Key Features

### 🔐 1. Smart Security Architecture
* **Role-Based Access Control (RBAC):**
    * **Manager View:** Access to Analytics, Financials, Registry, and Admin tools.
    * **Dispatcher View:** Restricted strictly to Trip Assignment and Command Center.
* **Session Management:** Uses `localStorage` to persist user sessions securely without a backend database.
* **Auto-Redirects:** Unauthorized users are automatically redirected to the login page.

### 📊 2. Interactive Modules
* **Command Center:** Real-time visualization of active, pending, and maintenance vehicles.
* **Trip Dispatcher:** A dedicated interface for assigning drivers to specific routes.
* **Vehicle Registry:** Digital logbook for fleet specifications and status.
* **Maintenance Tracker:** Predicts and logs service intervals to prevent breakdowns.

---

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3 (Modern Flexbox/Grid Layouts)
* **Logic:** Vanilla JavaScript (ES6+)
* **State Management:** Browser LocalStorage API
* **Icons:** FontAwesome 6

---

## 🧪 How to Test (Login Credentials)

To see the **Role-Based Logic** in action, please use the following credentials:

### 👨‍💼 1. The Manager (Full Access)
* **Email:** `admin@fleetflow.com`
* **Password:** `admin123`
* **Result:** You will see the full sidebar with Analytics, Fuel, and Registry options.

### 👷 2. The Dispatcher (Restricted Access)
* **Email:** `dispatch@fleetflow.com`
* **Password:** `user123`
* **Result:** * The sidebar will **hide** sensitive pages (Analytics, Maintenance).
    * The top-right profile will update to show **"Dispatcher"**.
    * Trying to access restricted pages manually will redirect you.

---

## 📸 Screenshots

*(You can drag and drop your screenshots here later!)*

---

## 💡 Future Improvements
* Integration with Google Maps API for real-time GPS tracking.
* Backend integration with Node.js/Express.
* AI-powered route optimization algorithms.

---

Made with ❤️ by [RAGNAROK]
>>>>>>> 3a8ad3849354a84e6a6d75d12f79f75c5d30962d
