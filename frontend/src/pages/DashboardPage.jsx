import { useState, useEffect } from 'react'
import { Activity, TrendingUp, Flame, Target } from 'lucide-react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { analyticsAPI, mlAPI } from '../services/api'

const DashboardPage = () => {
  const [stats, setStats] = useState(null)
  const [progress, setProgress] = useState(null)
  const [insights, setInsights] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [statsRes, progressRes, insightsRes] = await Promise.all([
        analyticsAPI.getStatistics(),
        analyticsAPI.getProgress(30),
        mlAPI.getInsights()
      ])

      setStats(statsRes.data)
      setProgress(progressRes.data)
      setInsights(insightsRes.data.insights || [])
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-600 mt-1">Welcome back! Here's your fitness overview.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-indigo-500 to-indigo-700 text-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm">Total Workouts</p>
              <p className="text-3xl font-bold mt-1">{stats?.totals?.workouts || 0}</p>
            </div>
            <Activity className="w-12 h-12 text-white/50" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-700 text-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm">Recent Activity</p>
              <p className="text-3xl font-bold mt-1">{stats?.recent_activity?.workouts_last_7_days || 0}</p>
              <p className="text-white/80 text-xs mt-1">Last 7 days</p>
            </div>
            <TrendingUp className="w-12 h-12 text-white/50" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-700 text-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm">Nutrition Logs</p>
              <p className="text-3xl font-bold mt-1">{stats?.totals?.nutrition_logs || 0}</p>
            </div>
            <Flame className="w-12 h-12 text-white/50" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-700 text-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm">Member Since</p>
              <p className="text-lg font-bold mt-1">{stats?.user_info?.member_since || 'N/A'}</p>
            </div>
            <Target className="w-12 h-12 text-white/50" />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Workout Progress */}
        <div className="card">
          <h2 className="text-xl font-bold text-slate-900 mb-4">Workout Progress (30 Days)</h2>
          {progress?.workouts?.daily_data?.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={progress.workouts.daily_data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="duration" stroke="#0ea5e9" name="Duration (min)" />
                <Line type="monotone" dataKey="calories_burned" stroke="#10b981" name="Calories" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-slate-500 text-center py-12">No workout data available</p>
          )}
        </div>

        {/* Workout Type Distribution */}
        <div className="card">
          <h2 className="text-xl font-bold text-slate-900 mb-4">Workout Types</h2>
          {progress?.workouts?.type_distribution && Object.keys(progress.workouts.type_distribution).length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={Object.entries(progress.workouts.type_distribution).map(([key, value]) => ({ type: key, count: value }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="type" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#0ea5e9" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-slate-500 text-center py-12">No workout type data available</p>
          )}
        </div>
      </div>

      {/* ML Insights */}
      {insights.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold text-slate-900 mb-4">AI Insights</h2>
          <div className="space-y-3">
            {insights.map((insight, index) => (
              <div key={index} className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                <p className="text-slate-900 font-medium">{insight.message}</p>
                {insight.data && (
                  <p className="text-slate-600 text-sm mt-1">
                    {JSON.stringify(insight.data)}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default DashboardPage
