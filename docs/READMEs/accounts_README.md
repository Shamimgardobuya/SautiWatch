# 📱 SMS Notification Feature — Safe & Confidential Reporting System

### ✨ Overview

This feature empowers victims of gender-based violence to **confidentially share their stories** with the **nearest relevant authority** for justice and closure.
Once a victim submits a report anonymously through the platform, the system automatically **decrypts** the report details and sends an **SMS alert** to the **nearest police station** using **Twilio**.

---

### 💡 How It Works

1. **Anonymous Report Submission**
   Victims submit incident details (including location) through a secure REST API.
   The description is **encrypted** before being stored in the database for privacy.

2. **Location-Based Matching**
   The system uses **Haversine formula** and **LocationIQ API** to calculate the nearest police station based on the report’s latitude and longitude.

3. **Authority Lookup**
   All police stations (Authorities) are preloaded with:

   * `latitude` and `longitude`
   * Publicly available `phone_number`
   * Optional `email` and `state`

4. **SMS Trigger via Django Signals**
   When a new report is created, a Django signal is triggered that:

   * Decrypts the incident description
   * Identifies the nearest authority
   * Sends the SMS alert using **Twilio** asynchronously via **Celery**

5. **Audit Logging**
   Every action — including SMS dispatch — is recorded in the **AuditLog** model for transparency and tracking.

---

### 🧩 Models Involved

#### **`Authority`**

Stores metadata for each police station or authority.

```python
class Authority(models.Model):
    name = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=70, null=True)
    email = models.EmailField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    state_phone_number = models.CharField(max_length=50, blank=True, null=True)
```

#### **`Report`**

Contains encrypted victim reports, location data, and urgency level.
Description is encrypted using **Fernet** (`cryptography.fernet`).

#### **`AuditLog`**

Tracks all system-level actions, including SMS notifications.

```python
class AuditLog(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)
```

---

### ⚙️ Core Logic

#### **1. Encryption / Decryption**

* Reports are encrypted using **Fernet** before being saved.
* Before sending SMS, the `description` field is **decrypted**:

  ```python
  from cryptography.fernet import Fernet
  f = Fernet(settings.ENCRYPTION_KEY)
  decrypted_text = f.decrypt(report.description.encode()).decode()
  ```

#### **2. Location Matching**

* All authorities have precomputed lat/lon.
* The nearest one is determined via the **Haversine formula**:

  ```python
  distance = haversine((report_lat, report_lon), (authority_lat, authority_lon))
  ```

#### **3. SMS Sending**

* SMS is sent using **Twilio’s Python SDK**:

  ```python
  from twilio.rest import Client
  client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
  client.messages.create(
      body=f"Urgent Incident Report:\n{decrypted_text}",
      from_=settings.TWILIO_PHONE_NUMBER,
      to=authority.phone_number
  )
  ```

#### **4. Asynchronous Execution**

* SMS dispatch runs in a **Celery task**, ensuring background processing without blocking the main request.

---

### 🔐 Authentication

* Users can sign up and log in through custom **REST endpoints**.
* Authentication compares credentials directly against Django’s `User` model (no JWT yet).
* Only authenticated users can access protected API routes (e.g., viewing reports, audit logs).

---

### 🌍 External Services Used

| Service                   | Purpose                                      |
| ------------------------- | -------------------------------------------- |
| **Twilio**                | Send SMS alerts                              |
| **LocationIQ API**        | Geocode and map reports to nearest authority |
| **Celery + Redis**        | Handle background task processing            |
| **Fernet (cryptography)** | Encrypt and decrypt sensitive report data    |

---

### ⚙️ Environment Variables

Add these to your `.env` or Django settings:

```bash
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1415xxxxxxx
LOCATIONIQ_API_KEY=your_locationiq_key
ENCRYPTION_KEY=your_fernet_key
```

---

### 🚀 Setup & Usage

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate

# 3. Run Celery worker
celery -A your_project_name worker -l info

# 4. Start Django server
python manage.py runserver
```

Submit a new report via API, and an SMS will automatically be sent to the nearest authority with public contact information.

---

### 🧾 Example SMS Output

```
🚨 GBV Alert 🚨
Incident near: Nairobi, Kenya
Urgency: High
Description: Assault reported at night near Ngong Road.

Please take immediate action.
```

---

### 📈 Future Improvements

* Add **JWT Authentication** for API security.
* Integrate **email alerts** alongside SMS.
* Add **fallback geocoding** when LocationIQ fails.
* Create a **dashboard** for audit log visualization.

---
