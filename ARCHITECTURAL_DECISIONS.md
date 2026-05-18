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

## Skills Matrix Implementation

### 1. Hierarchical Model Structure
- **Decision:** Use a four-tier relational model: `SkillTheme` -> `SkillSubCategory` -> `Skill` <- `UserSkill` (junction with `Profile`).
- **Reasoning:** 
    - Normalization allows for easy addition of new global skills without redundant data.
    - `UserSkill` isolates user-specific proficiency (level 0-5) from the global skill definition.
    - Hierarchical nesting reflects the "Professional Portfolio" UI structure (Themes > Subcategories > Skills).

### 2. Separation of Concerns (Skills App)
- **Decision:** Separate all skill-related models, views, and serializers into a dedicated `skills` Django app.
- **Reasoning:** 
    - Decouples professional identity (`profiles`) from the competency taxonomy (`skills`).
    - Prepares the system for future features where skills might be used independently of profiles (e.g., Job Postings, Team Analytics).
    - Makes the codebase more modular and easier to maintain as the number of technical domains grows.

### 3. Identifier Strategy
- **Decision:** Use `CharField` (slugs/keys) as Primary Keys for Theme, SubCategory, and Skill.
- **Reasoning:** 
    - Enables stable mapping between frontend constants and backend database records.
    - Prevents reliance on auto-incrementing integers which might drift between environments during early development.

### 3. Contextual Serialization
- **Decision:** Use a `SerializerMethodField` to inject the user's skill level into the global skill tree.
- **Reasoning:** 
    - Allows the frontend to fetch the entire matrix (including unlearned skills) in a single request.
    - Provides a "Full Tree" view which is necessary for the Matrix UI to show empty slots.
