import json
import boto3
import requests
from datetime import datetime, timedelta

# Get active Slack users
def get_slack_active_users(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://slack.com/api/users.list"
    response = requests.get(url, headers=headers)
    data = response.json()
    users = data.get("members", [])

    active_users = []
    for user in users:
        if not user.get("deleted") and not user.get("is_bot"):
            email = user.get("profile", {}).get("email")
            if email:
                active_users.append(email)
    return active_users

# Send message to inactive user via Slack bot
def notify_user_slack(token, user_email):
    # Get user ID
    user_info = requests.get(
        "https://slack.com/api/users.lookupByEmail",
        headers={"Authorization": f"Bearer {token}"},
        params={"email": user_email}
    ).json()
    
    user_id = user_info.get("user", {}).get("id")
    if not user_id:
        return

    # Send DM
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "channel": user_id,
            "text": "👋 Hey! We noticed you haven’t used Slack in 4 weeks. Do you still need access to your license?"
        }
    )

# Run only on specific days
def should_run_this_week():
    today_day = datetime.utcnow().day
    return today_day in [1, 8, 15, 22]

def lambda_handler(event, context):
    #if not should_run_this_week():
        #return {
            #'statusCode': 200,
            #'body': json.dumps('⏳ Skipped: Not a 4-week schedule day.')
        #}

    # Tokens and setup
    slack_token = "xoxb-123456-your-real-token"  # 🔐 Replace in production with Secrets Manager
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserLicenseUsage')
    sns = boto3.client('sns')
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # Step 1: Get Slack active users
    active_users = get_slack_active_users(slack_token)

    # Step 2: Update activity in DynamoDB
    for email in active_users:
        table.update_item(
            Key={'email': email},
            UpdateExpression="SET service = :s, lastChecked = :d, weeklyUsage = list_append(if_not_exists(weeklyUsage, :empty), :u)",
            ExpressionAttributeValues={
                ':s': 'Slack',
                ':d': today,
                ':u': [1],
                ':empty': []
            }
        )

    # Step 3: Scan and find inactive users
    response = table.scan()
    all_users = response.get('Items', [])
    inactive_users = []

    for user in all_users:
        usage = user.get('weeklyUsage', [])
        if sum(usage[-4:]) == 0:
            inactive_users.append(user['email'])

    # Step 4: Calculate estimated cost savings
    cost_per_license = 8  # in USD or change to INR
    estimated_savings = cost_per_license * len(inactive_users)

    # Step 5: Slack bot messages
    for email in inactive_users:
        notify_user_slack(slack_token, email)

    # Step 6: Email report via SNS
    if inactive_users:
        report_msg = f"""
🧾 Slack License Report

✅ Active Users: {len(active_users)}
❌ Inactive (last 4 weeks): {len(inactive_users)}
💰 Potential Savings: ${estimated_savings}/month

📧 Inactive Emails:
{chr(10).join(inactive_users)}
        """
        sns.publish(
            TopicArn='arn:aws:sns:eu-north-1:074719758593:license-usafe-report',
            Subject='Slack License Optimization Report',
            Message=report_msg
        )

    return {
        'statusCode': 200,
        'body': json.dumps(f"{len(active_users)} active users updated. {len(inactive_users)} inactive users processed.")
    }
