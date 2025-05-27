# Slack2Spotify Bot 🎵

A Slack bot that automatically detects YouTube URLs in messages and adds the songs to a Spotify playlist.

## Features

- 🎯 Automatically detects YouTube URLs in Slack messages
- 🎵 Extracts song information from YouTube videos
- 🔍 Searches for songs on Spotify
- ➕ Adds found songs to a specified Spotify playlist
- 🤖 Provides feedback messages in Slack
- 🧵 Processes multiple URLs concurrently

## Prerequisites

1. **Slack App**: Create a Slack app with bot permissions
2. **Spotify App**: Create a Spotify application for API access
3. **Python 3.7+**: Make sure you have Python installed

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd slack2spotify
pip install -r requirements.txt
```

### 2. Create Slack App

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name your app and select your workspace
4. Navigate to "OAuth & Permissions"
5. Add these Bot Token Scopes:
   - `chat:write`
   - `channels:history`
   - `groups:history`
   - `im:history`
   - `mpim:history`
6. Install the app to your workspace
7. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

### 3. Configure Slack Event Subscriptions

1. In your Slack app settings, go to "Event Subscriptions"
2. Enable events and set Request URL to: `https://your-domain.com/slack/events`
3. Subscribe to these bot events:
   - `message.channels`
   - `message.groups`
   - `message.im`
   - `message.mpim`
4. Save changes

### 4. Create Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create App"
3. Fill in app details
4. Add `http://localhost:8888/callback` to Redirect URIs
5. Copy your Client ID and Client Secret

### 5. Configure Environment Variables

1. Copy the example configuration:
   ```bash
   cp config.env.example .env
   ```

2. Edit `.env` with your credentials:
   ```bash
   # Slack Bot Configuration
   SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
   SLACK_SIGNING_SECRET=your-actual-signing-secret
   
   # Spotify Configuration
   SPOTIFY_CLIENT_ID=your-spotify-client-id
   SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   SPOTIFY_PLAYLIST_ID=your-playlist-id-here
   
   # Server Configuration
   PORT=3000
   ```

### 6. Authenticate with Spotify

Run the setup script to authenticate with Spotify:

```bash
python setup.py
```

This will:
- Open your browser for Spotify authentication
- Show your available playlists
- Help you find the playlist ID to use

### 7. Create or Find Spotify Playlist

You can either:
- Use an existing playlist (get the ID from the setup script)
- Create a new playlist on Spotify and copy its ID from the URL

Add the playlist ID to your `.env` file:
```bash
SPOTIFY_PLAYLIST_ID=37i9dQZF1DX0XUsuxWHRQd
```

## Running the Bot

### Development

```bash
python main.py
```

The bot will start on `http://localhost:3000` (or your configured port).

### Production

For production deployment, consider using:
- **Heroku**: Easy deployment with git
- **Railway**: Simple Python app hosting
- **DigitalOcean App Platform**: Managed container hosting
- **AWS/GCP/Azure**: Cloud platforms with container services

Make sure to:
1. Set environment variables in your hosting platform
2. Update the Slack Event Subscriptions URL to your public domain
3. Update the Spotify Redirect URI if needed

## Usage

1. **Add the bot to Slack channels** where you want it to monitor messages
2. **Share YouTube URLs** in those channels
3. **Watch the magic happen!** The bot will:
   - Detect YouTube URLs
   - Extract song information
   - Search for the song on Spotify
   - Add it to your playlist
   - Confirm with a message

### Example

When someone shares:
```
Check out this song! https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

The bot will respond:
```
✅ Added to playlist: **Rick Astley - Never Gonna Give You Up**
```

## Bot Permissions

The bot needs these Slack permissions:
- **Read messages**: To detect YouTube URLs
- **Send messages**: To provide feedback
- **Access public/private channels**: Based on where you want it to work

## Troubleshooting

### Common Issues

1. **"Spotify authentication failed"**
   - Run `python setup.py` to re-authenticate
   - Check your Spotify credentials in `.env`

2. **"Could not find song on Spotify"**
   - The YouTube video might not be a music track
   - The song might not be available on Spotify
   - Try improving the video title format

3. **"Slack events not received"**
   - Check your Event Subscriptions URL is correct
   - Ensure your server is publicly accessible
   - Verify bot permissions in Slack

4. **"Bot not responding"**
   - Check bot is invited to the channel
   - Verify `SLACK_BOT_TOKEN` is correct
   - Look at server logs for errors

### Logs

The bot provides detailed logging. Check the console output for:
- YouTube URL detection
- Song extraction results
- Spotify search queries
- API errors

## How It Works

1. **Message Monitoring**: Bot listens for all messages in channels it's added to
2. **URL Detection**: Uses regex to find YouTube URLs in messages
3. **Song Extraction**: Uses `yt-dlp` to get video metadata
4. **Title Parsing**: Attempts to extract artist and song name from video title
5. **Spotify Search**: Tries multiple search strategies to find the song
6. **Playlist Addition**: Adds the found track to the configured playlist
7. **Feedback**: Sends confirmation or error messages back to Slack

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Look at the server logs
3. Open an issue on GitHub with details

---

Made with ❤️ for music lovers who share songs in Slack! 