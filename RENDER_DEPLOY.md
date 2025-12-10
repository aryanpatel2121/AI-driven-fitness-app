# Render Deployment Guide

## Quick Setup (3 steps)

### 1. Push to GitHub

```bash
git add .
git commit -m "Add Firebase database"
git push origin main
```

### 2. Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-fitness-tracker-backend`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Add Environment Variables

In Render Dashboard → Environment tab, add these variables:

#### Required:
```
SECRET_KEY=your-random-secret-key-here
FIREBASE_CREDENTIALS_JSON=<paste entire JSON from your firebase credentials file>
```

#### Optional (if you have them):
```
GOOGLE_API_KEY=your_google_api_key
CALORIENINJAS_API_KEY=your_api_key
BACKEND_CORS_ORIGINS=["https://yourapp.netlify.app","http://localhost:5173"]
```

## How to get FIREBASE_CREDENTIALS_JSON

Open your Firebase credentials file:
```bash
cat backend/ai-fitness-tracker-3fef5-firebase-adminsdk-fbsvc-de7ee9a3e6.json
```

Copy the ENTIRE JSON output (all in one line) and paste it as the value for `FIREBASE_CREDENTIALS_JSON`.

## Deploy

Click **"Create Web Service"** - Render will automatically deploy!

Your API will be available at: `https://your-service-name.onrender.com`

## Update Frontend

Update your frontend `.env` to point to the new backend:
```
VITE_API_URL=https://your-service-name.onrender.com
```

## Verify Deployment

Test the health endpoint:
```bash
curl https://your-service-name.onrender.com/health
```

Should return: `{"status":"healthy"}`

## Troubleshooting

- **"Firebase initialization failed"**: Check that `FIREBASE_CREDENTIALS_JSON` is set correctly
- **"SECRET_KEY not set"**: Add `SECRET_KEY` environment variable
- **CORS errors**: Update `BACKEND_CORS_ORIGINS` with your frontend URL
