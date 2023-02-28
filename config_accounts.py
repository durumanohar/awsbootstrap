import boto3

client = boto3.client('organizations')

# Create new AWS account
response = client.create_account(
    Email='example@example.com',
    AccountName='example-account',
    IamUserAccessToBilling='ALLOW'
)

# Get account creation status
account_id = response['CreateAccountStatus']['AccountId']
status = response['CreateAccountStatus']['State']

# Wait for account creation to complete
while status == 'IN_PROGRESS':
    response = client.describe_create_account_status(
        CreateAccountRequestId=response['CreateAccountStatus']['Id']
    )
    status = response['CreateAccountStatus']['State']

# Enable GuardDuty and Config Rules for the new account
client = boto3.client('controltower')

response = client.update_managed_account(
    AccountId=account_id,
    AddManagedAccountRuleNames=[
        'AWS-GuardDuty-Org-Level',
        'AWS-ConfigRules-IAMPasswordPolicy',
        'AWS-ConfigRules-MFAEnabledForConsoleAccess',
    ]
)
