#  Export Amazon Cognito User Pool records into CSV

This project allows to export user records to CSV file from [Amazon Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)

## Instalation

In order to use this script you should have Python 2 or Python 3 installed on your platform
- run `pip install -r requirements.txt` (Python 2) or `pip3 install -r requirements.txt` (Python 3)

## Run export

To start export process you should run next command (__Note__: use `python3` if you have Python 3 instaled)
- `$ python exportallcognitousers.py
- Wait until you see output `INFO: End of Cognito User Pool reached`
- Find file `all-users.csv` that contains all exported users. [Example](https://github.com/hawkerfun/cognito-csv-exporter/blob/master/CognitoUsers.csv)

## Run Phone Number Verification
To start verificaiton process you should run next command (__Note__: use `python3` if you have Python 3 instaled)
- `$ python phoneNumberVerification.py
# awsCognitoUserExporter
