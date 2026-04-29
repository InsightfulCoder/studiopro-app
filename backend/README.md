# RouteX Backend API Documentation

The RouteX Backend is a Flask-powered microservice that coordinates smart waste collection using predictive analytics and multi-truck route optimization.

## Base URL
`http://127.0.0.1:8000`

---

## 📡 Endpoints

### 1. Get All Bins
**`GET /bins`**

Returns current status and location for all trash bins.

- **Request Body**: None
- **Success Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "lat": 20.9374,
      "lng": 77.7796,
      "fill": 65
    }
  ]
  ```

---

### 2. Update Sensor Data
**`POST /sensor-data`**

Receives real-time fill levels from IoT sensors.

- **Request Body**:
  ```json
  {
    "bin_id": 1,
    "fill_level": 85
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "bin_id": 1,
    "fill": 85
  }
  ```
- **Error Responses**:
    - **400 Bad Request**: Missing `bin_id` or `fill_level`.

---

### 3. Trigger Route Optimization
**`GET /optimize-route`**

Calculates optimized paths for available trucks based on **Priority Score**, **Predictions**, and **Thresholds**.

- **Request Body**: None
- **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "routes": {
      "1": [{"lat": 20.9374, "lng": 77.7796}, ...],
      "2": [{"lat": 20.9380, "lng": 77.7800}, ...]
    }
  }
  ```
- **Info Response (200 OK)**: Returned when no bins meet the collection criteria.
  ```json
  {
    "status": "info",
    "message": "No bins require collection.",
    "routes": {}
  }
  ```
- **Error Responses**:
    - **400 Bad Request**: No available trucks in the fleet.
    - **500 Internal Server Error**: Optimization engine failure.

---

### 4. Predictive Analytics
**`GET /analytics/fill-rates`**

Analyzes historical `FillLog` to estimate when bins will reach capacity.

- **Request Body**: None
- **Success Response (200 OK)**:
  ```json
  [
    {
      "bin_id": 1,
      "current_fill": 60,
      "predicted_full_in_hours": 12.5
    }
  ]
  ```
- *Note: `predicted_full_in_hours: -1` indicates insufficient data for prediction.*

---

### 5. Check Route Staleness
**`GET /check-route-update`**

Monitors the system for "Stale" routes caused by emergency overflows that aren't currently being serviced.

- **Request Body**: None
- **Success Response (200 OK)**:
  ```json
  {
    "is_stale": true
  }
  ```

---

## ⚠️ Error Codes

| Code | Type | Reason |
| :--- | :--- | :--- |
| **400** | Bad Request | Missing required payload fields or no trucks available. |
| **404** | Not Found | Requested bin ID does not exist in the database. |
| **500** | Server Error | Optimization algorithm or Database connection failure. |

---

## 🛠️ Performance Requirement
The `/optimize-route` endpoint is targetted to respond in **< 200ms** for 20 bins.
Current benchmarks show performance at **~50ms**.
