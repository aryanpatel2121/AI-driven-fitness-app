import { useState, useEffect } from 'react'
import { User, Mail, Calendar, Weight, Ruler, Edit2, X, Save } from 'lucide-react'
import { authAPI } from '../services/api'

const ProfilePage = () => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    full_name: '',
    age: '',
    weight: '',
    height: '',
    gender: ''
  })

  useEffect(() => {
    fetchUserProfile()
  }, [])

  const fetchUserProfile = async () => {
    try {
      const response = await authAPI.getCurrentUser()
      setUser(response.data)
      // Initialize form with user data
      setFormData({
        full_name: response.data.full_name || '',
        age: response.data.age || '',
        weight: response.data.weight || '',
        height: response.data.height || '',
        gender: response.data.gender || ''
      })
    } catch (error) {
      console.error('Error fetching user profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = () => {
    setIsEditing(true)
  }

  const handleCancel = () => {
    setIsEditing(false)
    // Reset form to current user data
    setFormData({
      full_name: user.full_name || '',
      age: user.age || '',
      weight: user.weight || '',
      height: user.height || '',
      gender: user.gender || ''
    })
  }

  const handleSave = async () => {
    try {
      const updateData = {
        full_name: formData.full_name || null,
        age: formData.age ? parseInt(formData.age) : null,
        weight: formData.weight ? parseFloat(formData.weight) : null,
        height: formData.height ? parseFloat(formData.height) : null,
        gender: formData.gender || null
      }
      
      await authAPI.updateProfile(updateData)
      await fetchUserProfile()
      setIsEditing(false)
    } catch (error) {
      console.error('Error updating profile:', error)
      alert(error.response?.data?.detail || 'Failed to update profile')
    }
  }

  if (loading) {
    return <div className="flex justify-center py-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  }

  if (!user) {
    return <div className="text-center py-12 text-slate-500">Unable to load profile</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Profile</h1>
          <p className="text-slate-600 mt-1">Manage your account information</p>
        </div>
        {!isEditing && (
          <button onClick={handleEdit} className="btn-primary flex items-center gap-2">
            <Edit2 className="w-4 h-4" />
            Edit Profile
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="lg:col-span-1">
          <div className="card text-center">
            <div className="w-24 h-24 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-full mx-auto flex items-center justify-center mb-4">
              <User className="w-12 h-12 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900">{user.full_name || user.username}</h2>
            <p className="text-slate-600 mt-1">@{user.username}</p>
            <div className="mt-4 pt-4 border-t border-slate-200">
              <p className="text-sm text-slate-500">Member since</p>
              <p className="font-medium text-slate-900">{new Date(user.created_at).toLocaleDateString()}</p>
            </div>
          </div>
        </div>

        {/* Details Card */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-slate-900">Personal Information</h3>
              {isEditing && (
                <div className="flex gap-2">
                  <button onClick={handleSave} className="btn-primary flex items-center gap-2">
                    <Save className="w-4 h-4" />
                    Save
                  </button>
                  <button onClick={handleCancel} className="btn-secondary flex items-center gap-2">
                    <X className="w-4 h-4" />
                    Cancel
                  </button>
                </div>
              )}
            </div>

            {isEditing ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
                  <input
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                    className="input-field"
                    placeholder="Enter your full name"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Age</label>
                    <input
                      type="number"
                      value={formData.age}
                      onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                      className="input-field"
                      placeholder="Age"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Gender</label>
                    <select
                      value={formData.gender}
                      onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                      className="input-field"
                    >
                      <option value="">Select gender</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Weight (kg)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.weight}
                      onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
                      className="input-field"
                      placeholder="Weight in kg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Height (cm)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.height}
                      onChange={(e) => setFormData({ ...formData, height: e.target.value })}
                      className="input-field"
                      placeholder="Height in cm"
                    />
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                  <Mail className="w-5 h-5 text-indigo-600" />
                  <div>
                    <p className="text-sm text-slate-500">Email</p>
                    <p className="font-medium text-slate-900">{user.email}</p>
                  </div>
                </div>

                {user.age && (
                  <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                    <Calendar className="w-5 h-5 text-indigo-600" />
                    <div>
                      <p className="text-sm text-slate-500">Age</p>
                      <p className="font-medium text-slate-900">{user.age} years</p>
                    </div>
                  </div>
                )}

                {user.weight && (
                  <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                    <Weight className="w-5 h-5 text-indigo-600" />
                    <div>
                      <p className="text-sm text-slate-500">Weight</p>
                      <p className="font-medium text-slate-900">{user.weight} kg</p>
                    </div>
                  </div>
                )}

                {user.height && (
                  <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                    <Ruler className="w-5 h-5 text-indigo-600" />
                    <div>
                      <p className="text-sm text-slate-500">Height</p>
                      <p className="font-medium text-slate-900">{user.height} cm</p>
                    </div>
                  </div>
                )}

                {user.gender && (
                  <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                    <User className="w-5 h-5 text-indigo-600" />
                    <div>
                      <p className="text-sm text-slate-500">Gender</p>
                      <p className="font-medium text-slate-900 capitalize">{user.gender}</p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* BMI Calculation */}
            {user.weight && user.height && !isEditing && (
              <div className="mt-6 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
                <h4 className="font-bold text-slate-900 mb-2">Body Mass Index (BMI)</h4>
                <p className="text-3xl font-bold text-indigo-600">
                  {(user.weight / Math.pow(user.height / 100, 2)).toFixed(1)}
                </p>
                <p className="text-sm text-slate-600 mt-1">
                  {(() => {
                    const bmi = user.weight / Math.pow(user.height / 100, 2)
                    if (bmi < 18.5) return 'Underweight'
                    if (bmi < 25) return 'Normal weight'
                    if (bmi < 30) return 'Overweight'
                    return 'Obese'
                  })()}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
