Pharmacy Management System
Student: Noor Fatima  ID: F2024408054  
Course: open source
Tech Stack: FastAPI + PostgreSQL (Supabase) + HTML/CSS/JS

A full-stack web application for managing pharmacy operations: medicines, customers, sales, prescriptions, and dashboard statistics.



 Project Structure


Pharmacy-Management-System
frontend
   index.html           Home page
    about.html          About page
    login.html           Login / Register
    dashboard.html       Dashboard with stats
    medicines.html       Medicine CRUD + search
    customers.html       Customer CRUD
    sales.html           Sales & billing
    prescriptions.html   Prescription management
    style.css            Shared styles
    api.js               API helper functions
backend
    main.py              FastAPI app (25 endpoints)
    models.py            Database models
    schemas.py           Request/response schemas
    database.py          Database connection
    auth.py              JWT authentication
    schema.sql           SQL for Supabase
    requirements.txt     Python packages
    .env.example         Environment variables template
 README.md






API docs: `http://127.0.0.1:8000/docs`

---

## Setup Instructions (Local)

### Step 1: Create Supabase Database

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Open **SQL Editor** and paste the contents of `backend/schema.sql`
4. Click **Run** to create tables and sample data
5. Go to **Project Settings → Database** and copy the **Connection string (URI)**
6. Replace `[YOUR-PASSWORD]` with your database password

### Step 2: Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file (copy from `.env.example`):

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxx.supabase.co:5432/postgres
SECRET_KEY=my-super-secret-key-123
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### Step 3: Run Frontend

Open `frontend/index.html` in your browser, or use Live Server extension in VS Code.

**Important:** For the frontend to talk to the backend, either:
- Open frontend through a local server (Live Server), OR
- Update `API_URL` in `frontend/api.js` if needed

### Step 4: Test the System

1. Open `login.html` and **Register** a new account
2. Login and go to **Dashboard** to see statistics
3. Add medicines, customers, sales, and prescriptions
4. Test search and filter on the medicines page

---

## Deployment

### Backend → Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo, set root directory to `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables: `DATABASE_URL` and `SECRET_KEY`

### Frontend → Vercel / Netlify

1. Push `frontend/` folder to GitHub
2. Deploy on [vercel.com](https://vercel.com) or [netlify.com](https://netlify.com)
3. Update `API_URL` in `frontend/api.js` to your Render backend URL

Database → Supabase

Already hosted on Supabase (free tier).

