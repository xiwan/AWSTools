import boto3
import json
import random
import os
import sys
import argparse
import time
from pprint import pprint

def main(region, identity_store_id, user_name, group_name):
    sso_identitystore = boto3.client('identitystore', region_name=region)
    sso_admin_client = boto3.client('sso-admin', region_name=region)

    if len(user_name) == 0 and len(group_name) == 0:
        print("user_name or group_name is required")
        return
    
    principalId = ''
    filter = []
    if len(user_name) > 0:
        filter.append({'AttributePath': 'UserName', 'AttributeValue': user_name})
        users = sso_identitystore.list_users(IdentityStoreId=identity_store_id, Filters=filter)
        for user in users['Users']:
            principalId = user['UserId']
            break

    if len(group_name) > 0:
        filter.append({'AttributePath': 'DisplayName', 'AttributeValue': group_name})
        groups = sso_identitystore.list_groups(IdentityStoreId=identity_store_id, Filters=filter)
        for group in groups['Groups']:
            principalId = group['GroupId']
            break
    
    if len(principalId) == 0 :
        print("not found valid user or group")
        return
    print(f'principalId: {principalId}')

    results = sso_admin_client.list_instances()
    for instance in results['Instances']:
        print(f'instance: {instance}')

        permissionsets_dict = []
        permissionsets = sso_admin_client.list_permission_sets(
            InstanceArn=instance['InstanceArn'], 
            MaxResults=100)
        permissionsets_dict += permissionsets['PermissionSets']
        while 'NextToken' in permissionsets:
            permissionsets = sso_admin_client.list_permission_sets(
                InstanceArn=instance['InstanceArn'], 
                NextToken=permissionsets['NextToken'], 
                MaxResults=100)
            permissionsets_dict += permissionsets['PermissionSets']
            pass
        
        # print(f'permissionsets_dict length: {len(permissionsets_dict)}')

        for permissionset in permissionsets_dict:
            # print(f'permissionset: {permissionset}')
            permissionsets_account_dict = []
            permissionsets_account = sso_admin_client.list_accounts_for_provisioned_permission_set(
                InstanceArn=instance['InstanceArn'], 
                PermissionSetArn=permissionset, 
                MaxResults=100)
            permissionsets_account_dict += permissionsets_account['AccountIds']
            while 'NextToken' in permissionsets_account:
                permissionsets_account = sso_admin_client.list_accounts_for_provisioned_permission_set(
                    InstanceArn=instance['InstanceArn'], 
                    PermissionSetArn=permissionset, 
                    NextToken=permissionsets_account['NextToken'], 
                    MaxResults=100)
                permissionsets_account_dict += permissionsets_account['AccountIds']
                pass

            for accountsId in permissionsets_account_dict:
                # print(accountsId)
                assignments_dict = []
                assignments = sso_admin_client.list_account_assignments(
                    AccountId=accountsId,
                    InstanceArn=instance['InstanceArn'], 
                    PermissionSetArn=permissionset,
                    MaxResults=100)
                assignments_dict += assignments['AccountAssignments']
                while 'NextToken' in assignments:
                    assignments = sso_admin_client.list_account_assignments(
                        AccountId=accountsId,
                        InstanceArn=instance['InstanceArn'], 
                        PermissionSetArn=permissionset,
                        NextToken=assignments['NextToken'], 
                        MaxResults=100)
                    assignments_dict += assignments['AccountAssignments']
                    pass

                for assignment in assignments_dict:
                    # print(assignment['PrincipalType'], assignment['PrincipalId'])
                    if assignment['PrincipalId'] == principalId:
                        permissiondata = sso_admin_client.describe_permission_set(
                            InstanceArn=instance['InstanceArn'], 
                            PermissionSetArn=permissionset)
                        print(f'======== {assignment["PrincipalType"]} {assignment["PrincipalId"]} =========')
                        pprint(permissiondata["PermissionSet"], indent=2)
                        pass
                pass
            pass
        pass
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create prefix list on any aws region')
    parser.add_argument('--region', type=str, help='target region: like us-east-1 or us-east-2', default='us-east-1')
    parser.add_argument('--identity-store-id', type=str, help='the identity store id', required=True)
    parser.add_argument('--user-name', type=str, help='search user name', nargs='?', default='')
    parser.add_argument('--group-name', type=str, help='search group name', nargs='?', default='')
    args = parser.parse_args()
    
    main(args.region, args.identity_store_id, args.user_name, args.group_name)

    pass