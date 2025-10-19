# Portal Management Service

A lean FastAPI service with SQLAlchemy to manage portals and users,
running in Docker containers.

## Features

- **Portals**: UUID, name
- **Users**: UUID, name, foreign key to portal
- Full CRUD operations for both entities
- PostgreSQL database
- Docker containerization

## Quick Start

1. **Start the services:**

   ```bash
   docker-compose up --build
   ```

2. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

## API Endpoints

### Portals

- `POST /portals/` - Create a portal
- `GET /portals/` - List all portals
- `GET /portals/{portal_id}` - Get a specific portal
- `DELETE /portals/{portal_id}` - Delete a portal

### Users

- `POST /users/` - Create a user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get a specific user
- `GET /portals/{portal_id}/users/` - Get users for a portal
- `DELETE /users/{user_id}` - Delete a user

## Example Usage

### Create a portal:

```bash
curl -X POST "http://localhost:8000/portals/" \
     -H "Content-Type: application/json" \
     -d '{"name": "My Portal"}'
```

### Create a user for the portal:

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "portal_id": "PORTAL_UUID_HERE"}'
```

## Development

The service uses:

- FastAPI for the web framework
- SQLAlchemy for ORM
- PostgreSQL as the database
- Docker for containerization
