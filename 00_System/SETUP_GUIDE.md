---
title: SETUP_GUIDE
type: note
tags:
- quest
- note
created: '2025-01-15'
modified: '2025-01-15'
---

# SETUP_GUIDE

---
title: SETUP GUIDE
type: note
tags:
- active
- note
created: '2025-08-14'
modified: '2025-08-14'
---

### 1. Discord Webhooks (Free)

**Purpose:** Get notifications when assets are generated

1. Open Discord and go to your server
2. Server Settings → Integrations → Webhooks
3. Click "New Webhook"
4. Copy the webhook URL
5. Add to n8n workflow as credential

### 2. Stability AI ($10 credits)

**Purpose:** High-quality SDXL image generation

1. Visit: https://platform.stability.ai
2. Create account and add credits ($10 minimum)
3. Go to Account → API Keys
4. Generate new API key
5. Add to n8n: HTTP Request node → Authentication → API Key

### 3. Replicate AI (Pay-per-use)

**Purpose:** Access to latest AI models (SDXL, AnimateDiff, etc.)

1. Visit: https://replicate.com
2. Sign up with GitHub
3. Go to Account → API tokens
4. Create new token
5. Usage: ~$0.01 per image

### 4. Airtable (Free tier)

**Purpose:** Database for asset management

1. Visit: https://airtable.com
2. Create workspace for "TTRPG Assets"
3. Go to Account → API
4. Generate personal access token
5. Scopes needed: data.records:read, data.records:write

### 5. Reddit API (Free)

**Purpose:** Pull trending D&D content

1. Visit: https://www.reddit.com/prefs/apps
2. Click "Create App"
3. Choose "script" type
4. Note the client ID and secret
5. No authentication needed for public subreddits

### 6. Weather API (Free)

**Purpose:** Generate weather-based events

1. Visit: https://openweathermap.org/api
2. Sign up for free account
3. Get API key from account dashboard
4. Free tier: 1000 calls/day

### 7. GitHub API (Free)

**Purpose:** Track D&D tools and updates

1. Visit: https://github.com/settings/tokens
2. Generate new token (classic)
3. Scopes: public_repo
4. Use in n8n HTTP Request nodes

### Import Workflows

1. Open n8n: http://localhost:5678
2. Click "Workflows" → "Import"
3. Select files from `scripts/n8n_workflows/`:
   - `mega_automation.json` - Main automation
   - `reddit_inspired.json` - Reddit integration
   - `weather_events.json` - Weather-based events
   - `multi_ai_pipeline.json` - Multi-AI generation

### Add Credentials in n8n

1. Settings → Credentials → Add Credential
2. Choose "Header Auth" for most APIs
3. Add your API keys:
   - Name: "OpenAI"
   - Header Name: "Authorization"
   - Header Value: "Bearer YOUR_KEY"

## 🎯 Quick Start Commands
```bash
# Test OpenAI integration

node scripts/openai_generator.js aquabyssos

# Run production workflow

node scripts/production_workflow.js --full

# Start n8n workflows

curl -X POST http://localhost:5678/webhook/ttrpg-generate

# Check generation status

curl http://localhost:5679/stats
```
## 💰 Cost Estimates

| Service | Free Tier | Paid Usage |
|---------|-----------|------------|
| OpenAI GPT-4 | No | ~$0.03/1K tokens |
| DALL-E 3 | No | $0.04/image (standard) |
| Stability AI | No | ~$0.002/image |
| Replicate | No | ~$0.01/image |
| Unsplash | 50/hour | Unlimited with attribution |
| Discord | Unlimited | Free |
| Reddit API | 60/minute | Free |
| Weather API | 1000/day | Free |
| Airtable | 1200 records | $20/month pro |

## 🚀 Recommended Workflow

1. **Start with Free Services:**
   - Reddit API → Get trending topics
   - Weather API → Generate events
   - Unsplash → Get inspiration
   - Discord → Notifications

2. **Add OpenAI (Already configured):**
   - GPT-4 → Generate lore
   - DALL-E 3 → Create images

3. **Scale with Paid Services:**
   - Stability AI → Bulk image generation
   - Replicate → Video generation
   - Airtable → Asset management

## 📊 Monitoring

Open the dashboard: `09_Performance/integration_dashboard.html`

Or check status via CLI:
# Check all services

node scripts/configure_apis.js

# View generation stats

cat 09_Performance/production_report.json

## 🔒 Security Notes

- Never commit API keys to git
- Keep `.obsidian/api_config.json` in `.gitignore`
- Use environment variables in production
- Rotate keys regularly
- Monitor usage to avoid unexpected charges

---

Ready to generate amazing TTRPG content with AI! 🎲✨

## Related

*Links to related content will be added here.*

## DM Notes

*Private notes for campaign integration:*
- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes
