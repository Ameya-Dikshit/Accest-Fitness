# ACEest Fitness & Gym - Complete API Reference

## 📡 API Overview

This document provides complete technical documentation for all API endpoints, request/response formats, and integration examples.

**Base URL:** `http://localhost:5000` (Development) or `https://api.aceest-fitness.com` (Production)

**API Version:** 1.0.0  
**Last Updated:** March 2024

---

## Table of Contents

1. [API Standards](#-api-standards)
2. [Authentication](#-authentication)
3. [Health & System](#-health--system-endpoints)
4. [Programs](#-programs-endpoints)
5. [Clients](#-clients-endpoints)
6. [Progress Tracking](#-progress-tracking-endpoints)
7. [Workouts](#-workouts-endpoints)
8. [Metrics](#-metrics-endpoints)
9. [Error Handling](#-error-handling)
10. [Integration Examples](#-integration-examples)

---

## 🏗️ API Standards

### Request Format

All requests must include proper headers:

```http
Content-Type: application/json
Accept: application/json
```

### Response Format

All responses follow this standardized format:

```json
{
  "status": "success|error",
  "message": "Descriptive message",
  "data": {},
  "count": 0,
  "timestamp": "2024-03-16T10:30:00"
}
```

### HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|-----------|
| GET | Retrieve resource | ✓ Yes |
| POST | Create resource | ✗ No |
| PUT | Update resource | ✓ Yes |
| DELETE | Remove resource | ✓ Yes |

### Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input, missing fields |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource (duplicate name) |
| 500 | Server Error | Unexpected server error |

---

## 🔐 Authentication

**Current Status:** No authentication required (Basic implementation)

**Future Enhancement:** JWT Token-based authentication

```http
Authorization: Bearer <token>
```

---

## 🏥 Health & System Endpoints

### 1. Health Check

Check if the API is running and healthy.

```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "ACEest Fitness API",
  "timestamp": "2024-03-16T10:30:00"
}
```

**Use Case:** Load balancer health checks, monitoring services

**Example:**
```bash
curl -X GET http://localhost:5000/health
```

---

### 2. Initialize Database

Initialize database tables and schema.

```http
POST /initialize
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Database initialized successfully"
}
```

**Response (500 Error):**
```json
{
  "status": "error",
  "message": "Error details"
}
```

**Use Case:** First-time setup, database reset

**Example:**
```bash
curl -X POST http://localhost:5000/initialize
```

---

## 🎯 Programs Endpoints

### 3. Get All Programs

Retrieve all available fitness programs.

```http
GET /programs
```

**Query Parameters:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "Fat Loss (FL)": {
      "factor": 22,
      "description": "High-intensity cardio with calorie deficit",
      "workout": "Mon: Back Squat 5x5 + Core, Tue: EMOM 20min Assault Bike, ..."
    },
    "Muscle Gain (MG)": {
      "factor": 35,
      "description": "Progressive strength training with surplus",
      "workout": "Mon: Squat 5x5, Tue: Bench 5x5, ..."
    },
    "Beginner (BG)": {
      "factor": 26,
      "description": "Full-body circuit focused on form mastery",
      "workout": "Full Body Circuit: Air Squats, Ring Rows, Push-ups, ..."
    }
  }
}
```

**Program Details:**

| Program | Factor | Calorie Calculation | Best For |
|---------|--------|-------------------|----------|
| Fat Loss (FL) | 22 | weight × 22 | Cutting/Fat loss |
| Muscle Gain (MG) | 35 | weight × 35 | Bulking/Hypertrophy |
| Beginner (BG) | 26 | weight × 26 | Beginners/Foundation |

**Example:**
```bash
curl -X GET http://localhost:5000/programs \
  -H "Content-Type: application/json"
```

---

## 👥 Clients Endpoints

### 4. List All Clients

Get all registered fitness clients.

```http
GET /clients
```

**Query Parameters:** None (Pagination available in future versions)

**Response (200 OK):**
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 30,
      "weight": 80.5,
      "program": "Fat Loss (FL)",
      "calories": 1771,
      "created_at": "2024-03-10T10:00:00"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "age": 28,
      "weight": 65.0,
      "program": "Muscle Gain (MG)",
      "calories": 2275,
      "created_at": "2024-03-12T14:30:00"
    }
  ]
}
```

**Use Case:** Dashboard overview, client listings

**Example:**
```bash
curl -X GET http://localhost:5000/clients
```

---

### 5. Create Client

Register a new fitness client.

```http
POST /clients
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe",
  "age": 30,
  "weight": 80.5,
  "program": "Fat Loss (FL)"
}
```

**Request Fields:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| name | string | Yes | Unique, max 100 chars |
| age | integer | Yes | 13-120 |
| weight | float | Yes | 30-300 kg |
| program | string | Yes | One of: "Fat Loss (FL)", "Muscle Gain (MG)", "Beginner (BG)" |

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Client 'John Doe' created successfully",
  "data": {
    "name": "John Doe",
    "age": 30,
    "weight": 80.5,
    "program": "Fat Loss (FL)",
    "calories": 1771
  }
}
```

**Response (400 Bad Request) - Missing Fields:**
```json
{
  "status": "error",
  "message": "Missing required fields: ['name', 'age', 'weight', 'program']"
}
```

**Response (400 Bad Request) - Invalid Program:**
```json
{
  "status": "error",
  "message": "Program must be one of: ['Fat Loss (FL)', 'Muscle Gain (MG)', 'Beginner (BG)']"
}
```

**Response (409 Conflict) - Duplicate Client:**
```json
{
  "status": "error",
  "message": "Client with this name already exists"
}
```

**Calculation Logic:**
```
Daily Calories = Weight (kg) × Program Factor

Example:
Weight: 80.5 kg
Program: Fat Loss (FL) with factor 22
Daily Calories: 80.5 × 22 = 1,771 kcal
```

**Example:**
```bash
curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 30,
    "weight": 80.5,
    "program": "Fat Loss (FL)"
  }'
```

---

### 6. Get Client Details

Retrieve specific client information.

```http
GET /clients/{name}
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "weight": 80.5,
    "program": "Fat Loss (FL)",
    "calories": 1771,
    "created_at": "2024-03-10T10:00:00"
  }
}
```

**Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Client 'John Doe' not found"
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/clients/John%20Doe
```

---

### 7. Update Client

Update client information (age, weight, or program).

```http
PUT /clients/{name}
Content-Type: application/json
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Request Body (Any combination of fields):**
```json
{
  "age": 31,
  "weight": 79.5,
  "program": "Muscle Gain (MG)"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Client 'John Doe' updated successfully"
}
```

**Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Client 'John Doe' not found"
}
```

**Response (400 Bad Request) - No Fields to Update:**
```json
{
  "status": "error",
  "message": "No valid fields to update"
}
```

**Important Notes:**
- Calories are automatically recalculated if weight or program changes
- Name cannot be updated (primary identifier)
- At least one field must be provided

**Example:**
```bash
curl -X PUT http://localhost:5000/clients/John%20Doe \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31,
    "weight": 79.5
  }'
```

---

### 8. Delete Client

Remove a client from the system.

```http
DELETE /clients/{name}
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Client 'John Doe' deleted successfully"
}
```

**Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Client 'John Doe' not found"
}
```

**Cascading Deletes:**
- Client progress records deleted
- Workout logs deleted
- Metrics records deleted

**Example:**
```bash
curl -X DELETE http://localhost:5000/clients/John%20Doe
```

---

## 📊 Progress Tracking Endpoints

### 9. Get Client Progress History

Retrieve weekly adherence history for a client.

```http
GET /clients/{name}/progress
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Response (200 OK):**
```json
{
  "status": "success",
  "count": 4,
  "data": [
    {
      "id": 1,
      "client_name": "John Doe",
      "week": "Week 10 - 2024",
      "adherence": 85,
      "created_at": "2024-03-09T10:00:00"
    },
    {
      "id": 2,
      "client_name": "John Doe",
      "week": "Week 11 - 2024",
      "adherence": 90,
      "created_at": "2024-03-16T10:00:00"
    }
  ]
}
```

**Response (200 OK) - No Data:**
```json
{
  "status": "success",
  "count": 0,
  "data": []
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/clients/John%20Doe/progress
```

---

### 10. Record Weekly Progress

Log weekly adherence for a client.

```http
POST /clients/{name}/progress
Content-Type: application/json
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Request Body:**
```json
{
  "adherence": 85
}
```

**Request Fields:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| adherence | integer | Yes | 0-100 (percentage) |

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Progress recorded for John Doe",
  "data": {
    "client_name": "John Doe",
    "week": "Week 11 - 2024",
    "adherence": 85
  }
}
```

**Response (400 Bad Request) - Invalid Adherence:**
```json
{
  "status": "error",
  "message": "Adherence must be between 0 and 100"
}
```

**Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Client 'John Doe' not found"
}
```

**Adherence Interpretation:**
```
0-20%:   Very low adherence (needs intervention)
21-40%:  Low adherence (off track)
41-60%:  Moderate adherence (inconsistent)
61-80%:  Good adherence (on track)
81-100%: Excellent adherence (exceeding)
```

**Example:**
```bash
curl -X POST http://localhost:5000/clients/John%20Doe/progress \
  -H "Content-Type: application/json" \
  -d '{
    "adherence": 85
  }'
```

---

## 🏋️ Workouts Endpoints

### 11. Get Client Workouts

Retrieve workout history for a client.

```http
GET /clients/{name}/workouts
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Response (200 OK):**
```json
{
  "status": "success",
  "count": 3,
  "data": [
    {
      "id": 1,
      "client_name": "John Doe",
      "date": "2024-03-16",
      "workout_type": "Back Squat 5x5 + Core",
      "duration_min": 60,
      "notes": "Great session, felt strong"
    },
    {
      "id": 2,
      "client_name": "John Doe",
      "date": "2024-03-15",
      "workout_type": "EMOM 20min Assault Bike",
      "duration_min": 25,
      "notes": null
    }
  ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/clients/John%20Doe/workouts
```

---

### 12. Log Workout

Record a workout session for a client.

```http
POST /clients/{name}/workouts
Content-Type: application/json
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Request Body:**
```json
{
  "workout_type": "Back Squat 5x5 + Core",
  "date": "2024-03-16",
  "duration_min": 60,
  "notes": "Great session, felt strong"
}
```

**Request Fields:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| workout_type | string | Yes | Exercise/program name |
| date | string | Yes | YYYY-MM-DD format |
| duration_min | integer | No | 1-600 minutes |
| notes | string | No | Additional comments |

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Workout logged successfully",
  "data": {
    "client_name": "John Doe",
    "workout_type": "Back Squat 5x5 + Core",
    "date": "2024-03-16"
  }
}
```

**Response (400 Bad Request) - Missing Required Fields:**
```json
{
  "status": "error",
  "message": "Missing required fields: ['workout_type', 'date']"
}
```

**Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Client 'John Doe' not found"
}
```

**Workout Type Examples:**
- "Back Squat 5x5 + Core"
- "EMOM 20min Assault Bike"
- "Bench Press + 21-15-9"
- "Deadlift + Box Jumps"
- "Zone 2 Cardio 30min"

**Example:**
```bash
curl -X POST http://localhost:5000/clients/John%20Doe/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "workout_type": "Back Squat 5x5 + Core",
    "date": "2024-03-16",
    "duration_min": 60,
    "notes": "Great session"
  }'
