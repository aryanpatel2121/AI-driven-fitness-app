import { useState, useEffect } from 'react'
import { Plus, Trash2, Dumbbell, Sparkles, Loader2 } from 'lucide-react'
import { workoutsAPI, predictionAPI } from '../services/api'

const WorkoutsPage = () => {
  const [workouts, setWorkouts] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [predicting, setPredicting] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    workout_type: 'strength',
    duration: '',
    calories_burned: '',
    notes: '',
    exercises: [],
    log_date: new Date().toISOString().split('T')[0]
  })

  useEffect(() => {
    fetchWorkouts()
  }, [])

  const fetchWorkouts = async () => {
    try {
      const response = await workoutsAPI.getAll()
      setWorkouts(response.data)
    } catch (error) {
      console.error('Error fetching workouts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePredict = async () => {
    if (!formData.name || !formData.duration) return
    
    setPredicting(true)
    try {
      const response = await predictionAPI.getWorkoutCalories(formData.name, parseInt(formData.duration))
      const data = response.data
      setFormData(prev => ({
        ...prev,
        calories_burned: data.calories_burned || prev.calories_burned
      }))
    } catch (error) {
      console.error('Error predicting workout:', error)
      alert(error.response?.data?.detail || 'Failed to predict calories. Please try again.')
    } finally {
      setPredicting(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await workoutsAPI.create({
        ...formData,
        duration: formData.duration ? parseInt(formData.duration) : null,
        calories_burned: formData.calories_burned ? parseFloat(formData.calories_burned) : null,
        log_date: new Date(formData.log_date).toISOString()
      })
      setShowForm(false)
      setFormData({ 
        name: '', 
        workout_type: 'strength', 
        duration: '', 
        calories_burned: '', 
        notes: '', 
        exercises: [],
        log_date: new Date().toISOString().split('T')[0]
      })
      fetchWorkouts()
    } catch (error) {
      console.error('Error creating workout:', error)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this workout?')) {
      try {
        await workoutsAPI.delete(id)
        fetchWorkouts()
      } catch (error) {
        console.error('Error deleting workout:', error)
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
          <h1 className="text-3xl font-bold text-slate-900">Workouts</h1>
          <p className="text-slate-600 mt-1">Track and manage your workout sessions</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Workout
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2 className="text-xl font-bold text-slate-900 mb-4">New Workout</h2>
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
                <label className="block text-sm font-medium text-slate-700 mb-2">Workout Name *</label>
                <input type="text" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="input-field" required />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Type *</label>
                <select value={formData.workout_type} onChange={(e) => setFormData({ ...formData, workout_type: e.target.value })} className="input-field">
                  <option value="strength">Strength</option>
                  <option value="cardio">Cardio</option>
                  <option value="flexibility">Flexibility</option>
                  <option value="sports">Sports</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Duration (minutes)</label>
                <input type="number" value={formData.duration} onChange={(e) => setFormData({ ...formData, duration: e.target.value })} className="input-field" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Calories Burned</label>
              <div className="flex gap-2">
                <input 
                  type="number" 
                  value={formData.calories_burned} 
                  onChange={(e) => setFormData({ ...formData, calories_burned: e.target.value })} 
                  className="input-field flex-1" 
                />
                <button 
                  type="button" 
                  onClick={handlePredict}
                  disabled={!formData.name || !formData.duration || predicting}
                  className="px-4 py-2 bg-purple-100 text-purple-700 rounded-xl font-medium hover:bg-purple-200 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {predicting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
                  Predict
                </button>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Notes</label>
              <textarea value={formData.notes} onChange={(e) => setFormData({ ...formData, notes: e.target.value })} className="input-field" rows="3"></textarea>
            </div>
            <div className="flex gap-3">
              <button type="submit" className="btn-primary">Save Workout</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {workouts.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <Dumbbell className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-500">No workouts yet. Add your first workout!</p>
          </div>
        ) : (
          workouts.map((workout) => (
            <div key={workout.id} className="card hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-bold text-slate-900">{workout.name}</h3>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 bg-slate-200 px-2 py-0.5 rounded">
                    {new Date(workout.log_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
                  </span>
                  <button onClick={() => handleDelete(workout.id)} className="text-red-500 hover:text-red-700">
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-slate-600"><span className="font-medium">Type:</span> {workout.workout_type}</p>
                {workout.duration && <p className="text-sm text-slate-600"><span className="font-medium">Duration:</span> {workout.duration} min</p>}
                {workout.calories_burned && <p className="text-sm text-slate-600"><span className="font-medium">Calories:</span> {workout.calories_burned}</p>}
                {workout.notes && <p className="text-sm text-slate-600 mt-2">{workout.notes}</p>}
                <p className="text-xs text-slate-400 mt-3">Added: {new Date(workout.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default WorkoutsPage
