# venmo-autopay [![run venmo-autopay](https://github.com/RileyMartinez/venmo-autopay/actions/workflows/actions.yml/badge.svg)](https://github.com/RileyMartinez/venmo-autopay/actions/workflows/actions.yml)
Automate Venmo payments on a schedule using GitHub Actions:
- main.py
  - Sends payments and requests via Venmo client
  - Sends success/failure email notifications via SmtpClient
  - Appends successful/failed transactions to main.log as a keep-alive for GitHub Actions
- smtp_client.py
  - SMTP client wrapper for sending emails
- venmo.py
  - Venmo client wrapper for sending/receiving payments
- example.env
  - Env template for required variables and secrets
- pyproject.toml and poetry.lock
  - Uses Poetry for venv and dependency management
  - See https://python-poetry.org/docs/
- .github/workflows/actions.yml
  - CI pipeline to run venmo-autopay on a monthly basis
  - Utilizes caching for faster runs