```

---

## 📏 Metrics Endpoints

### 13. Get Client Metrics

Retrieve body metrics history for a client.

```http
GET /clients/{name}/metrics
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Response (200 OK):**
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": 1,
      "client_name": "John Doe",
      "date": "2024-03-16",
      "weight": 79.5,
      "waist": 85.0,
      "bodyfat": 18.5
    },
    {
      "id": 2,
      "client_name": "John Doe",
      "date": "2024-03-10",
      "weight": 80.5,
      "waist": 86.0,
      "bodyfat": 19.0
    }
  ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/clients/John%20Doe/metrics
```

---

### 14. Record Body Metrics

Log body measurements for a client.

```http
POST /clients/{name}/metrics
Content-Type: application/json
```

**Path Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| name | string | John Doe |

**Request Body:**
```json
{
  "date": "2024-03-16",
  "weight": 79.5,
  "waist": 85.0,
  "bodyfat": 18.5
}
```

**Request Fields:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| date | string | Yes | YYYY-MM-DD format |
| weight | float | No | kg, 30-300 |
| waist | float | No | cm, 40-200 |
| bodyfat | float | No | %, 5-50 |

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Metrics recorded successfully",
  "data": {
    "client_name": "John Doe",
    "date": "2024-03-16"
  }
}
```

