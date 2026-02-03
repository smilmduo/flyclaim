# FlyClaim AI - n8n Hybrid Setup Guide

## 🎯 Option 2: n8n + Python Hybrid Architecture

**Benefits:**
- ✅ **60% less Python code** - n8n handles orchestration
- ✅ **Visual workflow** - Easy to understand and debug
- ✅ **Built-in nodes** - Email, HTTP, WhatsApp ready
- ✅ **Demo-friendly** - Show judges the visual flow
- ✅ **Faster development** - Connect boxes instead of coding

---

## 📐 Architecture Overview

```
User Message (WhatsApp/API)
        ↓
   n8n Workflow
        ↓
┌───────────────────────────────────┐
│     n8n Visual Orchestration     │
│                                   │
│  [Webhook] → [HTTP: Extract]     │
│       ↓                           │
│  [If: Valid?] → [HTTP: Eligible] │
│       ↓                           │
│  [If: Eligible?] → [HTTP: Doc]   │
│       ↓                           │
│  [Email: Send] → [Response]      │
└───────────────────────────────────┘
        ↓ (calls via HTTP)
┌───────────────────────────────────┐
│    Flask API (localhost:5000)    │
│                                   │
│  /api/extract     (Intake Agent) │
│  /api/eligibility (DGCA Rules)   │
│  /api/claim/generate (Document)  │
│  /api/claim/submit (Prepare)     │
└───────────────────────────────────┘
```

---

## 🚀 Quick Start (Step-by-Step)

### Step 1: Install Node.js (for n8n)

**Download & Install:**
- Go to: https://nodejs.org/
- Download **LTS version** for Windows
- Run installer (accept defaults)
- Verify in PowerShell:
  ```powershell
  node --version  # Should show v20.x.x or v18.x.x
  npm --version   # Should show 10.x.x
  ```

### Step 2: Install n8n

```powershell
# Install n8n globally
npm install -g n8n

# Verify installation
n8n --version
```

### Step 3: Set Up Python Environment

```powershell
# Navigate to project
cd C:\Users\ASUS\FlyClaim-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```powershell
# Copy example env file
copy .env.example .env

# Edit .env file (use notepad or any editor)
notepad .env
```

**Add your API keys in `.env`:**
```env
# Required
OPENAI_API_KEY=sk-your-openai-key-here

# For email (Gmail)
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password

# Optional (for later)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

**How to get Gmail App Password:**
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate password for "Mail"
5. Copy the 16-character password (no spaces)

### Step 5: Initialize Database

```powershell
python backend/database/init_db.py
```

You should see:
```
============================================================
FlyClaim AI - Database Initialization
============================================================
Creating database tables...
✓ Tables created successfully
...
✓ Database initialization completed successfully!
```

### Step 6: Start Flask API

**Open Terminal 1:**
```powershell
cd C:\Users\ASUS\FlyClaim-AI
.\venv\Scripts\Activate.ps1
python backend/app.py
```

You should see:
```
============================================================
🛫 FlyClaim AI - API Server Starting
============================================================
Server running on: http://localhost:5000
Health check: http://localhost:5000/health
Demo page: http://localhost:5000/demo
...
Ready for n8n integration!
============================================================
```

**Test the API:**
- Open browser: http://localhost:5000/demo
- Click "Extract Flight Details" button
- Should see JSON response with extracted data

### Step 7: Start n8n

**Open Terminal 2 (keep Flask running in Terminal 1):**
```powershell
n8n
```

You should see:
```
n8n ready on http://localhost:5678
Version: 1.x.x
```

**Open n8n:**
- Go to: http://localhost:5678
- First time: Set up username/password

### Step 8: Import Workflow

1. In n8n interface, click **"Workflows"** (top left)
2. Click **"Add Workflow"** → **"Import from File"**
3. Select: `C:\Users\ASUS\FlyClaim-AI\n8n_workflows\flyclaim_complete_workflow.json`
4. Click **"Import"**

You should see the complete visual workflow!

### Step 9: Configure n8n Email Node

1. In the workflow, click on **"5. Send Email to Airline"** node
2. Click **"Create New Credential"**
3. Select **"SMTP"**
4. Fill in:
   - **Host:** `smtp.gmail.com`
   - **Port:** `587`
   - **User:** Your Gmail address
   - **Password:** Your Gmail app password (from Step 4)
   - **Secure:** Enable TLS
5. Click **"Save"**

### Step 10: Test the Complete Workflow

#### Method 1: Using Webhook (Simplest)

1. In n8n workflow, click on **"WhatsApp Webhook"** node
2. Copy the **"Test URL"** (looks like: `http://localhost:5678/webhook-test/...`)
3. Open a new terminal and run:

