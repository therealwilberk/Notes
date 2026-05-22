---
title: "Hermes Agent Masterclass: 2. Deploy to VPS, Connect to Telegram, Discord, etc."
source: https://youtube.com/watch?v=dcXmUUZvDLE
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, masterclass, 2, deployment, docker, vps, telegram, discord, gateway]
---

# Hermes Agent Masterclass: 2. Deploy to VPS, Connect to Telegram, Discord, etc.

## Key Concepts
- **Backend** = wherever the agent runs (local, Docker, VPS, etc.)
- Six backend options: Local, Docker, SSH/VPS, Modal (serverless), Daytona (team workspaces), Singularity (HPC)
- **Docker backend**: sandboxed security — commands run inside container, host is untouched
- **VPS backend**: always-on remote server ($6/mo on DigitalOcean)
- Docker deployment does NOT reinstall Hermes — changes only the `terminal backend` setting
- **Gateway**: one long-running process that speaks 16+ platforms, all sharing same agent/memory/sessions/skills
- Gateway runs as **systemd service** — starts on boot, restarts on crashes

## Backend Options Comparison

| Backend | Cost | Security | Always-On | Best For |
|---------|------|----------|-----------|----------|
| Local | Free | Low | While laptop on | At-home use |
| Docker | Free | Medium (sandboxed) | While laptop on | Security-conscious local use |
| VPS (DigitalOcean) | $6/mo | Configurable | 24/7 | Mobile access, always-on |
| Modal | Variable | High | No (hibernates) | Bursty workloads |

## Step-by-Step: Docker Backend

1. **Install Docker Desktop** from docker.com
   - Download for your OS (Windows: download Windows version even though using WSL — Docker has built-in WSL integration)
2. **Enable WSL integration**: Docker Desktop → Settings → Resources → WSL Integration → Enable
3. **Verify Docker works**: `docker version` in WSL terminal
4. **Switch Hermes backend**: `hermes setup terminal`
   - Select Docker
   - Keep default Docker image (press Enter)
   - Persistent file system: Yes
   - CPU cores: 1
   - Memory: default
5. **Verify**: `hermes chat` → ask agent to run `hostname` — should show Docker container ID
6. **Security proof**: Files created by agent exist only in container, not on host. SSH keys/credentials are safe by default.

## Step-by-Step: VPS (DigitalOcean)

1. **Create DigitalOcean account** at digitalocean.com
2. **Create Droplet**:
   - Region: closest to you
   - OS: Ubuntu
   - Plan: Basic / Shared CPU / Regular — **$6/mo** (1 CPU, 1 GB RAM, 25 GB storage)
   - SSH key: follow their guide or run `ssh-keygen` locally → paste public key
3. **Copy droplet IP address**
4. **SSH in**: `ssh root@YOUR_IP`
5. **Install Hermes on VPS**: Same one-command install as local
   ```bash
   # Same install command from the repo
   # Dependencies auto-install (Python, Git, Node.js)
   ```
6. **Quick setup** on VPS: configure provider (same OpenRouter key), skip full setup
7. **Install gateway as systemd service**:
   ```
   # During setup, choose: system service
   # System service installed and enabled
   ```
8. **Enable persistent service** (survives SSH logout):
   ```bash
   loginctl enable-linger root
   ```
9. **Verify**: Exit SSH → reconnect → `systemctl --user status hermes-gateway` should still show active

## Step-by-Step: Telegram Bot

1. Open Telegram → search **@BotFather**
2. `/newbot` → choose name → choose username
3. Copy the **bot token** (never expose this)
4. During Hermes gateway setup, paste token when prompted
5. **Find your Telegram user ID**: Message **@userinfobot** on Telegram → it returns your numeric ID
6. Enter user ID in Hermes setup (allowlist — only you can talk to bot)
7. Gateway installed as systemd service → start it
8. Test: Open chat with your bot → send "Hi" → agent responds

## Step-by-Step: Discord Bot

1. Go to **discord.com/developers/applications**
2. Create New App → name it
3. **Bot settings** (critical!):
   - Enable **Server Members Intent** ✅
   - Enable **Message Content Intent** ✅
   - ⚠️ Without these, bot receives empty messages — common mistake!
4. Reset Token → copy token (never expose)
5. Enter Discord bot token during Hermes setup + your Discord user ID
6. **Invite bot to server**: OAuth2 → URL Generator
   - Scopes: `bot`, `application.commands`
   - Permissions: Send Messages, Manage Threads, Embed Links, Attach Files, Read Message History
7. Open generated URL → select your server → Authorize
8. Bot appears in server → creates thread → test messaging

## Gateway Architecture
```
                    ┌─────────────┐
   Telegram ────────┤             │
   Discord  ────────┤   Gateway   ├──── Single Agent
   Slack    ────────┤  (16+       │     (shared memory,
   iMessage ────────┤  adapters)  │      sessions, skills)
   WeChat   ────────┤             │
                    └─────────────┘
```
- One gateway, many platforms
- All adapters feed into ONE shared agent
- Same memory across Telegram, Discord, CLI
- Runs as systemd service

## Commands & Config Snippets

```bash
# Switch to Docker backend
hermes setup terminal   # Select Docker

# Verify Docker is running
docker version

# SSH into VPS
ssh root@YOUR_IP

# Check gateway status
systemctl --user status hermes-gateway

# Make gateway survive SSH logout
loginctl enable-linger root

# Resume sessions from CLI (same agent across platforms)
hermes chat
# /sessions → resume
```

## Tips & Gotchas
- **Docker ≠ reinstall**: Changing to Docker backend only affects where commands execute — all sessions/memories/skills remain
- **1 GB RAM minimum** for VPS — below that, browser tools struggle
- **Discord intents are critical**: Server Members Intent + Message Content Intent must both be enabled or bot gets empty messages
- **loginctl enable-linger** is essential for VPS — without it, systemd service stops when SSH disconnects
- Docker and VPS can be **complementary**: Docker at home, VPS for mobile access
- For production: set up non-root user with firewall rules (leaving root on open internet is a demo shortcut)
- Hetzner is good alternative VPS for EU users
- Telegram is recommended as easiest platform to set up — Discord is more complex but works the same

## Timestamps & Chapters
- 0:00 - Introduction & module overview
- 1:30 - Backend options overview (6 types)
- 4:00 - Docker Desktop setup & WSL integration
- 8:00 - Switching Hermes to Docker backend
- 11:00 - Testing Docker sandbox security
- 13:00 - DigitalOcean VPS setup ($6 droplet)
- 17:00 - SSH into VPS & install Hermes
- 19:00 - Gateway architecture explained
- 21:00 - Telegram bot setup (@BotFather)
- 24:00 - Discord bot setup (developer portal, intents, OAuth2)
- 28:00 - Installing gateway as systemd service
- 29:30 - Testing across Telegram, Discord, and CLI
- 30:00 - Live demo: business idea worked on from all three platforms

## Summary
Module 2 covers deploying Hermes beyond the local terminal: Docker sandboxing for security hardening, a $6/mo DigitalOcean VPS for 24/7 availability, and setting up the gateway to connect Telegram and Discord bots. Key lesson: one agent, one memory, accessible from 16+ platforms via the gateway. The live demo shows the same agent responding to the same task across Telegram, Discord, and CLI with shared session memory.
