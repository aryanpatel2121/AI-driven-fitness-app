# Firebase Setup Guide

This application uses Firebase Firestore as its database. Follow these steps to set up Firebase for your fitness tracker.

## Prerequisites

- A Google account
- Firebase project (free tier is sufficient for development)

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or select an existing project
3. Follow the setup wizard:
   - Enter a project name (e.g., "AI Fitness Tracker")
   - Accept the terms
   - Choose analytics settings (optional)
   - Click **"Create project"**

## Step 2: Enable Firestore Database

1. In your Firebase project, go to **Build** → **Firestore Database**
2. Click **"Create database"**
3. Choose **"Start in production mode"** (we'll set rules later)
4. Select a Firestore location (choose one closest to your users)
5. Click **"Enable"**

## Step 3: Generate Service Account Credentials

1. In Firebase Console, click the **gear icon** → **Project settings**
2. Go to the **"Service accounts"** tab
3. Click **"Generate new private key"**
4. A JSON file will be downloaded - **KEEP THIS SECURE!**
5. Rename the file to `firebase-credentials.json`

## Step 4: Configure Your Backend

### For Local Development:

1. Move `firebase-credentials.json` to your backend directory:
   ```bash
   mv ~/Downloads/your-project-xxxxx-firebase-adminsdk-xxxxx.json backend/firebase-credentials.json
   ```

2. Create a `.env` file in the `backend/` directory (copy from `.env.example`):
   ```bash
   cd backend
   cp .env.example .env
   ```

3. Update your `.env` file:
   ```env
   # Firebase Configuration
   FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

   # Security (generate a random secret key)
   GOOGLE_API_KEY=your_google_api_key_here
   SECRET_KEY=your-secret-key-here

   # API
   API_V1_PREFIX=/api/v1
   PROJECT_NAME=Fitness Tracker API

   # CORS
   BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
   ```

### For Production (Render.com):

1. Go to your Render dashboard → Your web service
2. Navigate to **"Environment"** tab
3. Add environment variable:
   - **Key**: `GOOGLE_APPLICATION_CREDENTIALS`
   - **Value**: Paste the **entire contents** of your `firebase-credentials.json` file as a JSON string

   Alternatively, you can upload the JSON file to Render and set the path:
   - Upload `firebase-credentials.json` to your repository (ensure it's in `.gitignore`)
   - Set `FIREBASE_CREDENTIALS_PATH` to the path where Render can access it

## Step 5: Set Firestore Security Rules (Optional but Recommended)

1. In Firebase Console, go to **Firestore Database** → **Rules**
2. Update the rules to:
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Allow read/write access only through Admin SDK (server-side)
       match /{document=**} {
         allow read, write: if false;
       }
     }
   }
   ```

This ensures all database access goes through your Backend (not directly from frontend), which is secured by your API authentication.

## Step 6: Install Dependencies and Run

1. Install the updated requirements:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. You should see:
   ```
   ✓ Firebase initialized successfully
   INFO:     Application startup complete.
   ```

## Firestore Collections Structure

Your data will be organized as follows:

- **users/** - User profiles and authentication
  - **{userId}/workouts/** - User's workout history
    - **{workoutId}/exercises/** - Exercises within a workout
  - **{userId}/nutrition_logs/** - User's nutrition entries
  - **{userId}/goals/** - User's fitness goals

## Troubleshooting

### Error: "Firebase credentials file not found"
- Check that `firebase-credentials.json` exists in your backend directory
- Verify the path in your `.env` file is correct

### Error: "Permission denied" in Firestore
- Verify your service account has the necessary permissions
- Check that Firestore is enabled in your Firebase project

### Error: "Module 'firebase_admin' not found"
- Run `pip install -r requirements.txt` again
- Make sure you're in your virtual environment

## Security Best Practices

⚠️ **IMPORTANT**: 
- **NEVER** commit `firebase-credentials.json` to Git
- Add it to `.gitignore` (already done in this project)
- For production, use environment variables or secure secret management
- Rotate your service account keys periodically

## Need Help?

- [Firebase Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Admin Python SDK](https://firebase.google.com/docs/reference/admin/python)
