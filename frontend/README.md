# FlyClaim AI - Frontend & Backend Setup

This guide provides complete instructions on how to install, configure, and run the FlyClaim AI application, including both the Python Backend and the React Frontend.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** (For the backend)
- **Node.js 18+ & npm** (For the frontend)
- **Git** (To clone the repository)

---

## 🚀 Installation & Setup

### 1. Backend Setup (Flask API)

The backend handles the business logic, AI agents, database, and authentication.

1.  **Navigate to the project root:**
    ```bash
    cd FlyClaim-AI
    ```

2.  **Create and activate a virtual environment:**
    *   **Windows:**
        ```powershell
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        ```
    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    *   Create a `.env` file in the root directory (copy from `.env.example`).
    *   Add your API keys (OpenAI, Twilio, etc.) and configuration.
    *   Ensure `DATABASE_URL` is set (default is `sqlite:///flyclaim.db`).

5.  **Initialize the Database:**
    ```bash
    python backend/database/init_db.py
    ```

6.  **Run the Backend Server:**
    ```bash
    python backend/app.py
    ```
    *   The server will start at `http://127.0.0.1:5000`.

---

### 2. Frontend Setup (React Dashboard)

The frontend provides a modern web interface for users to sign up, file claims, and track status.

1.  **Open a new terminal and navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node dependencies:**
    ```bash
    npm install
    ```

3.  **Run the Frontend Development Server:**
    ```bash
    npm run dev
    ```
    *   The frontend will start at `http://localhost:5173`.

---

## 🎮 How to Use

### 1. User Registration & Login
*   Open `http://localhost:5173` in your browser.
*   Click **Sign Up** to create a new account.
*   Enter your Name, Email, Phone Number, and a secure Password.
*   Once registered, you will be redirected to your Dashboard.

### 2. File a New Claim
*   From the **Dashboard**, click **"New Claim"** (or "File a Claim" from the Home page).
*   Enter your Flight Details:
    *   **Flight Number** (e.g., `6E-234`)
    *   **Date of Travel**
    *   **Airline Name**
    *   **Reason** (Delay, Cancellation, etc.)
*   Click **Submit Claim**.

### 3. Track Your Claim
*   After submission, you will be redirected to the **Tracking Page**.
*   You will see a **Claim Reference Number** (e.g., `FC-20251028-6E-234-0001`).
*   You can return to this page anytime by entering your Reference Number on the "Track Claim" page.
*   The timeline shows the current status:
    *   **Submitted:** Claim received.
    *   **In Review:** AI is verifying eligibility and generating documents.
    *   **Approved/Rejected:** Final decision from the airline/DGCA.

### 4. Dashboard Overview
*   The **Dashboard** lists all your submitted claims.
*   View status badges (e.g., "Initiated", "Submitted to Airline", "Resolved") at a glance.
*   Click on any claim to view detailed tracking information.

---

## 🛠️ Troubleshooting

*   **Backend won't start?**
    *   Check if the virtual environment is activated.
    *   Ensure all dependencies are installed (`pip install -r requirements.txt`).
    *   Check if port 5000 is free.

*   **Frontend can't connect to Backend?**
    *   Ensure the backend server is running on `http://127.0.0.1:5000`.
    *   Check the browser console (F12) for CORS errors. (CORS is enabled by default in `app.py`).

*   **Database errors?**
    *   If you changed the schema, delete `flyclaim.db` and re-run `python backend/database/init_db.py`.

---

**Built with ❤️ for Indian Travelers.**
