# Inventory Management System

A professional, full-featured Inventory Management & Billing System built with Django.

![Dashboard](https://via.placeholder.com/800x400.png?text=Dashboard+Preview)

## ✨ Key Features

### 📊 Analytics Dashboard
- **Visual Charts**: Real-time Bar & Doughnut charts for Stock Levels and Inventory Value.
- **KPI Cards**: Instant view of Total Products, Low Stock Alerts, and Revenue.
- **Role-Based Access**: Financial data hidden for non-admin staff.

### 🛒 Point of Sale (POS)
- **Multi-Item Billing**: Dynamic JavaScript-powered cart.
- **Real-Time Validation**: Prevents overselling stock.
- **Email Receipts**: Automatically emails customers their invoice upon checkout.

### 📦 Product Management
- **Search & Filter**: Find items instantly by Name or SKU.
- **Stock Tracking**: Automations marking items as "Low Stock" in UI.
- **Periodic Alerts**: Background task checks stock every 30 mins and emails Admin.

---

## 🚀 Getting Started

### Option 1: Quick Start (Local Development)
*Recommended for testing.*
```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Setup Database & User
python manage.py migrate
python manage.py createsuperuser

# 3. Run Server
python manage.py runserver
```
Visit: http://127.0.0.1:8000

### Option 2: Production (Docker)
*Recommended for deployment.*
```bash
# 1. Start Services (Nginx, Postgres, Redis)
.\deploy.ps1
```
Visit: http://localhost

---

## 🛠️ Tech Stack
- **Backend**: Django 5.x, Django REST Framework
- **Database**: PostgreSQL (Prod) / SQLite (Dev)
- **Async Tasks**: Celery + Redis
- **Frontend**: Bootstrap 5, Chart.js
- **Server**: Nginx + Gunicorn
