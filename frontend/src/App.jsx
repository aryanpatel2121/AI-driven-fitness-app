import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import DashboardPage from './pages/DashboardPage'
import WorkoutsPage from './pages/WorkoutsPage'
import NutritionPage from './pages/NutritionPage'
import AnalyticsPage from './pages/AnalyticsPage'
import ProfilePage from './pages/ProfilePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import Layout from './components/Layout'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token')
    if (token) {
      setIsAuthenticated(true)
    }
    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={
          isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />
        } />
        <Route path="/register" element={
          isAuthenticated ? <Navigate to="/dashboard" /> : <RegisterPage setIsAuthenticated={setIsAuthenticated} />
        } />
        
        <Route path="/" element={
          isAuthenticated ? <Layout setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/login" />
        }>
          <Route index element={<Navigate to="/dashboard" />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="workouts" element={<WorkoutsPage />} />
          <Route path="nutrition" element={<NutritionPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
