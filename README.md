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