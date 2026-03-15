# API Documentation

This document lists the available API endpoints for the SkillTrack backend.

## Authentication & Identity

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/api/register/` | POST | Create a new user account. | No |
| `/api/token/` | POST | Login to receive access and refresh tokens. | No |
| `/api/token/refresh/` | POST | Refresh an expired access token. | No |

## User Profile

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/api/v1/profiles/me/` | GET | Fetch the current user's profile and nested experiences. | Yes |
| `/api/v1/profiles/me/` | PUT/PATCH | Update user profile details (title, phone, bio, etc.). | Yes |

## Work Experience

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/api/v1/profiles/experiences/` | GET | List all experiences for the logged-in user. | Yes |
| `/api/v1/profiles/experiences/` | POST | Create a new work experience entry. | Yes |
| `/api/v1/profiles/experiences/<id>/` | GET | View a specific work experience. | Yes |
| `/api/v1/profiles/experiences/<id>/` | PUT/PATCH | Update a specific work experience. | Yes |
| `/api/v1/profiles/experiences/<id>/` | DELETE | Delete a specific work experience. | Yes |

## System Administration

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/admin/` | GET | Django Admin interface. | Yes (Staff) |

---
**Note:** All API calls (except Auth) require a `Bearer <token>` in the `Authorization` header. All URLs should end with a trailing slash `/`.
