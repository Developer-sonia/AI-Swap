# AI-Swap Deployment Guide for Render.com

## Quick Deploy

1. **Fork or clone this repository** to your GitHub account

2. **Connect to Render.com**:
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" and select "Web Service"

3. **Configure the service**:
   - **Name**: `ai-swap-backend` (or any name you prefer)
   - **Repository**: Select your forked repository
   - **Branch**: `main` (or your default branch)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn wsgi:app`

4. **Environment Variables** (if needed):
   - Add any required environment variables from `backend/env.example`

5. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

## Manual Deploy (Alternative)

If you prefer manual configuration:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use these settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn wsgi:app`
   - **Plan**: Free

## Important Notes

- The free plan has limitations on build time and monthly usage
- Your API will be available at: `https://your-app-name.onrender.com`
- API documentation: `https://your-app-name.onrender.com/docs`
- The frontend can be deployed separately as a Static Site if needed

## Troubleshooting

- Check the build logs if deployment fails
- Ensure all dependencies are in `backend/requirements.txt`
- Verify the `wsgi.py` file exists in the backend directory
- Make sure your code doesn't have any Windows-specific paths or commands 