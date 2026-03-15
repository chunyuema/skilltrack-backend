# Architectural Decisions

## Work Experience Implementation

### 1. Model Relationship: User -> Profile -> Experience
- **Decision:** Use a One-to-Many relationship from `Profile` to `Experience`.
- **Reasoning:** 
    - A `User` represents the identity and login.
    - A `Profile` represents the professional persona.
    - An `Experience` represents a specific job or role.
    - Decoupling `Profile` from `User` allows for future flexibility (e.g., multiple personas for one user).
    - Grouping professional metadata (like experiences) under the `Profile` makes the domain model cleaner.

### 2. Primary Key Strategy
- **Decision:** Each `Experience` entry has its own unique `id` (BigAutoField).
- **Reasoning:** 
    - Each job entry is a distinct entity that needs to be individually addressable for updates or deletions.
    - `profile_id` is used as a Foreign Key to link the experience to its owner.
    - Consistent with Django's default behavior and general database best practices.

### 3. Data Representation
- **Decision:** Use `JSONField` for `technologies`.
- **Reasoning:** 
    - Provides flexibility for a list of tags without requiring a separate table for a prototype.
    - Easily maps to the requested frontend format: `technologies: ['React', 'TypeScript', 'Node.js']`.
- **Decision:** Use `CharField` for `start_date` and `end_date` (nullable for "Present").
- **Reasoning:** 
    - Simpler for "YYYY-MM" formatting than standard DateFields.
    - Supports the "Present" logic more easily during serialization.
