<div align="center">

# 🏋️ Data-Driven Fitness Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node](https://img.shields.io/badge/Node-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00C853.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/)

**A modern, full-stack fitness tracking application with advanced analytics and machine learning capabilities.**

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## ✨ Features

### 🎯 Core Functionality
- **User Authentication** - Secure registration and login with JWT
- **Workout Tracking** - Log exercises, sets, reps, and weights
- **Nutrition Tracking** - Track calories and macronutrients
- **Progress Visualization** - Beautiful charts and graphs with Recharts
- **Profile Management** - Customize your fitness profile and goals

### 🤖 AI & Analytics
- **ML Predictions** - Performance forecasting using scikit-learn
- **Data Analytics** - Advanced insights powered by Pandas
- **Progress Trends** - Identify patterns in your fitness journey
- **Smart Recommendations** - Personalized workout and nutrition suggestions

### 💎 User Experience
- **Modern UI** - Clean, responsive design with Tailwind CSS
- **Real-time Updates** - Instant feedback on your activities
- **Mobile Responsive** - Works seamlessly on all devices
- **Dark Mode** - Easy on the eyes (coming soon)

---

## 🖼️ Demo

> Add screenshots of your application here

---

## 🏗️ Tech Stack

<table>
<tr>
<td valign="top" width="50%">

### Frontend
- **React 18.2** - Modern UI framework
- **Vite** - Lightning-fast build tool
- **React Router 6** - Client-side routing
- **Recharts 2.15** - Data visualization
- **Tailwind CSS 3.3** - Utility-first CSS
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client

</td>
<td valign="top" width="50%">

### Backend
- **FastAPI 0.104** - High-performance Python API
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Pydantic 2.5** - Data validation
- **Pandas 2.1** - Data analysis
- **scikit-learn 1.3** - Machine learning
- **python-jose** - JWT authentication

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.9+ ([Download](https://www.python.org/downloads/))

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/fitness-frontend-modern.git
cd fitness-frontend-modern
```

### 2️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database (SQLite - no setup needed!)
python init_db.py

# Start the backend server
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

### 3️⃣ Frontend Setup

Open a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4️⃣ Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Backend ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
fitness-frontend-modern/
│
├── frontend/                      # React frontend application
│   ├── public/                    # Static assets
│   ├── src/
│   │   ├── components/            # Reusable React components
│   │   │   ├── Dashboard/         # Dashboard widgets
│   │   │   ├── Workouts/          # Workout components
│   │   │   ├── Nutrition/         # Nutrition components
│   │   │   ├── Analytics/         # Analytics/charts
│   │   │   └── Profile/           # Profile components
│   │   ├── pages/                 # Page-level components
│   │   ├── services/              # API service layer
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── utils/                 # Helper functions
│   │   ├── App.jsx                # Root component
│   │   └── main.jsx               # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── backend/                       # FastAPI backend application
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/            # API endpoint routes
│   │   │       ├── auth.py        # Authentication endpoints
│   │   │       ├── workouts.py    # Workout endpoints
│   │   │       ├── nutrition.py   # Nutrition endpoints
│   │   │       ├── analytics.py   # Analytics endpoints
│   │   │       └── prediction.py  # ML prediction endpoints
│   │   ├── core/                  # Core configuration
│   │   │   ├── config.py          # App settings
│   │   │   └── security.py        # Security utilities
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # Business logic
│   │   │   ├── ai_service.py      # ML service
│   │   │   └── analytics_service.py
│   │   └── main.py                # FastAPI app entry
│   ├── init_db.py                 # Database initialization
│   ├── requirements.txt
│   └── .env.example
│
└── database/                      # Database files
    └── schema.sql                 # Database schema
```

---

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Workouts
- `GET /api/workouts` - Get all workouts for logged-in user
- `POST /api/workouts` - Create a new workout
- `GET /api/workouts/{id}` - Get specific workout
- `PUT /api/workouts/{id}` - Update workout
- `DELETE /api/workouts/{id}` - Delete workout

### Nutrition
- `GET /api/nutrition` - Get nutrition logs
- `POST /api/nutrition` - Log nutrition
- `GET /api/nutrition/{id}` - Get specific nutrition log
- `DELETE /api/nutrition/{id}` - Delete nutrition log

### Analytics
- `GET /api/analytics/progress` - Get progress analytics
- `GET /api/analytics/summary` - Get summary statistics

### Predictions (ML)
- `POST /api/predictions/workout-performance` - Predict workout performance
- `POST /api/predictions/goal-timeline` - Predict goal achievement

📖 **Full API Documentation**: Visit `http://localhost:8000/docs` when running the backend

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage  # With coverage
```

---

## 🛠️ Development

### Environment Variables

Backend `.env` file:
```env
# Application
APP_NAME=Fitness Tracker
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database (SQLite)
DATABASE_URL=sqlite:///./fitness_tracker.db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Code Style

```bash
# Frontend linting
cd frontend
npm run lint

# Backend linting
cd backend
pylint app/
```

---

## 🚢 Deployment

### Frontend (Vercel/Netlify)

```bash
cd frontend
npm run build
# Deploy the dist/ folder
```

### Backend (Railway/Render/Heroku)

```bash
cd backend
# Set environment variables on your platform
# Deploy with uvicorn app.main:app
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** for the amazing Python web framework
- **React** team for the incredible UI library
- **Recharts** for beautiful data visualizations
- **Tailwind CSS** for the utility-first CSS framework

---

## 📧 Contact

Have questions or suggestions? Feel free to [open an issue](https://github.com/yourusername/fitness-frontend-modern/issues)!

---

<div align="center">

**Made with ❤️ by fitness enthusiasts, for fitness enthusiasts**

⭐ Star this repo if you find it helpful!

</div>
