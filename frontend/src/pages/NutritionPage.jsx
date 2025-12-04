import { useState, useEffect } from 'react'
import { Plus, Trash2, Apple, Sparkles, Loader2 } from 'lucide-react'
import { nutritionAPI, predictionAPI } from '../services/api'

const NutritionPage = () => {
  const [logs, setLogs] = useState([])
  const [dailySummary, setDailySummary] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [predicting, setPredicting] = useState(false)
  const [formData, setFormData] = useState({
    meal_type: 'breakfast',
    food_name: '',
    calories: '',
    protein: '',
    carbs: '',
    fats: '',
    serving_size: '',
    log_date: new Date().toISOString().split('T')[0]
  })

  useEffect(() => {
    fetchNutritionData()
  }, [])

  const fetchNutritionData = async () => {
    try {
      const [logsRes, summaryRes] = await Promise.all([
        nutritionAPI.getAll({ days: 7 }),
        nutritionAPI.getDailySummary()
      ])
      setLogs(logsRes.data)
      setDailySummary(summaryRes.data)
    } catch (error) {
      console.error('Error fetching nutrition data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePredict = async () => {
    if (!formData.food_name) return
    
    setPredicting(true)
    try {
      const response = await predictionAPI.getNutrition(formData.food_name)
      const data = response.data
      setFormData(prev => ({
        ...prev,
        calories: data.calories || prev.calories,
        protein: data.protein || prev.protein,
        carbs: data.carbs || prev.carbs,
        fats: data.fats || prev.fats,
        serving_size: data.serving_size || prev.serving_size
      }))
    } catch (error) {
      console.error('Error predicting nutrition:', error)
      alert(error.response?.data?.detail || 'Failed to predict nutrition. Please try again.')
    } finally {
      setPredicting(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const calories = parseFloat(formData.calories)
    if (isNaN(calories)) {
      alert("Please enter a valid number for calories")
      return
    }

    try {
      await nutritionAPI.create({
        ...formData,
        calories: calories,
        protein: formData.protein ? parseFloat(formData.protein) : null,
        carbs: formData.carbs ? parseFloat(formData.carbs) : null,
        fats: formData.fats ? parseFloat(formData.fats) : null,
        log_date: new Date(formData.log_date).toISOString()
      })
      setShowForm(false)
      setFormData({ 
        meal_type: 'breakfast', 
        food_name: '', 
        calories: '', 
        protein: '', 
        carbs: '', 
        fats: '', 
        serving_size: '',
        log_date: new Date().toISOString().split('T')[0]
      })
      fetchNutritionData()
    } catch (error) {
      console.error('Error creating nutrition log:', error)
      alert(error.response?.data?.detail || "Failed to save log. Please check your input.")
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this log?')) {
      try {
        await nutritionAPI.delete(id)
        fetchNutritionData()
      } catch (error) {
        console.error('Error deleting nutrition log:', error)
      }
    }
  }

  if (loading) {
    return <div className="flex justify-center py-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Nutrition</h1>
          <p className="text-slate-600 mt-1">Track your daily nutrition and macros</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Log Food
        </button>
      </div>

      {/* Daily Summary */}
      {dailySummary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-orange-500 to-orange-700 text-white rounded-xl p-6">
            <p className="text-white/80 text-sm">Total Calories</p>
            <p className="text-3xl font-bold mt-1">{Math.round(dailySummary.total_calories)}</p>
            <p className="text-white/80 text-xs mt-1">Today</p>
          </div>
          <div className="bg-gradient-to-br from-blue-500 to-blue-700 text-white rounded-xl p-6">
            <p className="text-white/80 text-sm">Protein</p>
            <p className="text-3xl font-bold mt-1">{Math.round(dailySummary.total_protein)}g</p>
          </div>
          <div className="bg-gradient-to-br from-green-500 to-green-700 text-white rounded-xl p-6">
            <p className="text-white/80 text-sm">Carbs</p>
            <p className="text-3xl font-bold mt-1">{Math.round(dailySummary.total_carbs)}g</p>
          </div>
          <div className="bg-gradient-to-br from-purple-500 to-purple-700 text-white rounded-xl p-6">
            <p className="text-white/80 text-sm">Fats</p>
            <p className="text-3xl font-bold mt-1">{Math.round(dailySummary.total_fats)}g</p>
          </div>
        </div>
      )}

      {showForm && (
        <div className="card">
          <h2 className="text-xl font-bold text-slate-900 mb-4">Log Food</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Date *</label>
                <input 
                  type="date" 
                  value={formData.log_date} 
                  onChange={(e) => setFormData({ ...formData, log_date: e.target.value })} 
                  className="input-field" 
                  required 
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Meal Type *</label>
                <select value={formData.meal_type} onChange={(e) => setFormData({ ...formData, meal_type: e.target.value })} className="input-field">
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="dinner">Dinner</option>
                  <option value="snack">Snack</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Food Name *</label>
              <div className="flex gap-2">
                <input 
                  type="text" 
                  value={formData.food_name} 
                  onChange={(e) => setFormData({ ...formData, food_name: e.target.value })} 
                  className="input-field flex-1" 
                  placeholder="e.g., 2 eggs and toast"
                  required 
                />
                <button 
                  type="button" 
                  onClick={handlePredict}
                  disabled={!formData.food_name || predicting}
                  className="px-4 py-2 bg-purple-100 text-purple-700 rounded-xl font-medium hover:bg-purple-200 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {predicting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
                  Predict
                </button>
              </div>
            </div>
            <div className="grid grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Calories *</label>
                <input type="number" value={formData.calories} onChange={(e) => setFormData({ ...formData, calories: e.target.value })} className="input-field" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Protein (g)</label>
                <input type="number" step="0.1" value={formData.protein} onChange={(e) => setFormData({ ...formData, protein: e.target.value })} className="input-field" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Carbs (g)</label>
                <input type="number" step="0.1" value={formData.carbs} onChange={(e) => setFormData({ ...formData, carbs: e.target.value })} className="input-field" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Fats (g)</label>
                <input type="number" step="0.1" value={formData.fats} onChange={(e) => setFormData({ ...formData, fats: e.target.value })} className="input-field" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Serving Size</label>
              <input type="text" value={formData.serving_size} onChange={(e) => setFormData({ ...formData, serving_size: e.target.value })} className="input-field" placeholder="e.g., 1 cup, 100g" />
            </div>
            <div className="flex gap-3">
              <button type="submit" className="btn-primary">Save Log</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      {/* Nutrition Logs */}
      <div className="card">
        <h2 className="text-xl font-bold text-slate-900 mb-4">Recent Logs (Last 7 Days)</h2>
        {logs.length === 0 ? (
          <div className="text-center py-12">
            <Apple className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-500">No nutrition logs yet. Start tracking your meals!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {logs.map((log) => (
              <div key={log.id} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <span className="px-3 py-1 bg-primary-100 text-primary-700 text-xs font-medium rounded-full">{log.meal_type}</span>
                    <h3 className="font-semibold text-slate-900">{log.food_name}</h3>
                    <span className="text-xs text-slate-500 bg-slate-200 px-2 py-0.5 rounded">
                      {new Date(log.log_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
                    </span>
                  </div>
                  <div className="flex gap-4 mt-2 text-sm text-slate-600">
                    <span>{log.calories} cal</span>
                    {log.protein && <span>P: {log.protein}g</span>}
                    {log.carbs && <span>C: {log.carbs}g</span>}
                    {log.fats && <span>F: {log.fats}g</span>}
                  </div>
                  <p className="text-xs text-slate-400 mt-1">Added: {new Date(log.created_at).toLocaleString()}</p>
                </div>
                <button onClick={() => handleDelete(log.id)} className="text-red-500 hover:text-red-700 ml-4">
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default NutritionPage
