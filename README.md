# ⚡ SLS Hosting — Professional Telegram Hosting Bot

## New Professional Features Implemented
- Download/deploy progress cards with visual progress bar and speed line in Telegram repo import flow.
- Dashboard upgraded with speed, uptime, storage, and per-project file/runtime meter UI.
- Free plan limit: **2 active repos/projects max** per user.
- Premium management in bot with duration support: month/year and expiry tracking.
- Dynamic admin management directly in bot (add/remove/list admins).
- Owner/admin broadcast system in bot.

## Telegram Commands
- `/start`
- `/stats`
- `/broadcast <message>`
- `/addadmin <user_id>` (owner)
- `/removeadmin <user_id>` (owner)
- `/admins`
- `/premium <user_id> <month|year|off> <count>`
- `/setstartimage` (reply photo)
- `/setstartvideo` (reply video)
- `/clonebot <token>`
- Send repo URL to import/scan/deploy panel

## Business Logic
- Free users can host only 2 repos/projects at a time.
- Premium users bypass free limit while premium is active.
- Admin control can be updated from Telegram bot directly (no code edits needed).

Developer: @ItsRyoSudhish
Support/Updates: https://t.me/+yuLoicn7Djk0ZDY1

- Persistent bot state is now stored at `storage/bot_state.json` and auto-loaded on startup (users/admins/premium/runtimes/repos/projects).


## Heroku Deployment
- Added `Procfile` with `bot` and `api` process types.
- Added `app.json` for one-click Heroku app setup (env vars + dyno formation).
- Added `runtime.txt` pinned to Python 3.11.
- Added `requirements.txt` for Heroku Python buildpack compatibility.

### Deploy flow
1. Push repository to GitHub.
2. Create app from `app.json` on Heroku dashboard.
3. Set required env vars (`BOT_TOKEN`, `BOT_OWNER_ID`, `MONGO_URI`).
4. Enable both dynos: `bot` and `api`.
