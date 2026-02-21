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
