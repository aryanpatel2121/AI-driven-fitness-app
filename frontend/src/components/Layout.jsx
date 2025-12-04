import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { Activity, Dumbbell, Apple, BarChart3, User, LogOut } from 'lucide-react'

const Layout = ({ setIsAuthenticated }) => {
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    setIsAuthenticated(false)
    navigate('/login')
  }

  const navItems = [
    { path: '/dashboard', icon: Activity, label: 'Dashboard' },
    { path: '/workouts', icon: Dumbbell, label: 'Workouts' },
    { path: '/nutrition', icon: Apple, label: 'Nutrition' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/profile', icon: User, label: 'Profile' },
  ]

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-white border-r border-slate-200 shadow-sm">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-primary-600 flex items-center gap-2">
            <Activity className="w-8 h-8" />
            FitTracker
          </h1>
        </div>

        <nav className="px-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                <Icon className="w-5 h-5" />
                {item.label}
              </Link>
            )
          })}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full text-slate-600 hover:bg-red-50 hover:text-red-600 rounded-lg transition-all"
          >
            <LogOut className="w-5 h-5" />
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-8">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
