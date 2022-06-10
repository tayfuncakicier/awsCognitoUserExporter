import boto3

client = boto3.client('cognito-idp', 'eu-west-1')
response = client.admin_update_user_attributes(
    UserPoolId='user-pool-id',
    Username='username',
    UserAttributes=[
        {
            'Name': 'phone_number_verified',
            'Value': 'true'
        },
    ]
)
