# 🚀 Deployment Guide

Your Slack2Spotify bot is ready to deploy! Here are the easiest options:

## Option 1: Railway (Recommended) ⭐

### Steps:
1. **Create GitHub repo** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/slack2spotify.git
   git push -u origin main
   ```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your `slack2spotify` repository
   - Railway will auto-deploy!

3. **Set Environment Variables**:
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add all your environment variables:
     ```
     SLACK_BOT_TOKEN=xoxb-your-token
     SLACK_SIGNING_SECRET=your-secret
     SPOTIFY_CLIENT_ID=your-client-id
     SPOTIFY_CLIENT_SECRET=your-client-secret
     SPOTIFY_REDIRECT_URI=https://your-railway-url.railway.app/callback
     SPOTIFY_PLAYLIST_ID=your-playlist-id
     PORT=3000
     ```

4. **Update Slack App**:
   - Get your Railway URL (e.g., `https://slack2spotify-production.up.railway.app`)
   - Update Slack Event Subscriptions URL to: `https://your-railway-url/slack/events`
   - Update Spotify redirect URI to: `https://your-railway-url/callback`

### ✅ Benefits:
- ✅ **Free tier**: 500 hours/month
- ✅ **Auto-deploys** from GitHub
- ✅ **Custom domains** available
- ✅ **Easy scaling**

---

## Option 2: Heroku

### Steps:
1. **Install Heroku CLI**: `brew install heroku/brew/heroku`

2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set SLACK_BOT_TOKEN=xoxb-your-token
   heroku config:set SLACK_SIGNING_SECRET=your-secret
   heroku config:set SPOTIFY_CLIENT_ID=your-client-id
   heroku config:set SPOTIFY_CLIENT_SECRET=your-client-secret
   heroku config:set SPOTIFY_REDIRECT_URI=https://your-app.herokuapp.com/callback
   heroku config:set SPOTIFY_PLAYLIST_ID=your-playlist-id
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

### ✅ Benefits:
- ✅ **Classic platform**
- ✅ **Great documentation**
- ✅ **Add-ons ecosystem**

---

## Option 3: DigitalOcean App Platform

### Steps:
1. **Go to** [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
2. **Create App** from GitHub repo
3. **Configure**:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Run command: `python main.py`
4. **Set environment variables** in the dashboard

### ✅ Benefits:
- ✅ **$200 free credit** for new users
- ✅ **Predictable pricing**
- ✅ **Good performance**

---

## Post-Deployment Checklist

After deploying to any platform:

### 1. Update Slack App Settings:
- **Event Subscriptions URL**: `https://your-domain.com/slack/events`
- **OAuth Redirect URLs**: Keep your original setup

### 2. Update Spotify App Settings:
- **Redirect URIs**: Add `https://your-domain.com/callback`

### 3. Test Your Deployed Bot:
- Share a YouTube URL in Slack
- Check if songs are added to your playlist
- Monitor logs in your hosting platform

### 4. Set Up Monitoring:
- Most platforms provide built-in logging
- Set up alerts for downtime
- Monitor usage and costs

---

## 🎯 Recommended: Railway

**Railway is the easiest option** - just push to GitHub and deploy with one click!

1. Push your code to GitHub
2. Connect Railway to your repo  
3. Set environment variables
4. Update Slack/Spotify URLs
5. Your bot is live! 🎵

---

## Environment Variables Reference

```env
SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
SLACK_SIGNING_SECRET=your-actual-signing-secret
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
SPOTIFY_REDIRECT_URI=https://your-domain.com/callback
SPOTIFY_PLAYLIST_ID=your-playlist-id
PORT=3000
DEBUG=false
```

Make sure to update the redirect URIs in both Slack and Spotify after deployment! 