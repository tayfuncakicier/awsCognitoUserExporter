import boto3
import datetime
import time
from colorama import Fore

#you should write your region info
REGION = 'eu-west-1'
USER_POOL_ID = ''
LIMIT = 60
MAX_NUMBER_RECORDS = 0
REQUIRED_ATTRIBUTE = ["-attr", "name", "family_name", "phone_number", "UserStatus", "Enabled"]
CSV_FILE_NAME = 'all-users.csv'
USER_POOL_NAME = ''
NEXT_TOKEN = ''

csv_file = open(CSV_FILE_NAME, 'w')
client = boto3.client('cognito-idp', REGION)

#step:1 user pool list import.
with open('user-pools.txt', 'w') as f:
    while NEXT_TOKEN is not None:
        userPoolsResponse = client.list_user_pools(MaxResults = LIMIT) if NEXT_TOKEN == '' else client.list_user_pools(MaxResults = LIMIT, NextToken = NEXT_TOKEN)
        userPools = list(userPoolsResponse['UserPools'])
        for userPool in userPools:
            f.write(userPool['Id'] + ' ' + userPool['Name'])
            f.write('\n')
        NEXT_TOKEN = userPoolsResponse['NextToken'] if "NextToken" in userPoolsResponse else None
        print(Fore.YELLOW + "INFO: " + userPools.__len__().__str__() + " user pools imported" )
print(Fore.GREEN + "INFO: User Pool List succesfully imported!")
f.close()

#step:2 import users for all user pools
with open('user-pools.txt') as userPoolsListFile:
    userPoolList = userPoolsListFile.readlines()
    userPoolsListFile.close()

    for userpool in userPoolList:
        USER_POOL_ID = userpool.split()[0]
        USER_POOL_NAME = userpool.split()[1]
        REQUIRED_ATTRIBUTE.append('UserPoolName')
        csv_new_line = {REQUIRED_ATTRIBUTE[i]: '' for i in range(len(REQUIRED_ATTRIBUTE))}
        csv_file.write(",".join(csv_new_line.keys()) + '\n')
        USER_POOL_ID = userpool.split()[0]               
        def datetimeconverter(o):
            if isinstance(o, datetime.datetime):
                return str(o)
        def get_list_cognito_users(cognito_idp_cliend, next_pagination_token ='', limit = LIMIT):  
            return client.list_users(
                UserPoolId = USER_POOL_ID,
                Limit = limit,
                PaginationToken = next_pagination_token
            ) if next_pagination_token else client.list_users(
                UserPoolId = USER_POOL_ID,
                Limit = limit
            )

        pagination_counter = 0
        exported_records_counter = 0
        pagination_token = ""
        while pagination_token is not None:
            csv_lines = []
            try:
                user_records = get_list_cognito_users(
                    cognito_idp_cliend = client,
                    next_pagination_token = pagination_token,
                    limit = LIMIT if LIMIT < MAX_NUMBER_RECORDS else MAX_NUMBER_RECORDS
                )
            except client.exceptions.ClientError as err: 
                error_message = err.response["Error"]["Message"]
                print(Fore.RED + "Please Check your Cognito User Pool configs")
                print("Error Reason: " + error_message)
                csv_file.close()
                exit()
            except:
                print(Fore.RED + "Something else went wrong")
                csv_file.close()
                raise
            if set(["PaginationToken","NextToken"]).intersection(set(user_records)):
                pagination_token = user_records['PaginationToken'] if "PaginationToken" in user_records else user_records['NextToken']
            else:
                pagination_token = None
            for user in user_records['Users']:
                csv_line = csv_new_line.copy()
                for requ_attr in REQUIRED_ATTRIBUTE:
                    csv_line[requ_attr] = ''
                    if requ_attr in user.keys():
                        csv_line[requ_attr] = str(user[requ_attr])
                        continue
                    for usr_attr in user['Attributes']:
                        if usr_attr['Name'] == requ_attr:
                            csv_line[requ_attr] = str(usr_attr['Value'])
                csv_line['UserPoolName'] = USER_POOL_NAME
                csv_lines.append(",".join(csv_line.values()) + '\n')       
            csv_file.writelines(csv_lines)
            pagination_counter += 1
            exported_records_counter += len(csv_lines)
            print(Fore.YELLOW + "Page: #{} \n Total Exported Records: #{} \n".format(str(pagination_counter), str(exported_records_counter)))
            if MAX_NUMBER_RECORDS and exported_records_counter >= MAX_NUMBER_RECORDS:
                print(Fore.GREEN + "INFO: Max Number of Exported Reached")
                break    
            if pagination_token is None:
                print(Fore.GREEN + "INFO: End of Cognito User Pool reached")
            time.sleep(0.15)
    
csv_file.close()        