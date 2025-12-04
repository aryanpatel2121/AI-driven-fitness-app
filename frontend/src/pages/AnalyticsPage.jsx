import { useState, useEffect } from 'react'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { analyticsAPI, mlAPI } from '../services/api'
import { TrendingUp, Brain, Target } from 'lucide-react'

const AnalyticsPage = () => {
  const [progress, setProgress] = useState(null)
  const [predictions, setPredictions] = useState(null)
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const [progressRes, predictionsRes, recommendationsRes] = await Promise.all([
        analyticsAPI.getProgress(30),
        mlAPI.predictPerformance('strength', 7).catch(() => null),
        mlAPI.recommendGoals().catch(() => null)
      ])

      setProgress(progressRes.data)
      setPredictions(predictionsRes?.data)
      setRecommendations(recommendationsRes?.data)
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="flex justify-center py-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Analytics & Insights</h1>
        <p className="text-slate-600 mt-1">Advanced analytics powered by machine learning</p>
      </div>

      {/* Nutrition Progress */}
      {progress?.nutrition?.daily_data?.length > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-bold text-slate-900">Nutrition Trends (30 Days)</h2>
          </div>
          <ResponsiveContainer width="100%" height={350}>
            <AreaChart data={progress.nutrition.daily_data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area type="monotone" dataKey="calories" stackId="1" stroke="#f59e0b" fill="#fbbf24" name="Calories" />
              <Area type="monotone" dataKey="protein" stackId="2" stroke="#0ea5e9" fill="#38bdf8" name="Protein (g)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* ML Predictions */}
      {predictions && !predictions.error && (
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <Brain className="w-6 h-6 text-purple-600" />
            <h2 className="text-xl font-bold text-slate-900">AI Performance Predictions</h2>
          </div>
          <p className="text-slate-600 mb-4">
            Based on {predictions.historical_workouts} historical {predictions.workout_type} workouts
          </p>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={predictions.predictions}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" label={{ value: 'Days Ahead', position: 'insideBottom', offset: -5 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="predicted_duration" stroke="#8b5cf6" name="Duration (min)" strokeWidth={2} />
              <Line type="monotone" dataKey="predicted_calories" stroke="#10b981" name="Calories" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-purple-50 rounded-lg">
            <p className="text-sm text-slate-700">
              <strong>Model Accuracy:</strong> Duration: {(predictions.model_info.duration_score * 100).toFixed(1)}%, 
              Calories: {(predictions.model_info.calories_score * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      )}

      {/* Goal Recommendations */}
      {recommendations && recommendations.recommendations?.length > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-6 h-6 text-green-600" />
            <h2 className="text-xl font-bold text-slate-900">AI Goal Recommendations</h2>
          </div>
          <p className="text-slate-600 mb-4">
            Based on {recommendations.total_workouts} workouts over the {recommendations.period_analyzed}
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recommendations.recommendations.map((rec, index) => (
              <div key={index} className="p-4 bg-gradient-to-br from-green-50 to-green-100 border border-green-200 rounded-lg">
                <h3 className="font-bold text-slate-900 mb-2 capitalize">{rec.goal_type.replace('_', ' ')}</h3>
                <div className="space-y-1 text-sm">
                  <p className="text-slate-700">
                    <span className="font-medium">Current:</span> {rec.current_average} {rec.unit}
                  </p>
                  <p className="text-green-700 font-semibold">
                    <span className="font-medium">Target:</span> {rec.recommended_target} {rec.unit}
                  </p>
                  <p className="text-slate-600 text-xs mt-2 italic">{rec.rationale}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Workout Progress Chart */}
      {progress?.workouts?.daily_data?.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold text-slate-900 mb-4">Workout Intensity Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={progress.workouts.daily_data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="duration" stroke="#0ea5e9" name="Duration (min)" strokeWidth={2} />
              <Line yAxisId="right" type="monotone" dataKey="calories_burned" stroke="#f59e0b" name="Calories" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

export default AnalyticsPage
