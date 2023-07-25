# venmo-autopay
Automate Venmo payments on a schedule using GitHub Actions:
- main.py
  - Sends payments via Venmo client
  - Sends failure email via SMTP client if payment fails
  - Appends successful/failed transactions to status.log as a keep-alive for GitHub Actions
- smtp_client.py
  - SMTP client wrapper for sending emails
- venmo.py
  - Venmo client wrapper for sending payments
- empty.env
  - Env template that contains all necessary env variables and secrets
