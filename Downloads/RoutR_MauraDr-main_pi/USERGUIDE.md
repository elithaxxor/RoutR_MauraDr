# RoutR_MauraDr User Guide

## Overview
RoutR_MauraDr is a modular, secure, and extensible platform for scanning networks, identifying routers, and running exploits from a managed payloads library—with full UI, API, and backend support for automation and reporting.

---

## Getting Started

### 1. Installation
- Clone the repository:
  ```bash
  git clone <your_repo_url>
  cd RoutR_MauraDr-main_pi
  ```
- Install backend dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Install frontend dependencies:
  ```bash
  cd web/client
  npm install
  ```
- Copy `.env.example` to `.env` and fill in your values.

### 2. Running the Application
- Start backend (Flask + Celery):
  ```bash
  cd web/server
  flask run
  celery -A web.src.tasks.scan_task.celery worker --loglevel=info
  celery -A web.src.tasks.exploit_task.celery worker --loglevel=info
  ```
- Start frontend:
  ```bash
  cd web/client
  npm start
  ```

---

## Usage

### 1. Login
- Access the web UI and log in with your credentials.

### 2. Scan a Network
- Enter a network CIDR and select scan intensity.
- Start the scan and wait for results.

### 3. View Devices & Exploitation
- View discovered devices and their details.
- Select a device to see available exploits (payloads) or choose "All" to run every applicable exploit.
- Trigger exploits and monitor results in real time.

### 4. Results & Reports
- View detailed results for each exploit attempt.
- Download logs and reports as needed.

---

## Advanced Features
- **Payload Management:** Add or modify exploit payloads in the `payloads/` directory. Each payload should include metadata for automated matching.
- **API Access:** Use the REST API for automation or integration with other tools.
- **Security:** All actions are authenticated and logged. Use HTTPS in production.

---

## Troubleshooting
- Ensure all environment variables are set in `.env`.
- Check Celery and Flask logs for errors.
- For database or Redis issues, verify services are running and accessible.

---

## Support
For questions, suggestions, or issues, please open an issue on the GitHub repository or contact the maintainers.
