
🧭 Safe & Confidential Reporting System
A privacy-focused platform that empowers victims to report incidents safely and anonymously, connect with verified support professionals, and promote community accountability through data-driven insights.

🏗️ Project Overview
This system allows users to submit incident reports confidentially, access immediate support contacts, and helps authorities track community-level reports responsibly.
 It combines a Django REST API backend, React.js frontend, SQLite database, and Twilio SMS integration for secure notifications.
Designs were created in Figma, and all API endpoints are exposed through REST for seamless integration.

🚀 Features
1. Safe & Confidential Reporting
    Anonymous or optional victim identification.
    Incident reporting with location, urgency, and description.
    Data encryption for sensitive fields.
    Automatic SMS notification to nearby authorities via Twilio.
    Quick Exit button for user safety.
    

2. Immediate Access to Help
    Verified list of therapists, counsellors, and health professionals.
    Filter contacts based on region or location.
    Direct “Call” or “Email” options from the interface.


3. Community Accountability - Not yet implemented
    Regional report aggregation and threshold alerts.
    Automated SMS/email notifications when cases exceed thresholds.
    Admin analytics dashboard showing:
    Reports per region
    Urgency distribution
    Monthly trends
    Public “Community Insights” page with anonymized data (optional).
    


🧩 Tech Stack
**Backend**
    Django (Python)
    Django REST Framework
    SQLite
    Twilio for SMS notifications


**Frontend**
    React.js
    Axios for API calls
    Styled with CSS / Figma-based design system

Other Tools
    Figma (for UI/UX design)
    Git & GitHub (for version control)
    Render or Koyeb (for deployment)



⚙️ Setup Instructions
1. Clone the repository
```git clone https://github.com/yourusername/sauti_watch.git```
```cd safe-reporting-system```

2. Set up the Backend (Django)
cd backend
```python -m venv venv```
```source venv/bin/activate ``` # On Windows use venv\Scripts\activate
```pip install -r requirements.txt```

3. Apply Migrations
```python manage.py migrate```

4. Run the Development Server
```python manage.py runserver```

Backend runs by default at: http://127.0.0.1:8000/

5. Set up Environment Variables
Create a .env file in the backend directory with:
  TWILIO_ACCOUNT_SID=your_twilio_account_sid
  TWILIO_AUTH_TOKEN=your_twilio_auth_token
  TWILIO_PHONE_NUMBER=your_twilio_phone_number
  CORS_ALLOWED_ORIGINS=http://localhost:3000
  ALLOWED_HOSTS=localhost
  DEBUG=True

7. Run the Frontend (React)
   ```cd frontend```
   ``` npm install```
   ``` npm start  ```

Frontend runs by default at: http://localhost:3000
**📡 API Endpoints**

  | Endpoint        | Method | Description                             |
  | --------------- | ------ | --------------------------------------- |
  | `/api/reports/` | POST   | Create a new report (anonymous allowed) |
  | `/api/reports/` | GET    | List all reports (admin only)           |
  | `/api/support/` | GET    | List all verified support contacts      |
  | `/api/support/` | POST   | Add a new support contact (admin only)  |



**🛡️ Security & Privacy**
    Sensitive data (like victim name) is encrypted using Fernet/Django cryptography.
    Anonymous reporting supported — no authentication required for report creation.
    Admin dashboard protected with role-based permissions.
    HTTPS enforced in production; CSP headers and secure cookies enabled.



**📊 Future Improvements**
    Implement AI-powered pattern detection for repeated locations/incidents.
    Add voice-based reporting for accessibility.
    Integration with Google Maps API for more accurate regional mapping.
    SMS fallback for areas with poor internet connectivity.



📁 Project Structure
safe-reporting-system/
│
├── backend/
│   ├── reports/
│   ├── support/
│   ├── dashboard/
│   ├── manage.py
│   └── db.sqlite3
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── figma-designs/
│   └── mockups/
│
└── README.md





