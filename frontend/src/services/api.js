import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  getCurrentUser: () => api.get('/auth/me'),
  updateProfile: (userData) => api.put('/auth/me', userData),
}

// Workouts API
export const workoutsAPI = {
  getAll: (params) => api.get('/workouts', { params }),
  getById: (id) => api.get(`/workouts/${id}`),
  create: (workout) => api.post('/workouts', workout),
  delete: (id) => api.delete(`/workouts/${id}`),
}

// Nutrition API
export const nutritionAPI = {
  getAll: (params) => api.get('/nutrition', { params }),
  create: (nutrition) => api.post('/nutrition', nutrition),
  getDailySummary: (date) => api.get(`/nutrition/daily-summary${date ? `?date=${date}` : ''}`),
  delete: (id) => api.delete(`/nutrition/${id}`)
}

export const predictionAPI = {
  getNutrition: (query) => api.post('/prediction/nutrition', { query }),
  getWorkoutCalories: (activity, duration) => api.post('/prediction/workout', { activity, duration })
}

// Analytics API
export const analyticsAPI = {
  getProgress: (days = 30) => api.get('/analytics/progress', { params: { days } }),
  getTrends: (metric, days = 30) => api.get('/analytics/trends', { params: { metric, days } }),
  getStatistics: () => api.get('/analytics/statistics'),
}

// ML Predictions API
export const mlAPI = {
  predictPerformance: (workoutType, daysAhead = 7) => 
    api.get('/ml/predict-performance', { params: { workout_type: workoutType, days_ahead: daysAhead } }),
  recommendGoals: () => api.get('/ml/recommend-goals'),
  getInsights: () => api.get('/ml/workout-insights'),
}

export default api
