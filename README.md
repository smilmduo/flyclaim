# FlyClaim AI - Agentic AI for Indian Flight Compensation

> **India's first autonomous AI agent system that handles flight compensation claims end-to-end under DGCA regulations.**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

---

## 🎯 Problem Statement

- **2.58M+ Indian passengers** face flight delays/cancellations yearly
- **Less than 2%** receive compensation (₹5,000-₹20,000)
- **90%** don't know they can claim under DGCA CAR Section 3
- **61%** never get compensation due to airline resistance
- **30-90 days** manual process → most passengers give up

## 💡 Solution

**FlyClaim AI** = Multi-agent autonomous system that handles complete claim lifecycle:

✅ WhatsApp-first interface (no app needed)  
✅ Automatic flight verification  
✅ DGCA-compliant eligibility check  
✅ AI-generated legal claim letters  
✅ Auto-submission to airline nodal officers  
✅ 30-day tracking + auto-escalation to AirSewa/DGCA  
✅ Consumer court draft preparation  

**"From flight disruption to compensation — fully automated by AI."**

---

## 🏗️ Architecture

```
┌─────────────┐
│  WhatsApp   │
│   (Twilio)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│       Flask Backend (Python)        │
│  ┌──────────────────────────────┐   │
│  │   AI Agents (GPT-4)          │   │
│  │  • Intake Agent              │   │
│  │  • Eligibility Agent         │   │
│  │  • Document Agent            │   │
│  │  • Submission Agent          │   │
│  │  • Monitoring Agent          │   │
│  │  • Escalation Agent          │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
       │         │         │
       ▼         ▼         ▼
┌──────────┐ ┌──────┐ ┌─────────┐
│AviationStack│ │SQLite│ │ Email│
│    API    │ │  DB  │ │ (SMTP) │
└──────────┘ └──────┘ └─────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.9+ + Flask | API orchestration |
| **AI Engine** | OpenAI GPT-4 | Multi-agent reasoning |
| **Orchestration** | n8n (optional) | Visual workflow |
| **WhatsApp** | Twilio API | User interface |
| **Flight Data** | AviationStack API | Real-time verification |
| **Database** | SQLite → PostgreSQL | Claim tracking |
| **PDF Generation** | ReportLab | Legal documents |
| **Email** | SMTP (Gmail) | Airline submission |
| **Frontend** | Flask + Jinja2 | Web dashboard |

---

## 🚀 Quick Start (Windows)

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- OpenAI API key
- Twilio account (free tier)
- AviationStack API key (free tier)

### Installation

```powershell
# 1. Clone/navigate to project
cd C:\Users\ASUS\FlyClaim-AI

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Edit .env with your API keys

# 5. Initialize database
python backend/database/init_db.py

# 6. Run the application
python backend/app.py
```

Server starts at: `http://localhost:5000`

---

## 🔑 Environment Variables

Create a `.env` file with:

```env
# OpenAI
OPENAI_API_KEY=sk-your-openai-key-here

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# AviationStack API
AVIATIONSTACK_API_KEY=your-aviationstack-key

# Email (for airline submission)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# App Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///flyclaim.db
```

### Getting API Keys:

1. **OpenAI**: https://platform.openai.com/api-keys
2. **Twilio**: https://www.twilio.com/try-twilio (Free trial: $15 credit)
3. **AviationStack**: https://aviationstack.com/signup/free (Free: 100 requests/month)
4. **Gmail App Password**: Google Account → Security → 2-Step Verification → App Passwords

---

## 📁 Project Structure

```
FlyClaim-AI/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── intake_agent.py          # Extracts flight details from text
│   │   ├── eligibility_agent.py      # DGCA rule validation
│   │   ├── document_agent.py         # Generates claim letters
│   │   ├── submission_agent.py       # Sends to airlines
│   │   ├── monitoring_agent.py       # Tracks 30-day window
│   │   └── escalation_agent.py       # AirSewa/DGCA escalation
│   ├── database/
│   │   ├── models.py                 # SQLAlchemy models
│   │   └── init_db.py                # Database initialization
│   ├── utils/
│   │   ├── dgca_rules.py             # DGCA CAR Section 3 logic
│   │   ├── pdf_generator.py          # ReportLab PDF creation
│   │   ├── flight_api.py             # AviationStack integration
│   │   └── email_sender.py           # SMTP email automation
│   ├── routes/
│   │   ├── whatsapp_webhook.py       # Twilio webhook handler
│   │   ├── api_routes.py             # REST API endpoints
│   │   └── web_routes.py             # Dashboard routes
│   ├── templates/                    # HTML templates
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── claim_status.html
│   ├── static/                       # CSS, JS, images
│   │   ├── css/
│   │   └── js/
│   ├── config.py                     # Configuration
│   └── app.py                        # Main Flask app
├── n8n_workflows/
│   └── flyclaim_workflow.json        # Importable n8n workflow
├── docs/
│   ├── DGCA_CAR_Section3.md          # DGCA regulations
│   ├── claim_template.md             # Letter templates
│   └── API.md                        # API documentation
├── tests/
│   ├── test_agents.py
│   └── test_dgca_rules.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🎮 Usage

### Via WhatsApp:

1. Send message to Twilio WhatsApp number: `whatsapp:+14155238886`
2. Type: `"My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours"`
3. AI automatically:
   - Verifies flight data
   - Checks DGCA eligibility
   - Generates claim letter
   - Emails airline nodal officer
   - Sends you confirmation

### Via Web Dashboard:

1. Go to `http://localhost:5000`
2. Enter flight details
3. View claim status and documents
4. Track 30-day airline response window