```powershell
# Test with curl (or use Postman)
curl -X POST http://localhost:5678/webhook-test/YOUR-WEBHOOK-ID `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"My IndiGo flight 6E-234 from Delhi to Mumbai on 28 October was delayed by 5 hours\"}'
```

#### Method 2: Using Demo Page

1. Open: http://localhost:5000/demo
2. Type your flight delay message
3. Click "Extract Flight Details"
4. See the AI extract information in real-time

---

## 🎮 Testing the Agents

### Test 1: Intake Agent (Extract Details)

```powershell
curl -X POST http://localhost:5000/api/extract `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours\"}'
```

**Expected Response:**
```json
{
  "flight_number": "6E-234",
  "airline_name": "IndiGo",
  "flight_date": "2024-10-28",
  "departure": "Delhi",
  "arrival": "Mumbai",
  "disruption_type": "delay",
  "delay_hours": 5,
  "confidence": "high"
}
```

### Test 2: Eligibility Agent (Check DGCA Rules)

```powershell
curl -X POST http://localhost:5000/api/eligibility `
  -H "Content-Type: application/json" `
  -d '{\"flight_number\": \"6E-234\", \"flight_duration_hours\": 2.5, \"delay_hours\": 5, \"disruption_type\": \"delay\", \"is_international\": false}'
```

**Expected Response:**
```json
{
  "eligible": true,
  "compensation_amount": 10000,
  "currency": "INR",
  "reason": "Delay of 5 hours exceeds threshold...",
  "legal_basis": "DGCA CAR Section 3, Series M, Part IV"
}
```

### Test 3: Complete Flow in n8n

1. Click **"Execute Workflow"** button in n8n (top right)
2. Send test data to webhook
3. Watch nodes turn green as they execute
4. Check email - claim should be sent to airline!

---

## 📊 Workflow Visualization

In n8n, you'll see this visual flow:

```
┌─────────────┐
│ WhatsApp    │ → User sends message
│ Webhook     │
└──────┬──────┘
       ↓
┌─────────────┐
│ 1. Intake   │ → Extract flight details using GPT-4
│ Agent       │
└──────┬──────┘
       ↓
┌─────────────┐
│ Valid Data? │ → Check if all required fields present
└──┬────────┬─┘
   ↓ Yes    ↓ No → Ask for missing info
┌─────────────┐
│ 2. Eligibility │ → Check DGCA rules
│ Agent          │
└──────┬─────────┘
       ↓
┌─────────────┐
│ Eligible?   │ → Check compensation amount
└──┬────────┬─┘
   ↓ Yes    ↓ No → Inform not eligible
┌─────────────┐
│ 3. Document │ → Generate claim letter
│ Agent       │
└──────┬──────┘
       ↓
┌─────────────┐
│ 4. Submission│ → Prepare email
│ Agent        │
└──────┬───────┘
       ↓
┌─────────────┐
│ 5. Send     │ → Email to airline
│ Email       │
└──────┬──────┘
       ↓
┌─────────────┐
│ ✅ Success  │ → Confirmation to user
│ Response    │
└─────────────┘
```

---

## 🔧 Troubleshooting

### Issue 1: n8n not starting
```powershell
# Try clearing cache
npm cache clean --force
npm install -g n8n --force
```

### Issue 2: Flask API errors
```powershell
# Check if virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 3: OpenAI API errors
- Check your API key is correct in `.env`
- Verify you have credits: https://platform.openai.com/usage
- Try using GPT-3.5 instead: set `OPENAI_MODEL=gpt-3.5-turbo` in `.env`

### Issue 4: Email not sending
- Verify Gmail app password (not regular password)
- Check 2-Step Verification is enabled
- Try a different email service (Outlook, Yahoo)

---

## 💰 Cost Breakdown (MVP Testing)

| Service | Cost | Usage for Testing |
|---------|------|-------------------|
| OpenAI GPT-4 | ~$0.03/1K tokens | ~$2-5 for 100 test claims |
| n8n | Free (self-hosted) | Unlimited |
| Flask | Free | Unlimited |
| Gmail SMTP | Free | 500 emails/day |
| **Total for MVP** | **~$2-5** | Enough for demo |

---

## 📈 Advantages Over Option 1 (Pure Python)

| Aspect | Option 1 (Python) | Option 2 (n8n) |
|--------|-------------------|----------------|
| **Code lines** | ~2,000+ lines | ~800 lines + visual |
| **Setup time** | 5-7 days | 2-3 days |
| **Debugging** | Code inspection | Visual + logs |
| **Demo** | Need to explain code | Show visual flow |
| **Scalability** | Custom implementation | Built-in scaling |
| **Maintenance** | Code changes | Drag-drop changes |

---

## 🎯 Next Steps

### For Hackathon Demo:

1. **Record Video:**
   - Show n8n visual workflow
   - Test complete flow with live data
   - Show email being sent

2. **Prepare Slides:**
   - Screenshot of n8n workflow
   - Before/After comparison
   - Impact metrics

3. **Add Features:**
   - WhatsApp integration (use Twilio)
   - Web dashboard for claim tracking
   - PDF attachment of claim letter

### For Production:

1. **Deploy Flask API:**
   - Use Railway, Render, or Heroku
   - Get production URL

2. **Deploy n8n:**
   - Use n8n Cloud (easiest)
   - Or self-host on VPS

3. **Add Monitoring:**
   - Track claim success rates
   - Monitor API response times
   - Set up error alerts

---

## 📞 Support

- **n8n Community:** https://community.n8n.io/
- **n8n Docs:** https://docs.n8n.io/
- **Project Issues:** Check `PROJECT_STATUS.md`

---

**🎉 You're ready to build FlyClaim AI with n8n!**

Start both servers and see the magic happen:
1. Terminal 1: `python backend/app.py`
2. Terminal 2: `n8n`
3. Browser: http://localhost:5678

