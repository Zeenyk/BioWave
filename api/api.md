# 📡 BioWave API Documentation

Base URL: `http://<biowave-server-ip>:<port>/api`

Authentication: *(Optional)* – add `Authorization: Bearer <token>` header for protected routes.

## 📘 Endpoints Overview

### 🔁 Status & Control

#### `GET /status`

Returns current bioreactor state and latest sensor readings.

**Response:**

```json
{
  "timestamp": "2025-04-11T10:00:00Z",
  "stirring": true,
  "rpm": 300,
  "temperature": 37.5,
  "ph": 6.8,
  "oxygen": 98
}
```

---

#### `POST /control`

Send manual control commands (e.g., set RPM, toggle stirring).

**Payload:**

```json
{
  "command": "set_rpm",
  "value": 250
}
```

---

### ⏱️ Scheduled Operations

#### `GET /schedule`

List all scheduled operations.

**Response:**

```json
[
  {
    "id": 1,
    "command": "set_rpm",
    "value": 300,
    "time": "2025-04-11T12:00:00Z"
  }
]
```

---

#### `POST /schedule`

Add a new scheduled operation.

**Payload:**

```json
{
  "command": "set_rpm",
  "value": 300,
  "time": "2025-04-11T12:00:00Z"
}
```

---

#### `DELETE /schedule/{id}`

Remove a scheduled operation.

---

### 📊 Data Logging

#### `GET /logs`

Download log entries. Optional filters: `?from=...&to=...`

**Response:**

```json
[
  {
    "timestamp": "2025-04-11T10:00:00Z",
    "temperature": 37.2,
    "ph": 6.9,
    "rpm": 200
  }
]
```

---

#### `GET /logs/export`

Returns CSV file of logs. Optional filters: `?from=...&to=...`

---

### 🔐 Users (Optional)

#### `POST /auth/login`

Login and receive access token.

**Payload:**

```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response:**

```json
{ "token": "..." }
```

---

#### `POST /auth/logout`

Invalidate current token.

---
