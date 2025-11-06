# java‑track‑assignment – Employee Management Service  

*An Employee Management System for the Java track, built with Spring Boot.*

---  

## Table of Contents
1. [Service Overview](#service-overview)  
2. [Architecture](#architecture)  
3. [API Documentation](#api-documentation)  
   - [Common Conventions](#common-conventions)  
   - [Endpoints](#endpoints)  
4. [Setup & Installation](#setup--installation)  
5. [Configuration](#configuration)  
6. [Usage Examples](#usage-examples)  
   - [cURL](#curl-examples)  
   - [Java (RestTemplate)](#java-resttemplate-example)  
   - [Postman Collection (link)](#postman-collection)  
7. [Dependencies](#dependencies)  
8. [Development & Contribution](#development--contribution)  
9. [License & Contact](#license--contact)  

---  

## Service Overview
The **Employee Management Service** (EMS) is a lightweight RESTful API that enables:

| Feature | Description |
|---------|-------------|
| **Employee retrieval** | Fetch full employee details by their unique identifier. |
| **On‑boarding** | Create new employees for a wide range of roles (FTE, STE, Intern, etc.) via dedicated endpoints. |
| **Resignation handling** | Return the notice‑period required for a given employee. |
| **Date‑based analytics** | Count employees who joined, left, or were onboarded on a specific date. |
| **Stateless & portable** | Runs as a self‑contained Spring Boot jar; no external servlet container required. |
| **Extensible** | Clean layered architecture (Controller → Service → Repository) that can be expanded with new roles, validation, security, or persistence back‑ends. |

The service is primarily intended for **demo / training** purposes but follows production‑grade patterns (DTOs, validation, exception handling, and unit/integration tests).

---  

## Architecture
```
+------------------------------------------------------------+
|                         CLIENTS                           |
|  (Browser, Postman, curl, other services, mobile apps)    |
+------------------------------|-----------------------------+
                               |
                               v
+------------------------------+-----------------------------+
|                     Spring Boot Application               |
|  +--------------------+   +----------------------------+   |
|  |   Controllers      |   |   Exception Handlers      |   |
|  +--------------------+   +----------------------------+   |
|            |                         |                 |
|            v                         v                 |
|  +--------------------+   +----------------------------+   |
|  |      Services      |   |   Validation / Mapper      |   |
|  +--------------------+   +----------------------------+   |
|            |                         |                 |
|            v                         v                 |
|  +--------------------+   +----------------------------+   |
|  |   Repositories     |   |   Domain Entities (JPA)   |   |
|  +--------------------+   +----------------------------+   |
|            |                         |                 |
|            v                         v                 |
|  +------------------------------------------------------+ |
|  |                 Persistence Layer                    | |
|  | (H2 in‑memory for dev / test, configurable to MySQL) | |
|  +------------------------------------------------------+ |
+------------------------------------------------------------+
```

### Layer responsibilities  

| Layer | Responsibility |
|-------|----------------|
| **Controller** | Maps HTTP requests → DTOs, delegates to Service, returns appropriate HTTP responses. |
| **Service** | Business logic (e.g., calculating notice period, checking duplicate employee IDs). |
| **Repository** | Spring Data JPA interfaces for CRUD operations on `Employee` entities. |
| **Domain Entity** | JPA‑annotated `Employee` POJO representing rows in the `employees` table. |
| **Exception Handler** | Centralised `@ControllerAdvice` translating Java exceptions into JSON error payloads. |
| **Configuration** | `application.yml` + profile‑specific overrides (`application-local.yml`). |

---  

## API Documentation  

### Common Conventions
| Item | Description |
|------|-------------|
| **Base URL** | `http://localhost:{port}` (default port `8080`). |
| **Content‑Type** | `application/json` for request & response bodies. |
| **Date format** | ISO‑8601 – `yyyy-MM-dd` (e.g., `2025-01-31`). |
| **HTTP status codes** | `200 OK` – success; `201 Created` – resource created; `400 Bad Request` – validation error; `404 Not Found` – employee not found; `500 Internal Server Error` – unexpected failures. |
| **Authentication** | None by default. The service can be wrapped with Spring Security (e.g., JWT) if required – see *Extending the Service* section. |
| **Error payload** | ```json { "timestamp": "...", "status": 400, "error": "Bad Request", "message": "validation failed", "path": "/employee" }``` |

---

### Endpoints  

| # | HTTP Method | Path | Description | Request Body | Success Response |
|---|-------------|------|-------------|--------------|------------------|
| 1 | **GET** | `/employee/{id}` | Retrieve employee details for the given **id**. | – | `200` → `EmployeeDto` |
| 2 | **POST** | `/onboard/{role}` | On‑board a **Full‑Time Employee (FTE)**, **STE**, **Intern**, etc. Role is case‑insensitive (`SDE`, `SDET`, `IT`, `MANAGER`, `HR`, `RECRUITMENT`, `FINANCE`, `ARCHITECT`, `STE`, `INTERN`). | `EmployeeCreateDto` | `201` → `EmployeeDto` |
| 3 | **GET** | `/employee/resignation` | Return the resignation **notice period** (in days) for a given employee. Query param `employeeId` is required. | – | `200` → `{ "employeeId": 12, "noticePeriodDays": 30 }` |
| 4 | **GET** | `/employee/date/{date}` | Count the number of employees **joined** on the supplied date. | – | `200` → `{ "date": "2025-07-01", "joinedCount": 5 }` |
| 5 | **GET** | `/employee/endDate/{date}` | Count the number of employees **leaving** (i.e., resignation end date) on the supplied date. | – | `200` → `{ "date": "2025-07-31", "leavingCount": 2 }` |
| 6 | **GET** | `/employee/onboardingDate/{date}` | Count the number of employees **on‑boarded** (i.e., start date) on the supplied date. | – | `200` → `{ "date": "2025-07-01", "onboardedCount": 4 }` |

> **Note:** All `POST /onboard/{role}` endpoints share the same request contract (`EmployeeCreateDto`) – the only difference is the role path variable.  

---

#### 1. Retrieve Employee Details  

```
GET /employee/42
```

**Response (200)**  

```json
{
  "id": 42,
  "firstName": "Alice",
  "lastName": "Smith",
  "email": "alice.smith@example.com",
  "role": "SDE",
  "startDate": "2025-06-01",
  "endDate": null,
  "noticePeriodDays": null
}
```

**Error (404)**  

```json
{
  "timestamp": "2025-11-04T12:34:56.789+00:00",
  "status": 404,
  "error": "Not Found",
  "message": "Employee with id 42 not found",
  "path": "/employee/42"
}
```

---

#### 2. On‑board a New Employee  

```
POST /onboard/SDE
Content-Type: application/json
```

**Request body (`EmployeeCreateDto`)**  

```json
{
  "firstName": "Bob",
  "lastName": "Johnson",
  "email": "bob.johnson@example.com",
  "startDate": "2025-08-01",
  "noticePeriodDays": 30
}
```

**Response (201 Created)**  

```json
{
  "id": 101,
  "firstName": "Bob",
  "lastName": "Johnson",
  "email": "bob.johnson@example.com",
  "role": "SDE",
  "startDate": "2025-08-01",
  "endDate": null,
  "noticePeriodDays": 30
}
```

**Validation errors (400)**  

```json
{
  "timestamp": "2025-11-04T12:35:01.123+00:00",
  "status": 400,
  "error": "Bad Request",
  "message": "email must be a well‑formed email address",
  "path": "/onboard/SDE"
}
```

---

#### 3. Get Resignation Notice Period  

```
GET /employee/resignation?employeeId=101
```

**Response (200)**  

```json
{
  "employeeId": 101,
  "noticePeriodDays": 30
}
```

**Error (404)** – employee not found  

```json
{
  "timestamp": "...",
  "status": 404,
  "error": "Not Found",
  "message": "Employee with id 101 not found",
  "path": "/employee/resignation"
}
```

---

#### 4‑6. Date‑Based Counters  

```
GET /employee/date/2025-08-01
GET /employee/endDate/2025-12-31
GET /employee/onboardingDate/2025-08-01
```

All return a simple JSON payload with the date and a numeric `count`. Example for the first endpoint:

```json
{
  "date": "2025-08-01",
  "joinedCount": 3
}
```

---

### Extending the API (Future Work)

| Feature | How to add |
|---------|------------|
| **Authentication / Authorization** | Add Spring Security with JWT or Basic Auth; protect `/onboard/**` and analytics endpoints. |
| **Pagination / Filtering** | Extend `/employee` with query params (`page`, `size`, `role`, `status`). |
| **Bulk On‑boarding** | Add `POST /onboard/batch` accepting a list of `EmployeeCreateDto`. |
| **Audit Trail** | Enable Spring Data JPA Auditing (`@CreatedDate`, `@LastModifiedDate`). |
| **External DB** | Switch the default H2 to MySQL/PostgreSQL via profile‑specific datasource config. |

---  

## Setup & Installation  

### Prerequisites  

| Tool | Minimum version |
|------|-----------------|
| **Java Development Kit (JDK)** | 17 (or later) |
| **Maven** | 3.8.x (wrapper `mvnw` is bundled) |
| **Git** | any recent version |
| **Docker** (optional) | 20.x – for running a MySQL container if you replace H2 |

> The project ships with the **Maven Wrapper** (`mvnw` / `mvnw.cmd`), so you do **not** need a global Maven installation – the wrapper will download the correct Maven version automatically.

### Step‑by‑step

```bash
# 1. Clone the repository
git clone https://github.com/<your‑org>/javaEmployeeOnboarding.git
cd javaEmployeeOnboarding

# 2. Build the project (tests will run automatically)
./mvnw clean verify

# 3. Run the application (default profile = "local")
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
#   OR (if you prefer the packaged jar)
./mvnw package -DskipTests
java -jar target/javaEmployeeOnboarding-0.0.1-SNAPSHOT.jar \
     --spring.profiles.active=local
```

The service will start on **http://localhost:8080** (unless overridden in `application.yml`).

### Running with Docker (optional)

```bash
# Build the Docker image
docker build -t java-employee-onboarding:latest .

# Run the container (exposes 8080)
docker run -p 8080:8080 java-employee-onboarding:latest
```

If you want to use MySQL instead of the embedded H2, spin up a container first:

```bash
docker run -d \
  --name mysql-dev \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=employee_db \
  -p 3306:3306 mysql:8
```

Then start the Spring Boot app with the `prod` profile (which reads `application-prod.yml` where you can configure the datasource URL, username, password).

---  

## Configuration  

Configuration lives under `src/main/resources`. The default file is `application.yml`; environment‑specific overrides are in `application-local.yml` and can be added for `prod`, `test`, etc.

### `application.yml` (excerpt)

```yaml
server:
  port: 8080

spring:
  datasource:
    # Default to H2 in‑memory for dev and tests
    url: jdbc:h2:mem:employee-db;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
    driver-class-name: org.h2.Driver
    username: sa
    password:
    platform: h2
  jpa:
    hibernate:
      ddl-auto: update   # create‑drop / update / validate / none
    show-sql: true
    properties:
      hibernate:
        format_sql: true

# Logging
logging:
  level:
    root: INFO
    com.example: DEBUG
```

### `application-local.yml`

```yaml
spring:
  profiles: local

  # Override DB if you prefer a file‑based H2 or external DB
  datasource:
    url: jdbc:h2:file:./data/employee-db
    username: sa
    password:
```

### Overriding via Environment Variables  

Spring Boot automatically maps environment variables (uppercase, underscores) to properties. For example, to run the service on port `9090`:

```bash
export SERVER_PORT=9090
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

Commonly overridden variables:

| Variable | Purpose |
|----------|---------|
| `SERVER_PORT` | HTTP port |
| `SPRING_DATASOURCE_URL` | JDBC URL |
| `SPRING_DATASOURCE_USERNAME` | DB user |
| `SPRING_DATASOURCE_PASSWORD` | DB password |
| `SPRING_PROFILES_ACTIVE` | Active Spring profile (`local`, `prod`, `test`) |

---  

## Usage Examples  

### cURL Examples  

```bash
# 1️⃣ Get employee #5
curl -s http://localhost:8080