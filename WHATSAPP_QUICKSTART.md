# 📱 WhatsApp Integration - Quick Start

## 🚀 **3-Minute Setup**

### 1. Get Twilio Account
- Sign up: https://www.twilio.com/try-twilio
- Get **$15.50 free credit** (500 WhatsApp messages)

### 2. Join WhatsApp Sandbox
1. Twilio Console → Messaging → Try it out → WhatsApp
2. Open WhatsApp, message **+1 415 523 8886**
3. Send: `join [your-code]` (shown in Twilio)

### 3. Get Credentials
Copy from Twilio Dashboard:
- Account SID
- Auth Token  
- Phone: +14155238886

### 4. Add to .env
```env
TWILIO_ACCOUNT_SID=ACxxx...
TWILIO_AUTH_TOKEN=xxx...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 5. Setup ngrok (for local testing)
```powershell
# Download: https://ngrok.com/download
cd C:\ngrok
.\ngrok.exe http 5000

# Copy HTTPS URL (e.g., https://abc123.ngrok.io)
```

### 6. Configure Webhook in Twilio
- Twilio → Messaging → WhatsApp Sandbox
- **When message comes in:** `https://abc123.ngrok.io/webhook/whatsapp`
- Click Save

### 7. Start Flask
```powershell
cd C:\Users\ASUS\FlyClaim-AI
.\venv\Scripts\Activate.ps1
python backend/app.py
```

### 8. Test!
Send on WhatsApp:
```
My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours
```

**Expected Response:**
```
✅ Great News!
You are eligible for ₹10,000 compensation!
...
```

---

## 🎮 **Test Messages**

| Message | Expected Result |
|---------|----------------|
| `hi` | Welcome message |
| `help` | Feature list |
| `My IndiGo 6E-234 from Delhi to Mumbai on 28 Oct delayed 5 hours` | ₹10,000 eligible |
| `My flight was delayed` | Asks for missing info |
| `Air India AI-615 cancelled on Nov 1` | Cancellation result |

---

## 🔧 **Troubleshooting**

| Problem | Solution |
|---------|----------|
| No response | Check Flask is running |
| Webhook error | Verify ngrok URL in Twilio |
| OpenAI error | Check API key in .env |
| ngrok expired | Restart ngrok (2hr limit on free) |

---

## 💰 **Costs**

- Twilio Trial: **$15.50 FREE** (500 messages)
- ngrok: **FREE** (2hr sessions)
- OpenAI: **~$0.03/message**

**Total for 100 tests: ~$3-5**

---

## 📊 **Architecture**

```
WhatsApp → Twilio → ngrok → Flask → AI Agents → Response
```

---

## 🎯 **For Production**

Deploy Flask to Railway/Heroku:
```powershell
railway up
# Get URL: https://your-app.railway.app
```

Update Twilio webhook to production URL (no ngrok needed)

---

## 📱 **Demo Tips**

1. Screen record your phone
2. Show WhatsApp conversation
3. Send complete message
4. Wait 2-3 seconds
5. Show AI response with ₹ amount
6. Highlight: No app, instant, AI-powered

---

**Full Guide:** `WHATSAPP_SETUP.md`  
**Questions?** Check `BUILD_COMPLETE.md`

