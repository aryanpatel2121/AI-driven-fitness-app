# PostgreSQL Setup Guide for Render

Follow these steps to set up a persistent PostgreSQL database on Render.

## Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. Click **"New +"** button (top right)
3. Select **"PostgreSQL"**
4. Fill in the form:
   - **Name**: `fitness-tracker-db` (or any name you like)
   - **Database**: `fitness_db`
   - **User**: `fitness_user`
   - **Region**: Same as your backend service (e.g., Oregon)
   - **PostgreSQL Version**: Latest (15+)
   - **Plan**: **Free**
5. Click **"Create Database"**
6. Wait 1-2 minutes for creation to complete

## Step 2: Get Database Connection String

1. After creation, you'll see the database dashboard
2. Scroll down to **"Connections"** section
3. Copy the **"Internal Database URL"** (starts with `postgresql://`)
   - Example: `postgresql://fitness_user:abc123xyz@dpg-xxxxx.oregon-postgres.render.com/fitness_db`
   - ⚠️ **Use Internal URL, not External** (Internal is faster and free)

## Step 3: Add Database URL to Backend Service

1. Go back to Render Dashboard
2. Click on your **backend service** (web service)
3. Click **"Environment"** tab on the left
4. Find the `DATABASE_URL` variable (or add it if missing):
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL you copied
5. Click **"Save Changes"**

## Step 4: Redeploy Backend

Render will **automatically redeploy** after you save the environment variable.

Watch for these logs to confirm success:
```
✓ Installing dependencies...
✓ Database tables created/checked successfully.
✓ Raw BACKEND_CORS_ORIGINS from settings: ...
✓ Parsed CORS origins = ['https://ai-driven-fitness-app.netlify.app', ...]
```

## Step 5: Test Persistence

1. Go to your frontend: https://ai-driven-fitness-app.netlify.app
2. **Register a new account** (use fresh credentials)
3. **Log in** with that account
4. Add a nutrition log or workout
5. **Trigger a redeploy** (push any small change to GitHub)
6. After redeploy completes, **log in again** with the same credentials
7. ✅ **Expected**: Login succeeds, data is still there!

## Troubleshooting

### Database Connection Errors
- Make sure you copied the **Internal Database URL** (not External)
- Verify the URL is complete (starts with `postgresql://`)
- Check Render logs for specific error messages

### Login Still Fails After Setup
- Clear browser localStorage: `localStorage.clear()` in console
- Register a **new** account (old accounts from SQLite are gone)
- Verify database was created successfully in Render

### Free Database Expiration
- Render free PostgreSQL expires after **30 days**
- You'll get an email reminder before expiration
- To extend: Create a new free database and update DATABASE_URL
- Or upgrade to paid tier ($7/month) for permanent storage

## Alternative: External PostgreSQL (Neon)

If you want a truly permanent free database:

1. Go to https://neon.tech
2. Sign up for free account
3. Create a new project
4. Copy the connection string
5. Add to Render as `DATABASE_URL`
6. Neon's free tier has no 30-day limit!

## Next Steps

After successful setup:
- All user accounts will persist across deployments ✅
- All nutrition logs and workouts saved permanently ✅
- No more "user not found" errors ✅
- Database survives Render redeployments ✅
