# Discord Bot Setup Checklist

## Step 1: Create Application
1. Go to https://discord.com/developers/applications
2. Click "New Application" → name it (e.g., "JobBot" or "Zenicious")
3. Go to "Bot" tab → click "Add Bot"

## Step 2: Bot Permissions
Under "Bot" tab:
- [ ] Enable "Message Content Intent" (CRITICAL — n8n needs to read messages)
- [ ] Enable "Server Members Intent" (optional, for member tracking)

Under "OAuth2 → URL Generator":
- Scopes: `bot`, `applications.commands`
- Permissions:
  - Send Messages
  - Embed Links
  - Attach Files
  - Read Message History
  - Add Reactions
  - Use Slash Commands
  - Manage Messages (for pinning dashboard)

## Step 3: Invite Bot
- Copy the generated URL from OAuth2 → URL Generator
- Open in browser → select your server → Authorize

## Step 4: Get Credentials
- **Bot Token**: Bot tab → "Reset Token" → copy (keep secret)
- **Server (Guild) ID**: Right-click server name → Copy Server ID (enable Developer Mode in Discord settings)
- **Channel IDs**: Right-click each channel → Copy Channel ID

## Step 5: Share with Me
I need:
1. Bot token (save to .env, never share in chat)
2. Server ID
3. Channel IDs for: #alerts, #feed-eee, #dashboard, #log

## Step 6: n8n Credentials
In n8n (http://localhost:5678):
1. Go to Credentials → Add Credential → Discord Bot
2. Paste bot token
3. Test connection

---

## Channel ID Template
Fill this in after creating channels:

```
#alerts:        
#feed-eee:      
#feed-general:  
#validated:     
#applied:       
#companies:     
#dashboard:     
#log:           
#agent-status:  
```
