# LicenseShrinker-AI
AI-powered Slack license optimizer using AWS Lambda, DynamoDB, SNS
# LicenseShrinker AI

> 💸 Cut SaaS waste with AI! Automatically detect and report inactive Slack users using AWS Lambda + DynamoDB + SNS.

## 🔥 Inspiration
Enterprises lose millions on unused SaaS licenses every year. Inspired by this challenge, we built **LicenseShrinker AI**, a lightweight serverless solution to track user activity, estimate savings, and reduce waste.

## 🛠️ How It Works
1. A Lambda function runs weekly (via EventBridge).
2. It checks Slack for active users using the Slack API.
3. It updates a DynamoDB table with weekly usage.
4. After 4 weeks, it flags inactive users and:
   - Sends them Slack DMs asking if they need the license
   - Emails a savings report via SNS to the admin

## 📦 Built With
- **AWS Lambda**
- **AWS DynamoDB**
- **Amazon SNS**
- **EventBridge**
- **Slack API**
- **Python**
- **Boto3 + Requests**

## 🎯 Features
- Tracks usage weekly for Slack
- Flags inactive users after 4 weeks
- Sends cost-saving reports via email
- Messages inactive users via Slack bot


## 🧠 What We Learned
- Mastered AWS Lambda + IAM roles and permissions
- Integrated Slack API with secure tokens
- Automated multi-step pipelines with EventBridge + SNS

## 🏆 Accomplishments
- Fully functional cost-saving tracker
- Serverless and scalable with no maintenance
- Sleek automation via Slack messages

## 🔮 What's Next
- Zoom API integration for multi-app license tracking
- Analytics dashboard for HR/admins
- Secrets Manager integration for better security



---

