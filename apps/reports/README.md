# SautiWatch Reports API

The **SautiWatch Reports API** powers the *SautiWatch* platform — a secure system for reporting and managing cases of **gender-based violence (GBV)**.  
It supports encrypted data handling, report tracking, and role-based access for reporters and authorities.

---

## Overview

The Reports API allows:
- **Reporters** to submit confidential GBV reports.
- **Authorities** to view, assign, and resolve reports securely.

- **Secure Reporting**: End-to-end encryption for sensitive data
- **Anonymous Reporting**: Optional anonymity for victims
- **Report Tracking**: Unique tracking IDs for each report
- **Assignment System**: Reports can be assigned to specific authorities
- **Status Management**: Track report progress (pending, under review, resolved)
- **Search & Filtering**: Advanced querying capabilities

It uses **Django REST Framework (DRF)** and enforces strict authentication and permission rules to protect sensitive information.

---

## 🔐 Authentication & Permissions

| Type | Description |
|------|--------------|
| **Authentication** | Required for all endpoints |
| **Permission** | `reports.can_view_reports` for viewing and managing reports |
| **Reporter Access** | POST only (submit reports) |
| **Authority Access** | View, assign, and resolve reports |

---

## 🚀 API Endpoints

### 🗺️ Regions

#### `GET /regions/`
List all available regions.

**Permissions:** Authenticated users with `reports.can_view_reports`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Nairobi",
    "code": "NRB"
  }
]
```

---

### 📄 Reports

#### `GET /reports/`
List all reports with filtering and search options.

**Query Parameters:**
- `status` – pending / under_review / resolved  
- `urgency_level` – low / medium / high / critical  
- `region` – region ID  
- `search` – tracking ID, location, or description  

**Response Example:**
```json
[
  {
    "id": 1,
    "tracking_id": "SR-2024-000001-ABC12",
    "decrypted_victim_name": "Anonymous",
    "is_anonymous": true,
    "location": "Downtown",
    "region": 1,
    "region_name": "Nairobi",
    "incident_date": "2024-01-01T10:00:00Z",
    "decrypted_description": "Incident description",
    "image": "/media/reports/image.jpg",
    "status": "pending",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

---

#### `POST /reports/`
Create a new report.

**Permissions:** Authenticated users

**Request Body:**
```json
{
  "victim_name": "John Doe",
  "is_anonymous": false,
  "assaulter_name": "Jane Smith",
  "assaulter_description": "Description",
  "location": "Location details",
  "region": 1,
  "incident_date": "2024-01-01T10:00:00Z",
  "description": "Incident description",
  "image": "uploaded_file"
}
```

**Response:**  
Returns the created report with a generated `tracking_id`.

---

#### `GET /reports/{id}/`
Retrieve a single report.


### 👮 Report Management

#### `POST /reports/{report_id}/assign/`
Assigns the report to the current user and marks it **Under Review**.

**Response:**
```json
{
  "message": "Report SR-2024-000001-ABC12 assigned and marked Under Review."
}
```

---

#### `POST /reports/{report_id}/resolve/`
Marks the report as **Resolved**.

**Response:**
```json
{
  "message": "Report SR-2024-000001-ABC12 marked as Resolved."
}
```

---


## ⚙️ Developer Setup

### Prerequisites
- Python 3.10+
- Django 5+
- Django REST Framework
- Virtual environment

### Setup Steps
```bash
# Clone repository
git clone https://github.com/yourusername/sautiwatch-api.git
cd sautiwatch-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

---

