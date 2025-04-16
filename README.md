
# Flask REST API for Users, Departments, Posts, and Comments

This project is a RESTful API built using **Flask** and **PostgreSQL**, supporting CRUD operations for:

- Users
- Departments
- Posts
- Comments

Each module has full CRUD support. Users can be assigned to departments. Posts are created by users and can have multiple comments.

---

##  Getting Started

###  Prerequisites

- Python 3.9+
- PostgreSQL
- pip

### 🔧 Project Structure

```
project/
│
├── app.py
├── config/
│   └── database.py
├── controllers/
│   ├── users/
│   ├── departments/
│   ├── posts/
│   └── comments/
├── routes/
│   └── routes.py
├── utils.py
└── requirements.txt
```

---

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/mariamloutfy/userManagement
   ```
`

2. Configure database connection in `config/database.py`:
   ```python
   DB_NAME = "userdb"
   DB_USER = "myuser"
   DB_PASSWORD = "mypassword"
   DB_HOST = "localhost"
   ```

3. Run the app:
   ```bash
   python app.py
   ```

---

## 🧾 Database Tables

### `users`

| Column       | Type      |
|--------------|-----------|
| id           | SERIAL PK |
| username     | TEXT      |
| email        | TEXT      |
| password     | TEXT      |
| phone        | TEXT      |
| department_id| INTEGER FK|

### `departments`

| Column       | Type      |
|--------------|-----------|
| id           | SERIAL PK |
| departmentname| TEXT     |
| isactive     | BOOLEAN   |

### `posts`

| Column       | Type      |
|--------------|-----------|
| id           | SERIAL PK |
| title        | TEXT      |
| description  | TEXT      |
| created_by   | INTEGER FK (user_id) |
| created_at   | TIMESTAMP |

### `comments`

| Column       | Type      |
|--------------|-----------|
| id           | SERIAL PK |
| comment      | TEXT      |
| created_at   | TIMESTAMP |
| created_by   | INTEGER FK (user_id) |
| post_id      | INTEGER FK |

---

## API Endpoints

### Auth
- `POST /login` – User login

### Users
- `POST /users` – Create user
- `GET /users` – List all users
- `GET /users/<id>` – Get user by ID
- `PUT /users/<id>` – Update user
- `DELETE /users/<id>` – Delete user
- `PUT /users/<id>/assign_department` – Assign user to department

### Departments
- `POST /departments` – Create department
- `GET /departments` – List all departments
- `GET /departments/<id>` – Get department by ID
- `PUT /departments/<id>` – Update department
- `DELETE /departments/<id>` – Delete department

### Posts
- `POST /posts` – Create post
- `GET /posts` – List all posts with author info and comment count
- `GET /posts/<id>` – Get post details + author + comments
- `PUT /posts/<id>` – Update post
- `DELETE /posts/<id>` – Delete post

### Comments
- `POST /comments` – Create comment
- `GET /comments` – List all comments
- `GET /comments/<id>` – Get comment by ID
- `PUT /comments/<id>` – Update comment
- `DELETE /comments/<id>` – Delete comment

---

## Sample POSTMAN Test

To create a user:

**POST** `/users`
```json
{
  "username": "ahmed",
  "email": "ahmed@email.com",
  "password": "securepass123",
  "phone": "0123456789",
  "department_id": 1
}
```

To create a post:

**POST** `/posts`
```json
{
  "title": "New Feature",
  "description": "We’ve launched a new feature!",
  "created_by": 1
}
```

---

## Security Notes

- Passwords are hashed using `werkzeug.security`.
- Input validation is applied for required fields.
- SQL statements use parameterized queries to prevent SQL injection.

---

## Author

Mariam Loutfy

---

## License


