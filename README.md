# TEJUSKA Cloud Intelligence
## Enterprise B2B SaaS Platform for Cloud Cost Optimisation

---

## Architecture Overview

| Layer     | Technology                         | Host                        |
|-----------|------------------------------------|-----------------------------|
| Database  | PostgreSQL (Supabase)              | Supabase Cloud              |
| Backend   | FastAPI + Uvicorn                  | Hugging Face Spaces         |
| Frontend  | Streamlit                          | Streamlit Community Cloud   |

---

## Prerequisites

- Python 3.12+
- Supabase account (free tier is sufficient to start)
- Hugging Face account with Spaces access
- Streamlit Community Cloud account linked to GitHub
- Stripe account (for payment webhooks)
- Twilio account (for SMS notifications) - optional
- SMTP credentials (Gmail App Password recommended)

---

## Step 1 - Supabase Database Setup

1. Log in at https://supabase.com and create a new project.
2. Note down:
   - `Project URL` (e.g. `https://xxxx.supabase.co`)
   - `Service Role Key` (Settings > API)
   - `Database Password` (the one you set during project creation — this project uses `4oo05JOHFnFriigF`)
3. Open **SQL Editor** inside Supabase Studio.
4. Paste the entire contents of `database/init_db.sql` and click **Run**.
5. Verify that the tables `tenants`, `subscriptions`, and `consolidated_billing` appear under **Table Editor**.

The DATABASE_URL format used by the backend:
```
postgresql://postgres:4oo05JOHFnFriigF@db.<SUPABASE_PROJECT_REF>.supabase.co:5432/postgres
```

---

## Step 2 - Backend Deployment on Hugging Face Spaces

1. Create a new Space at https://huggingface.co/spaces
   - SDK: **Docker**
   - Visibility: **Public** (or Private with a token)
2. Push all files inside the `backend/` folder to the Space repository:
   ```
   cd backend
   git init
   git remote add origin https://huggingface.co/spaces/<YOUR_HF_USERNAME>/<SPACE_NAME>
   git add .
   git commit -m "Initial backend deployment"
   git push origin main
   ```
3. Inside the Space **Settings > Repository secrets**, add the following secrets:

   | Secret Name          | Value                                      |
   |----------------------|--------------------------------------------|
   | DATABASE_URL         | postgresql://postgres:4oo05JOHFnFriigF@... |
   | OPENAI_API_KEY       | sk-...                                     |
   | SLACK_WEBHOOK_URL    | https://hooks.slack.com/services/...       |
   | SMTP_HOST            | smtp.gmail.com                             |
   | SMTP_PORT            | 587                                        |
   | SMTP_USER            | you@gmail.com                              |
   | SMTP_PASSWORD        | your_app_password                          |
   | TWILIO_ACCOUNT_SID   | ACxxxx                                     |
   | TWILIO_AUTH_TOKEN    | your_token                                 |
   | TWILIO_FROM_NUMBER   | +1234567890                                |
   | STRIPE_SECRET_KEY    | sk_live_...                                |
   | STRIPE_WEBHOOK_SECRET| whsec_...                                  |
   | RAZORPAY_KEY_ID      | rzp_live_...                               |
   | RAZORPAY_KEY_SECRET  | your_razorpay_secret                       |

4. Hugging Face will build the Docker image automatically. The Space URL will be:
   `https://<YOUR_HF_USERNAME>-<SPACE_NAME>.hf.space`

---

## Step 3 - Frontend Deployment on Streamlit Community Cloud

1. Push all files inside the `frontend/` folder to a **public** GitHub repository.
2. Log in at https://share.streamlit.io
3. Click **New app** and point it to:
   - Repository: `<your_github_repo>`
   - Branch: `main`
   - Main file path: `app.py`
4. Under **Advanced settings > Secrets**, add the following in TOML format:

   ```toml
   BACKEND_URL = "https://<YOUR_HF_USERNAME>-<SPACE_NAME>.hf.space"

   [google_oauth]
   client_id     = "your_google_client_id"
   client_secret = "your_google_client_secret"

   [github_oauth]
   client_id     = "your_github_client_id"
   client_secret = "your_github_client_secret"
   ```

5. Click **Deploy**. Streamlit will install dependencies from `requirements.txt` automatically.

---

## Step 4 - Stripe Webhook Configuration

1. In your Stripe Dashboard, go to **Developers > Webhooks**.
2. Add endpoint: `https://<YOUR_HF_USERNAME>-<SPACE_NAME>.hf.space/webhooks/stripe`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
4. Copy the **Signing Secret** and set it as `STRIPE_WEBHOOK_SECRET` in HF Spaces secrets.

---

## Step 5 - Google and GitHub OAuth Setup

**Google:**
1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID (Web Application).
3. Authorised redirect URI: `https://share.streamlit.io/auth/callback`
4. Copy Client ID and Secret to Streamlit secrets.

**GitHub:**
1. Go to https://github.com/settings/developers
2. Register a new OAuth App.
3. Callback URL: `https://share.streamlit.io/auth/callback`
4. Copy Client ID and Secret to Streamlit secrets.

---

## Local Development

```bash
# 1. Clone / enter the project
cd tejuska_saas

# 2. Backend
cd backend
pip install -r requirements.txt
export DATABASE_URL="postgresql://postgres:4oo05JOHFnFriigF@localhost:5432/tejuska"
uvicorn main:app --reload --port 7860

# 3. Frontend (separate terminal)
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
tejuska_saas/
|-- database/
|   `-- init_db.sql
|-- backend/
|   |-- Dockerfile
|   |-- requirements.txt
|   |-- main.py
|   |-- notifications.py
|   |-- ai_engine.py
|   `-- payment_webhooks.py
|-- frontend/
|   |-- requirements.txt
|   |-- app.py
|   |-- pages/
|   |   |-- 1_FinOps_Dashboard.py
|   |   |-- 2_Pro_Automations.py
|   |   |-- 3_AI_Assistant.py
|   |   `-- 4_Upgrade_Plan.py
|   `-- utils/
|       `-- api_client.py
`-- README.md
```