---

## 🧠 AI Agents Explained

| Agent | Responsibility | Technology |
|-------|---------------|-----------|
| **Intake Agent** | Extracts flight number, date, delay duration from natural language | GPT-4 with structured output |
| **Eligibility Agent** | Applies DGCA CAR Section 3 rules, calculates compensation (₹5k-₹20k) | Rule engine + GPT-4 |
| **Document Agent** | Drafts legal claim letter citing DGCA regulations | GPT-4 with legal templates |
| **Submission Agent** | Emails airline nodal officer (as per DGCA mandate) | SMTP automation |
| **Monitoring Agent** | Tracks 30-day airline response deadline | Scheduled jobs |
| **Escalation Agent** | Auto-escalates to AirSewa/DGCA if no response | API/form automation |
| **Legal Agent** | Prepares consumer court complaint template | GPT-4 legal generation |

---

## 📊 DGCA Rules (CAR Section 3)

### Compensation Matrix:

| Flight Duration | Delay | Compensation |
|----------------|-------|--------------|
| < 1 hour | > 2 hours | ₹5,000 |
| 1-2 hours | > 2 hours | ₹7,500 |
| > 2 hours | > 2 hours | ₹10,000 |
| Cancellation | < 2 weeks notice | ₹10,000-₹20,000 |
| Denied Boarding | Confirmed ticket | ₹10,000-₹20,000 |

### Exemptions (No Compensation):

- Extraordinary circumstances (weather, security threats, ATC strikes)
- Passenger informed ≥2 weeks before departure
- Alternative flight offered within 1 hour

**Reference**: [DGCA CAR Section 3, Series M, Part IV](https://www.dgca.gov.in)

---

## 🧪 Testing

```powershell
# Run unit tests
pytest tests/ -v

# Test specific agent
pytest tests/test_agents.py::test_intake_agent -v

# Test DGCA rules
pytest tests/test_dgca_rules.py -v
```

---

## 🌐 API Endpoints

### REST API:

```
POST   /api/claim/create          # Create new claim
GET    /api/claim/<id>            # Get claim status
POST   /api/claim/<id>/escalate   # Manual escalation
GET    /api/claims/user/<phone>   # Get user's claims

POST   /webhook/whatsapp          # Twilio webhook (internal)
```

### Example Request:

```bash
curl -X POST http://localhost:5000/api/claim/create \
  -H "Content-Type: application/json" \
  -d '{
    "flight_number": "6E-234",
    "date": "2025-10-28",
    "delay_hours": 5,
    "passenger_name": "Rahul Kumar",
    "passenger_email": "rahul@example.com",
    "passenger_phone": "+919876543210"
  }'
```

---

## 🔄 n8n Workflow (Optional)

For visual orchestration:

1. Install n8n: `npm install -g n8n`
2. Run: `n8n`
3. Import workflow: `n8n_workflows/flyclaim_workflow.json`
4. Configure nodes with your API keys
5. Activate workflow

Benefits:
- Visual agent flow
- Easy debugging
- No-code modifications
- Parallel execution

---

## 🚀 Deployment

### Option 1: Heroku (Easy)

```bash
heroku create flyclaim-ai
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku config:set OPENAI_API_KEY=sk-...
```

### Option 2: Railway (Modern)

```bash
railway login
railway init
railway up
```

### Option 3: DigitalOcean / AWS (Production)

- Use Docker container
- Set up PostgreSQL database
- Configure environment variables
- Use Gunicorn + Nginx

---

## 💰 Business Model

### Phase 1 (India - MVP):
- Free eligibility check
- **10% success fee** on compensation (vs industry 25-35%)
- Alternative: **₹199 flat fee** per claim

### Phase 2 (EU/UK/UAE):
- Support EU261, UK CAA, UAE GCAA
- **20-30% commission** (market standard)
- Premium fast-track service

### Phase 3 (B2B SaaS):
- API for airlines/insurers (subscription)
- White-label for travel agencies
- Analytics dashboard

---

## 📈 Scalability

- **Multi-region**: Add EU261, UK CAA rules
- **Multi-channel**: Telegram, voice IVR, mobile app
- **Multi-language**: Hindi, Tamil, Bengali support
- **ML predictions**: Delay forecasting
- **Blockchain**: Immutable claim records

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📜 Legal Disclaimer

FlyClaim AI is an automation tool. Users are responsible for:
- Accuracy of flight information provided
- Review of generated claim documents
- Final submission decisions

This tool does not provide legal advice. Consult an attorney for complex cases.

---

## 📞 Support

- **Email**: support@flyclaim.ai
- **Issues**: GitHub Issues
- **Docs**: [Full documentation](docs/)

---

## 🏆 Hackathon Ready

This project is designed for:
- ✅ 5-7 day build timeline
- ✅ Clear demo workflow
- ✅ Real-world impact
- ✅ Scalable architecture
- ✅ Visual presentation (n8n)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- DGCA for passenger rights framework
- OpenAI for GPT-4 API
- Twilio for WhatsApp Business API
- AviationStack for flight data

---

**Built with ❤️ for Indian travelers | Making flight compensation accessible to all**

