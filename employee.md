# Employee Management Service Documentation
*Version: 1.0.0*  
*Last Updated: 2025‑11‑04*  

> **Disclaimer** – This documentation was generated from a repository analysis.  Some implementation details (e.g. request/response payloads, security) are inferred from the code‑base and the original README.  Please adjust the sections that differ from the actual source code.

---  

## Table of Contents
1. [Service Overview](#1-service-overview)  
2. [Architecture](#2-architecture)  
3. [API Documentation](#3-api-documentation)  
   - [Common Conventions](#common-conventions)  
   - [Endpoints](#endpoints)  
4. [Setup & Installation](#4-setup--installation)  
5. [Configuration](#5-configuration)  
6. [Usage Examples](#6-usage-examples)  
7. [Dependencies](#7-dependencies)  
8. [Development & Contribution](#8-development--contribution)  
9. [Appendix](#9-appendix)  

---  

## 1. Service Overview
The **Employee Management Service** is a Spring Boot micro‑service that centralises all employee‑related operations for the Java track of the organisation.  

### Core Capabilities
| Capability | Description |
|------------|-------------|
| **Employee retrieval** | Fetch full employee details by unique identifier. |
| **On‑boarding** | Add a new employee of any supported role (FTE, STE, Intern, etc.) via a single endpoint that infers the role from the URL path. |
| **Resignation handling** | Return the notice‑period required for a given employee based on company policy. |
| **Date‑based analytics** | Count employees who joined, left, or were onboarded on a specific date. |
| **Extensible role model** | New roles can be added without code changes – only the enumeration and validation rules need updates. |

> **Goal** – Provide a simple, REST‑ful API that can be consumed by internal tools (HR portals, payroll systems, reporting dashboards) and external partners.

---  

## 2. Architecture
### 2.1 High‑Level Diagram  

```
┌─────────────────────────────────────────────────────┐
│                     CLIENTS                         │
│  (Web UI, Mobile, CLI, Other Services)              │
└───────────────▲───────────────────────▲─────────────┘
                │                       │
                │ HTTP (JSON)           │
                ▼                       ▼
┌─────────────────────────────────────────────────────┐
│               Spring Boot Application                │
│  ┌─────────────────────┐   ┌─────────────────────┐  │
│  │   REST Controllers  │   │   Exception Handler │  │
│  └─────────▲───────────┘   └─────────▲───────────┘  │
│            │                         │           │
│            │                         │           │
│  ┌─────────▼───────────┐   ┌─────────▼───────────┐ │
│  │   Service Layer     │   │   Validation / DTO  │ │
│  └─────────▲───────────┘   └─────────▲───────────┘ │
│            │                         │           │
│            │                         │           │
│  ┌─────────▼───────────┐   ┌─────────▼───────────┐ │
│  │  Repository (JPA)   │   │   Domain Model      │ │
│  └─────────▲───────────┘   └─────────▲───────────┘ │
│            │                         │           │
│            ▼                         ▼           │
│   ┌───────────────┐          ┌───────────────┐   │
│   │   Database    │          │   In‑memory   │   │
│   │ (MySQL / PG)  │          │  H2 (dev)     │   │
│   └───────────────┘          └───────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 2.2 Layered Breakdown
| Layer | Responsibility | Typical Spring Artefacts |
|-------|----------------|--------------------------|
| **Controller** | Exposes REST endpoints, maps request payloads to DTOs, returns responses. | `@RestController`, `@RequestMapping`, `@PathVariable`, `@RequestBody` |
| **Service** | Business logic (e.g. role‑specific validation, notice‑period calculation). | `@Service`, transaction handling (`@Transactional`) |
| **Repository** | Data‑access using Spring Data JPA. | `JpaRepository<Employee, Long>` |
| **Domain Model** | JPA entities (`Employee`, `Role` enum) and value objects. | `@Entity`, Lombok (`@Data`, `@Builder`) |
| **DTO / Validation** | Input/Output objects that decouple API contracts from persistence model. | `@Validated`, `@NotBlank`, `@JsonProperty` |
| **Exception Handling** | Centralised error translation to HTTP status codes. | `@ControllerAdvice`, `@ExceptionHandler` |
| **Configuration** | Externalises DB credentials, server port, profile‑specific settings. | `application.yml`, `@ConfigurationProperties` |

### 2.3 External Dependencies
* **Database** – MySQL (production) / H2 (development & test).  
* **Security** – The current project does **not** enforce authentication, but an optional Spring Security starter is included and can be enabled with a profile (`security`).  
* **Documentation** – Swagger/OpenAPI is auto‑generated on `/v3/api-docs` and UI available at `/swagger-ui.html` (if the `springdoc-openapi-ui` dependency is present).  

---  

## 3. API Documentation  

> **Base URL** – `http://localhost:8080/api/v1` (configurable via `server.servlet.context-path`).  

### Common Conventions
| Item | Convention |
|------|------------|
| **Media Type** | `application/json` for both request and response bodies. |
| **Date Format** | ISO‑8601 (`yyyy-MM-dd`). All date path variables must follow this format. |
| **Success Codes** | `200 OK` (GET), `201 Created` (POST), `204 No Content` (DELETE). |
| **Error Codes** | `400 Bad Request` (validation), `404 Not Found` (missing employee), `500 Internal Server Error` (unexpected). |
| **Error Payload** | ```json { "timestamp":"2025‑11‑04T12:34:56.789+00:00", "status":400, "error":"Bad Request", "message":"<detail>", "path":"/api/v1/..." }``` |
| **Authentication** | None by default.  When `security` profile is active, the API expects a JWT Bearer token in the `Authorization` header. |

### 3.1 Endpoints  

| # | Method | Path | Description | Request Body | Response Body |
|---|--------|------|-------------|--------------|---------------|
| 1 | `GET` | `/employee/{id}` | Retrieve a single employee’s full profile. | – | `EmployeeResponse` |
| 2 | `POST` | `/onboard/{role}` | On‑board a new employee of the given role (e.g. `SDE`, `HR`, `Intern`). | `EmployeeCreateRequest` | `EmployeeResponse` (201) |
| 3 | `GET` | `/employee/resignation/{id}` | Get the required notice‑period (in days) for the employee’s resignation. | – | `{ "employeeId": 12, "noticePeriodDays": 30 }` |
| 4 | `GET` | `/employee/date/{date}` | Count employees **joined** on the supplied date. | – | `{ "date":"2024-07-01", "joinedCount":5 }` |
| 5 | `GET` | `/employee/endDate/{date}` | Count employees **leaving** (end‑date) on the supplied date. | – | `{ "date":"2024-12-31", "leavingCount":2 }` |
| 6 | `GET` | `/employee/onboardingDate/{date}` | Count employees **onboarded** (first day in system) on the supplied date. | – | `{ "date":"2024-07-01", "onboardedCount":5 }` |

> **Note** – All date path variables must be URL‑encoded (`2024-07-01`).

#### 3.1.1 `GET /employee/{id}`
```http
GET /api/v1/employee/42 HTTP/1.1
Host: localhost:8080
Accept: application/json
```

**Response (200)**
```json
{
  "id": 42,
  "firstName": "Alice",
  "lastName": "Johnson",
  "email": "alice.johnson@example.com",
  "role": "SDE",
  "startDate": "2024-07-01",
  "endDate": null,
  "status": "ACTIVE"
}
```

**Possible Errors**
| Code | Reason |
|------|--------|
| 404 | Employee with the supplied `id` does not exist. |
| 400 | `id` is not a numeric value. |

#### 3.1.2 `POST /onboard/{role}`
```http
POST /api/v1/onboard/SDE HTTP/1.1
Host: localhost:8080
Content-Type: application/json
Accept: application/json

{
  "firstName": "Bob",
  "lastName": "Smith",
  "email": "bob.smith@example.com",
  "startDate": "2024-10-15"
}
```

**Response (201 Created)**
```json
{
  "id": 103,
  "firstName": "Bob",
  "lastName": "Smith",
  "email": "bob.smith@example.com",
  "role": "SDE",
  "startDate": "2024-10-15",
  "endDate": null,
  "status": "ACTIVE"
}
```

**Validation Rules**
| Field | Constraint |
|-------|------------|
| `firstName`, `lastName` | Not blank, max 50 chars |
| `email` | Valid email format, unique |
| `startDate` | Must be today or a future date |
| `role` (path variable) | Must be one of the supported enum values (`SDE`, `SDET`, `IT`, `MANAGER`, `HR`, `RECRUITMENT`, `FINANCE`, `ARCHITECT`, `STE`, `INTERN`). |

**Possible Errors**
| Code | Reason |
|------|--------|
| 400 | Validation failure – see error payload for details. |
| 409 | Email already exists. |
| 404 | Role not recognised (invalid path variable). |

#### 3.1.3 `GET /employee/resignation/{id}`
```http
GET /api/v1/employee/resignation/42 HTTP/1.1
Host: localhost:8080
Accept: application/json
```

**Response (200)**
```json
{
  "employeeId": 42,
  "noticePeriodDays": 30
}
```

*The notice‑period is derived from the employee’s role and tenure (business rule defined in `ResignationService`).*

#### 3.1.4 `GET /employee/date/{date}`
```http
GET /api/v1/employee/date/2024-07-01 HTTP/1.1
Host: localhost:8080
Accept: application/json
```

**Response (200)**
```json
{
  "date": "2024-07-01",
  "joinedCount": 5
}
```

#### 3.1.5 `GET /employee/endDate/{date}`
```http
GET /api/v1/employee/endDate/2024-12-31 HTTP/1.1
Host: localhost:8080
Accept: application/json
```

**Response (200)**
```json
{
  "date": "2024-12-31",
  "leavingCount": 2
}
```

#### 3.1.6 `GET /employee/onboardingDate/{date}`
```http
GET /api/v1/employee/onboardingDate/2024-07-01 HTTP/1.1
Host: localhost:8080
Accept: application/json
```

**Response (200)**
```json
{
  "date": "2024-07-01",
  "onboardedCount": 5
}
```

### 3.2 Swagger / OpenAPI
If the optional `springdoc-openapi-ui` dependency is on the classpath, the API documentation is automatically published at:

```
http://localhost:8080/v3/api