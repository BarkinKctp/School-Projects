# User Management App

Full-stack CRUD app with React frontend and Express/PostgreSQL backend.

## Quick Start

### Backend
```bash
cd backend
cp .env.example .env  # configure your PostgreSQL credentials
npm install
npm run dev           # runs on http://localhost:3000
```

### Frontend
```bash
cd frontend
npm install
npm run dev           # runs on http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user` | Get all users |
| GET | `/api/user/:id` | Get user by ID |
| POST | `/api/user` | Create user |
| PUT | `/api/user/:id` | Update user |
| DELETE | `/api/user/:id` | Delete user |

## Tech Stack

**Frontend:** React, Vite  
**Backend:** Express.js, PostgreSQL, Joi