**Response (400 Bad Request) - Missing Date:**
```json
{
  "status": "error",
  "message": "Date is required"
}
```

**Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Client 'John Doe' not found"
}
```

**Metrics Guide:**

| Metric | Range | Frequency | Purpose |
|--------|-------|-----------|---------|
| Weight | 30-300 kg | Weekly | Track overall mass |
| Waist | 40-200 cm | Weekly/Monthly | Track fat loss |
| Body Fat | 5-50% | Monthly | Track composition |

**Example:**
```bash
curl -X POST http://localhost:5000/clients/John%20Doe/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-03-16",
    "weight": 79.5,
    "waist": 85.0,
    "bodyfat": 18.5
  }'
```

---

## ⚠️ Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "status": "error",
  "message": "Descriptive error message",
  "code": "ERROR_CODE"
}
```

### Error Codes

| Status | Message | Likely Cause | Solution |
|--------|---------|-------------|----------|
| 400 | Missing required fields | Incomplete request | Add missing fields |
| 400 | Invalid value for field | Wrong data type | Check field format |
| 404 | Resource not found | ID/name doesn't exist | Verify resource exists |
| 409 | Duplicate resource | Name already exists | Use different name |
| 500 | Internal server error | Server crash | Check server logs |

### Common Error Scenarios

#### Invalid Program Name
```bash
$ curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "age": 30,
    "weight": 70,
    "program": "Invalid Program"
  }'
```

