import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authAPI } from '../services/api'
import { Activity } from 'lucide-react'

const LoginPage = ({ setIsAuthenticated }) => {
  const [formData, setFormData] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const params = new URLSearchParams()
      params.append('username', formData.username)
      params.append('password', formData.password)

      const response = await authAPI.login(params)
      localStorage.setItem('token', response.data.access_token)
      setIsAuthenticated(true)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Activity className="w-16 h-16 text-primary-600" />
          </div>
          <h1 className="text-3xl font-bold text-slate-900">Welcome Back</h1>
          <p className="text-slate-600 mt-2">Sign in to continue your fitness journey</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Username
            </label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              className="input-field"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Password
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="input-field"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary py-3 text-lg disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="text-center mt-6 text-slate-600">
          Don't have an account?{' '}
          <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}

export default LoginPage
