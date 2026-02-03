# 📱 WhatsApp Integration Setup Guide

## Complete guide to add WhatsApp messaging to FlyClaim AI using Twilio

---

## 🎯 What You'll Get

After setup, users can:
- ✅ Send flight delay info via WhatsApp
- ✅ Get instant eligibility check (₹5K-₹20K)
- ✅ Receive automated compensation claim
- ✅ Track claim status via WhatsApp

**Example conversation:**
```
User: My IndiGo flight 6E-234 from Delhi to Mumbai 
      on 28 Oct was delayed by 5 hours

Bot:  ✅ Great News!
      You are eligible for ₹10,000 compensation!
      
      Reply 'YES' to file the claim automatically
```

---

## 📋 Prerequisites

- ✅ FlyClaim AI backend running
- ✅ OpenAI API key (already configured)
- ✅ Gmail account (for sending claims)
- ⏳ Twilio account (we'll set this up now)

---

## 🚀 Step-by-Step Setup

### Step 1: Create Twilio Account

1. **Go to Twilio:**
   - Visit: https://www.twilio.com/try-twilio
   - Click **"Sign up for free"**

2. **Fill registration:**
   - Email address
   - Password
   - First & Last name
   - Country: India
   - Phone number: Your mobile number

3. **Verify phone:**
   - Enter OTP sent to your phone

4. **Complete welcome questionnaire:**
   - Purpose: "Products & Services" or "Testing"
   - Products: Select "Messaging"
   - Language: Python
   - Click "Get Started with Twilio"

5. **Get your free trial:**
   - You'll receive **$15.50 in free credits**
   - Good for ~500 WhatsApp messages

### Step 2: Enable WhatsApp Sandbox

1. **In Twilio Console:**
   - Left sidebar → **"Messaging"**
   - Click **"Try it out"**
   - Select **"Send a WhatsApp message"**

2. **Join sandbox:**
   - You'll see a **Sandbox phone number**: `+1 415 523 8886`
   - You'll see a **join code**: like `join <word>-<word>`
   - Example: `join color-butter`

3. **Activate WhatsApp:**
   - Open WhatsApp on your phone
   - Start a chat with: **+1 415 523 8886**
   - Send the join code: `join color-butter` (use YOUR code)
   - You'll get confirmation: "Sandbox is ready!"

4. **Save sandbox details:**
   ```
   Sandbox Number: +1 415 523 8886
   Your Join Code: join color-butter (yours will be different)
   ```

### Step 3: Get Twilio Credentials

1. **In Twilio Console Dashboard:**
   - You'll see **"Account Info"** box
   - Copy these three values:

   ```
   Account SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Auth Token: (click "show" then copy)
   My Twilio phone number: +14155238886
   ```

2. **Keep these safe** - we'll add them to `.env` file

### Step 4: Configure Webhook URL

#### Option A: Local Testing with ngrok (Recommended for Development)

1. **Install ngrok:**
   - Download: https://ngrok.com/download
   - Extract to `C:\ngrok\`
   - Sign up for free account: https://dashboard.ngrok.com/signup
   - Copy your auth token

2. **Configure ngrok:**
   ```powershell
   cd C:\ngrok
   .\ngrok.exe config add-authtoken YOUR_NGROK_TOKEN
   ```

3. **Start ngrok tunnel:**
   ```powershell
   .\ngrok.exe http 5000
   ```

   You'll see:
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:5000
   ```

4. **Copy the HTTPS URL:** `https://abc123.ngrok.io`

5. **Configure Twilio Webhook:**
   - Go to Twilio Console
   - Messaging → Try it out → Send a WhatsApp message
   - Scroll to **"Sandbox Configuration"**
   - **When a message comes in:** 
     - Paste: `https://abc123.ngrok.io/webhook/whatsapp`
   - Click **"Save"**

#### Option B: Deployed Server (Production)

If you've deployed Flask to Heroku/Railway/etc:
```
Webhook URL: https://your-app-name.herokuapp.com/webhook/whatsapp
```

### Step 5: Update .env File

```powershell
cd C:\Users\ASUS\FlyClaim-AI
notepad .env
```

Add these lines:
```env
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token-here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Save and close notepad**

### Step 6: Start Flask Server

```powershell
cd C:\Users\ASUS\FlyClaim-AI
.\venv\Scripts\Activate.ps1
python backend/app.py
```

You should see:
```
🛫 FlyClaim AI - API Server Starting
============================================================
Server running on: http://localhost:5000
...
WhatsApp webhook: /webhook/whatsapp
```

### Step 7: Test WhatsApp Integration

1. **Open WhatsApp** on your phone

2. **Find the conversation** with `+1 415 523 8886`

3. **Send test message:**
   ```
   My IndiGo flight 6E-234 from Delhi to Mumbai on 28 October was delayed by 5 hours
   ```

4. **You should get response:**
   ```
   ✅ Great News!

   You are eligible for ₹10,000 compensation!

   📋 Details:
   Flight: 6E-234
   Date: 2024-10-28
   Route: Delhi → Mumbai
   Issue: Delay

   💼 Legal Basis:
   DGCA CAR Section 3

   🚀 Next Steps:
   Reply 'YES' to file the claim automatically
   ```

---

## 🎮 Test Commands

Try these messages:

### 1. Welcome Message
```
hi
```
Response: Bot introduction and instructions

### 2. Help Command
```
help
```
Response: List of features and example usage

### 3. Full Claim (All info)
```
My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours
```
Response: Eligibility result with compensation amount

### 4. Partial Info (Missing details)
```
My flight was delayed yesterday
```
Response: Bot asks for missing information

### 5. Cancellation
```
Air India flight AI-615 from Bangalore to Delhi on Nov 1 was cancelled
```
Response: Cancellation compensation result

### 6. Not Eligible (Short delay)
```
My SpiceJet flight SG-123 from Mumbai to Pune on Oct 30 was delayed 1 hour
```
Response: Not eligible (delay < 2 hours)

---

## 🔧 Troubleshooting

### Issue 1: "Webhook not responding"

**Check:**
- Is Flask server running?
- Is ngrok tunnel active?
- Is ngrok URL correct in Twilio?

**Fix:**
```powershell
# Terminal 1: Restart ngrok
cd C:\ngrok
.\ngrok.exe http 5000

# Terminal 2: Restart Flask
cd C:\Users\ASUS\FlyClaim-AI
.\venv\Scripts\Activate.ps1
python backend/app.py
```

### Issue 2: "Account SID must start with AC"

**Fix:** Double-check you copied the full Account SID from Twilio dashboard

### Issue 3: "OpenAI API error"

**Fix:** Check your OpenAI API key in `.env` file and verify you have credits

### Issue 4: ngrok session expired

**Symptom:** Webhook stops working after 2 hours

**Fix:** Restart ngrok (free tier has 2-hour sessions)
```powershell
.\ngrok.exe http 5000
# Copy new URL and update Twilio webhook
```

**Solution:** Upgrade to ngrok paid ($8/month) or deploy to cloud

---

## 💰 Cost Breakdown

| Service | Free Tier | Paid |
|---------|-----------|------|
| **Twilio Trial** | $15.50 credit | $0.005/WhatsApp msg |
| **ngrok** | 2-hour sessions | $8/month (persistent URL) |
| **OpenAI GPT-4** | Pay-as-you-go | ~$0.03/request |
| **Flask** | Free (local) | $5-10/month (cloud) |

**Total for Testing:** ~$15 free credit (300-500 messages)

---

## 📊 Conversation Flow

```
┌─────────────────────┐
│ User: Flight delay  │
│ message via WhatsApp│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Twilio forwards to  │
│ Flask webhook       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Intake Agent        │
│ (Extract details)   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Eligibility Agent   │
│ (Check DGCA rules)  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Response sent back  │
│ via WhatsApp        │
└─────────────────────┘
```

---

## 🚀 Deploy to Production

### Option 1: Railway (Easiest)

1. **Install Railway CLI:**
   ```powershell
   npm install -g @railway/cli
   ```

2. **Deploy:**
   ```powershell
   cd C:\Users\ASUS\FlyClaim-AI
   railway login
   railway init
   railway up
   ```

3. **Get URL:**
   ```powershell
   railway domain
   ```
   Example: `https://flyclaim-ai.railway.app`

4. **Update Twilio webhook:**
   ```
   https://flyclaim-ai.railway.app/webhook/whatsapp
   ```

### Option 2: Heroku

```powershell
heroku create flyclaim-ai
git push heroku main
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set TWILIO_ACCOUNT_SID=AC...
```

Webhook URL: `https://flyclaim-ai.herokuapp.com/webhook/whatsapp`

---

## 🎯 Advanced Features

### 1. Multi-user Support

Current setup handles multiple users automatically - each WhatsApp number is tracked separately.

### 2. Session State

To add conversation memory:
- Store user state in database
- Track partial information across messages
- Remember context for follow-up questions

### 3. Rich Media

Send images/PDFs via WhatsApp:
```python
from twilio.rest import Client

client.messages.create(
    from_='whatsapp:+14155238886',
    to='whatsapp:+919876543210',
    body='Your claim letter:',
    media_url=['https://your-server.com/claim.pdf']
)
```

### 4. WhatsApp Business API

For production (verified sender, custom branding):
- Apply for WhatsApp Business API
- Takes 2-3 weeks approval
- Cost: $0.004-0.009 per conversation

---

## 📱 Demo Script (For Presentation)

1. **Show your phone screen** (via screen sharing or recording)

2. **Open WhatsApp** → Twilio Sandbox number

3. **Send message:**
   ```
   My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours
   ```

4. **Show instant response** with compensation amount

5. **Highlight:**
   - Natural language understanding
   - Instant DGCA rule application
   - No app download needed
   - Works on any phone

---

## 🎉 Success!

You now have:
✅ WhatsApp integration working  
✅ Real-time AI responses  
✅ Automated eligibility checks  
✅ Professional demo capability  

**Test it now!** Send a message to your Twilio sandbox number.

---

## 📞 Support

- **Twilio Docs:** https://www.twilio.com/docs/whatsapp
- **ngrok Docs:** https://ngrok.com/docs
- **Twilio Console:** https://console.twilio.com/
- **FlyClaim AI Issues:** Check `BUILD_COMPLETE.md`

---

**Next:** Test the complete flow from WhatsApp → AI → Claim! 🚀

