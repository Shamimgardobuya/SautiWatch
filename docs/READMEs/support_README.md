## 🛠️ Support Module — Django REST API

The **Support Module** provides a simple REST API that allows users to access verified support contacts such as therapists, counsellors, and health professionals.
It enables filtering by **region** and **category**, making it easy to find relevant support services across different areas.

---

### 🚀 Features

* ✅ List all **verified** support contacts
* 🔍 Filter support contacts by **region** or **category**
* ➕ Create new support contact entries (POST)
* 🌐 Fully RESTful API built with **Django REST Framework (DRF)**

---

### 📦 Model Structure

```python
class SupportContact(models.Model):
    CATEGORY_CHOICES = (
        ("Therapist", "Therapist"),
        ("Counsellor", "Counsellor"),
        ("Health", "Health"),
    )

    name = models.CharField(max_length=50)
    organization = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    region = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
```

---

### 🌍 API Base URL

**Production:**

```
https://sautiwatch.onrender.com/api/support/
```

---

### 🧭 Endpoints

| Method   | Endpoint                                       | Description                                           |
| -------- | ---------------------------------------------- | ----------------------------------------------------- |
| **GET**  | `/api/support/`                                | Retrieve all verified support contacts                |
| **GET**  | `/api/support/?region=Nairobi`                 | Filter contacts by region                             |
| **GET**  | `/api/support/?category=Therapist`             | Filter contacts by category                           |
| **GET**  | `/api/support/?region=Nairobi&category=Health` | Combine filters                                       |
| **POST** | `/api/support/`                                | Create a new support contact (requires valid payload) |

---

### 📩 Example GET Response

**Request:**

```bash
GET https://sautiwatch.onrender.com/api/support/?region=Nairobi
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Jane Doe",
    "organization": "Wellness Center",
    "category": "Therapist",
    "phone_number": "+254712345678",
    "email": "jane@example.com",
    "region": "Nairobi",
    "is_verified": true
  }
]
```

---

### 🧾 Example POST Request

**Endpoint:**

```
POST https://sautiwatch.onrender.com/api/support/
```

**Payload:**

```json
{
  "name": "John Smith",
  "organization": "Healing Minds",
  "category": "Counsellor",
  "phone_number": "+254700112233",
  "email": "johnsmith@example.com",
  "region": "Kisumu",
  "is_verified": false
}
```

**Response (201 Created):**

```json
{
  "id": 2,
  "name": "John Smith",
  "organization": "Healing Minds",
  "category": "Counsellor",
  "phone_number": "+254700112233",
  "email": "johnsmith@example.com",
  "region": "Kisumu",
  "is_verified": false
}
```

---

### ⚙️ Filtering Logic

The API supports flexible filtering via query parameters:

* `region` → case-insensitive partial match (`icontains`)
* `category` → exact match (must be one of: Therapist, Counsellor, Health)

Example:

```
GET /api/support/?region=Mombasa&category=Health
```

---

### 🧱 Serializer

```python
from rest_framework import serializers
from .models import SupportContact

class SupportContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportContact
        fields = ['id', 'name', 'organization', 'category', 'phone_number', 'email', 'region', 'is_verified']
```

---

### 🔑 URL Configuration

```python
# project/urls.py
urlpatterns = [
    path('api/support/', include('apps.support.urls')),
]
```

### 🧪 Testing (with cURL)

```bash
# List all verified contacts
curl -X GET https://sautiwatch.onrender.com/api/support/

# Create new contact
curl -X POST https://sautiwatch.onrender.com/api/support/ \
-H "Content-Type: application/json" \
-d '{
  "name": "Jane Doe",
  "organization": "Health Link",
  "category": "Health",
  "phone_number": "+254711223344",
  "email": "jane.doe@example.com",
  "region": "Nairobi",
  "is_verified": false
}'
```

---

### 🧩 Notes

* Only verified contacts (`is_verified=True`) are shown in GET requests.
* Unverified contacts can still be created (POST) but won’t appear until verified.
* Ensure CORS and permissions are configured if calling from a frontend app.

---
