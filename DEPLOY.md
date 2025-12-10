# Quick Deployment Checklist

## ✅ Ready for GitHub
```bash
git push origin main
```

## ✅ Ready for Render

### Step 1: Create Web Service
- Go to Render Dashboard → New Web Service
- Connect GitHub repo: `AI-driven-fitness-app`
- Root Directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 2: Environment Variables (REQUIRED)

Get Firebase JSON:
```bash
cat backend/ai-fitness-tracker-3fef5-firebase-adminsdk-fbsvc-de7ee9a3e6.json
```

Add in Render → Environment:
```
SECRET_KEY=your-random-secret-key-here-change-this
FIREBASE_CREDENTIALS_JSON=<paste entire JSON output from above>
BACKEND_CORS_ORIGINS=["https://yourfrontend.netlify.app"]
```

Optional (if you have them):
```
GOOGLE_API_KEY=your_key
CALORIENINJAS_API_KEY=your_key
```

### Step 3: Deploy
Click "Create Web Service" - Done!

## Frontend Update
Update frontend `.env`:
```
VITE_API_URL=https://your-render-url.onrender.com
```

## Verify
```bash
curl https://your-render-url.onrender.com/health
```
Should return: `{"status":"healthy"}`

---

**Note**: Firebase credentials are NOT in Git (protected by .gitignore) ✅
