# 🛡️ SafeRoute API

SafeRoute API is a Django REST Framework backend service that helps users find **safe routes** and **critical emergency services** (hospitals, police stations, fire stations) based on their location.  
It uses **OpenStreetMap Nominatim API** to fetch geolocation data and integrates **Redis caching** to optimize repeated queries.  

This project is designed for **real-world applicability** and **scalability**, with clean architecture, clear API documentation, and deployment readiness.

---

## 📖 Real-World Problem & Solution

**Problem:**  
In emergencies, people often don’t know the safest and quickest path to the nearest hospital or police station.  
Existing apps focus on directions but don’t prioritize **safety-related services along the route**.

**Solution:**  
SafeRoute API bridges that gap by integrating real-time location lookups, mapping safety facilities, and storing frequently accessed results in cache for fast performance.  

---

## ✨ Features

- **Nearby Services Lookup** – Search for hospitals, police stations, fire stations by user’s coordinates.
- **Route Safety Analysis** – Get directions and see emergency service locations along the way.
- **User Profiles** – Save frequently used locations and preferred service types.
- **Caching with Redis** – Reduce API calls and improve speed.
- **Secure Authentication** – Token-based authentication with Django REST Framework.
- **Pagination & Filtering** – Efficient API data handling.
- **Scalable Architecture** – Separation of concerns with multiple apps.
- **API Documentation** – DRF browsable API & Postman Collection.

---
saferoute/
├── saferoute/           # Main project settings
├── users/               # Handles user authentication & profiles
├── services/            # External API integrations
├── routes/              # Core routing logic & feedback
└── manage.py

---

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework  
- **Database:** PostgreSQL (SQLite for local dev)  
- **Caching:** Redis  
- **External API:** [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/)  
- **Authentication:** DRF Token Auth  
- **Deployment:** Render / Railway  

---

## 📂 Models

### User
| Field        | Type    | Notes |
|--------------|---------|-------|
| username     | String  | Unique, required |
| email        | Email   | Unique, required |
| password     | String  | Hashed |
| saved_locations | JSON | List of saved coordinates |

### ServiceCategory
| Field  | Type  | Notes |
|--------|-------|-------|
| name   | String| Hospital, Police, Fire Station |

### ServiceLocation
| Field        | Type   | Notes |
|--------------|--------|-------|
| name         | String | Service name |
| latitude     | Float  | Required |
| longitude    | Float  | Required |
| category     | FK     | ServiceCategory |

---

## 🗺 ERD Diagram

*(Insert ERD image here once created with Lucidchart/Draw.io)*

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET    | `/api/services/` | List all service categories | ❌ |
| GET    | `/api/services/nearby/?lat=...&lon=...` | Get nearby safety services | ❌ |
| GET    | `/api/routes/safe/?from=...&to=...` | Get safe route with nearby services | ❌ |
| POST   | `/api/users/register/` | Create new user | ❌ |
| POST   | `/api/users/login/` | Get auth token | ❌ |
| GET    | `/api/users/profile/` | View user profile | ✅ |
| PUT    | `/api/users/profile/` | Update user profile | ✅ |

---

## 🧾 Example API Call

**Request:**
```bash
GET /api/services/nearby/?lat=-1.286389&lon=36.817223&category=hospital
```

**Response:**
```json
[
  {
    "name": "Kenyatta National Hospital",
    "latitude": -1.3000,
    "longitude": 36.8000,
    "category": "hospital",
    "distance_km": 2.5
  }
]
```

---

## 🚀 Caching Strategy

We use **Redis** to cache results of:
- Nearby services queries
- Frequent route lookups

**Implementation in DRF:**
- When a request is made for a location, check Redis cache first.
- If not found, fetch from API, store in Redis, and return.
- Cache expires after **1 hour**.

---

## 📅 Project Timeline

| Week | Phase                | Tasks |
|------|----------------------|-------|
| 1    | Idea & Planning       | Define project scope, choose API, design models |
| 2    | Design Phase          | Create ERD, API endpoint list, architecture plan |
| 3    | Start Building        | Set up Django project, configure DRF, implement user auth |
| 4    | Continue Building     | Implement service lookups, integrate caching, write tests |
| 5    | Finalize & Submit     | Optimize, write README, deploy, create demo video |

---

## ⚙ Installation

```bash
git clone https://github.com/yourusername/saferoute-api.git
cd saferoute-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Testing

```bash
python manage.py test
```

---

## 📄 License
MIT License

---

## 👤 Author
Your Name — [LinkedIn](https://www.linkedin.com/in/rich-mwendwa-b3296a302/) | [GitHub](https://github.com/RichBen03)