**Response:**
```json
{
  "status": "error",
  "message": "Program must be one of: ['Fat Loss (FL)', 'Muscle Gain (MG)', 'Beginner (BG)']"
}
```

#### Client Not Found
```bash
$ curl -X GET http://localhost:5000/clients/NonExistent
```

**Response:**
```json
{
  "status": "error",
  "message": "Client 'NonExistent' not found"
}
```

#### Duplicate Client
```bash
$ curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 30, "weight": 70, "program": "Fat Loss (FL)"}'

$ curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 30, "weight": 70, "program": "Fat Loss (FL)"}'
```

**Response (Second Request):**
```json
{
  "status": "error",
  "message": "Client with this name already exists"
}
```

---

## 💻 Integration Examples

### JavaScript/Fetch

```javascript
// Get all clients
fetch('http://localhost:5000/clients')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Create a client
const client = {
  name: 'John Doe',
  age: 30,
  weight: 80.5,
  program: 'Fat Loss (FL)'
};

fetch('http://localhost:5000/clients', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(client)
})
  .then(response => response.json())
  .then(data => console.log('Client created:', data))
  .catch(error => console.error('Error:', error));
```

### Python/Requests

```python
import requests

# Base URL
BASE_URL = 'http://localhost:5000'

# Get all clients
response = requests.get(f'{BASE_URL}/clients')
print(response.json())

# Create a client
client_data = {
    'name': 'John Doe',
    'age': 30,
    'weight': 80.5,
    'program': 'Fat Loss (FL)'
}

response = requests.post(
    f'{BASE_URL}/clients',
    json=client_data
)
print(response.json())

# Record progress
progress_data = {'adherence': 85}

response = requests.post(
    f'{BASE_URL}/clients/John Doe/progress',
    json=progress_data
)
print(response.json())
```

### cURL Examples

```bash
# Check health
curl -X GET http://localhost:5000/health

# List all clients
curl -X GET http://localhost:5000/clients

# Create client
curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 30,
    "weight": 80.5,
    "program": "Fat Loss (FL)"
  }'

# Get client details
curl -X GET "http://localhost:5000/clients/John%20Doe"

# Update client
curl -X PUT "http://localhost:5000/clients/John%20Doe" \
  -H "Content-Type: application/json" \
  -d '{"age": 31, "weight": 79.5}'

# Record progress
curl -X POST "http://localhost:5000/clients/John%20Doe/progress" \
  -H "Content-Type: application/json" \
  -d '{"adherence": 85}'

# Log workout
curl -X POST "http://localhost:5000/clients/John%20Doe/workouts" \
  -H "Content-Type: application/json" \
  -d '{
    "workout_type": "Back Squat 5x5",
    "date": "2024-03-16",
    "duration_min": 60,
    "notes": "Great session"
  }'

# Delete client
curl -X DELETE "http://localhost:5000/clients/John%20Doe"
```

### Postman Collection

Import this JSON into Postman:

```json
{
  "info": {
    "name": "ACEest Fitness API",
    "version": "1.0.0"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/health"
      }
    },
    {
      "name": "Get All Programs",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/programs"
      }
    },
    {
      "name": "Create Client",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/clients",
        "body": {
          "mode": "raw",
          "raw": "{\"name\": \"John Doe\", \"age\": 30, \"weight\": 80.5, \"program\": \"Fat Loss (FL)\"}"
        }
      }
    }
  ]
}
```

---

## 📚 Endpoint Summary Table

| Endpoint | Method | Purpose | Auth | Rate Limit |
|----------|--------|---------|------|-----------|
| /health | GET | Check API status | ✗ | None |
| /initialize | POST | Initialize DB | ✗ | None |
| /programs | GET | List programs | ✗ | None |
| /clients | GET | List all clients | ✗ | None |
| /clients | POST | Create client | ✗ | None |
| /clients/{name} | GET | Get client | ✗ | None |
| /clients/{name} | PUT | Update client | ✗ | None |
| /clients/{name} | DELETE | Delete client | ✗ | None |
| /clients/{name}/progress | GET | Get progress | ✗ | None |
| /clients/{name}/progress | POST | Record progress | ✗ | None |
| /clients/{name}/workouts | GET | Get workouts | ✗ | None |
| /clients/{name}/workouts | POST | Log workout | ✗ | None |
| /clients/{name}/metrics | GET | Get metrics | ✗ | None |
| /clients/{name}/metrics | POST | Record metrics | ✗ | None |

---

**API Documentation Generated:** March 2024  
**Status:** Production Ready ✅  
**Contact:** devops@aceest-fitness.com
