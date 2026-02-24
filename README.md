# ArticleSpace

A professional, modular article publishing platform built with Django and Django REST Framework. This application features a secure role-based access control system, a comprehensive publishing workflow, and full REST API support.

## Technical Architecture

### 1. Modular Design
The project uses a domain-driven modular structure:
- `core/`: Project configuration and global settings.
- `apps/accounts/`: Identity management, custom user models, and role-based permissions.
- `apps/articles/`: Core business logic for article lifecycles, state management, and content delivery.

### 2. Role-Based Access Control (RBAC)
The system enforces security through a tiered permission model:
- **Admin**: Full administrative oversight of users and content.
- **Editor**: Authorized to create, manage, and execute the publishing workflow.
- **Viewer**: Restricted to read-only access for published articles.

### 3. Publishing Workflow
Implements a state-driven pipeline (`DRAFT` → `PUBLISHED`).
- Content is restricted via dynamic Queryset filtering based on user authorization and article status.
- Secure state transitions handled via backend logic to ensure data integrity.

### 4. Headless API & Authentication
- **RESTful API**: Built with Django REST Framework for seamless frontend/mobile integration.
- **JWT Authentication**: Utilizes JSON Web Tokens for secure, stateless API communication.
- **Session Auth**: Supports traditional session-based authentication for the Web UI.

### 5. Deployment & DevOps
- **Containerization**: Fully Dockerized environment using Docker Compose.
- **Database**: PostgreSQL integration for production-grade reliability.
- **Static Files**: Optimized delivery via WhiteNoise.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Identity**: SimpleJWT (JWT Authentication)
- **Database**: PostgreSQL
- **Environment**: Docker, Gunicorn

## Getting Started

### Local Development (Docker)
1. Build and launch the containers:
   ```bash
   docker-compose up --build
   ```
2. Execute migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### API Endpoints (Integration Layer)
- `POST /api/v1/auth/token/`: Authenticate and receive JWT tokens.
- `GET /api/v1/articles/`: Retrieve published content.
- `POST /api/v1/articles/`: Author a new draft (Authorized roles only).
- `POST /api/v1/articles/{slug}/publish/`: Execute the publishing workflow for a specific article.

---
ArticleSpace stands as a production-grade template for a publishing platform, demonstrating a clear understanding of backend security, API design standards, and modular software engineering—perfect for a professional Software Engineering portfolio.
