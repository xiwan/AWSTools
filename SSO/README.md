# CheckUserPermissionset

## Brief

With this script, you can easily found the related permissionsets for particular user-name or group-name

## implementation 

1. get principal id from user-name/group-name and identity-store-id
> aws identitystore list-users
2. get instanceArn
> aws sso-admin list-instances
3. get all permissionset
> aws sso-admin list-permission-sets
4. get mapping accounts for each permissionset
> aws sso-admin list-accounts-for-provisioned-permission-set
5. get princialId, type could be user or group
> aws sso-admin list-account-assignments
6. get detail info for permissionset
> aws sso-admin describe-permission-set

## arguments

* --identity-store-id: required, depends on your identity source/provider
* --region: default value us-east-1
* --user-name: 
* --group-name:

## Samples

```
python3 CheckUserPermissionsets.py --identity-store-id d-9067446aaa --group-name CostOptimization
```

> principalId: b4089478-40a1-706e-4a44-ccfa3d33bfc0

> instance: {'InstanceArn': 'arn:aws:sso:::instance/ssoins-7223ea8246eb4298', 'IdentityStoreId': 'd-9067446aaa'}

> GROUP b4089478-40a1-706e-4a44-ccfa3d33bfc0

>{'Name': 'management_CostOptimization', 'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223ea8246eb4298/ps-ff6808e746e49166', 'Description': 'management_CostOptimization', 'CreatedDate': datetime.datetime(2022, 11, 28, 14, 23, 57, 115000, tzinfo=tzlocal()), 'SessionDuration': 'PT2H'}

```
python3 CheckUserPermissionsets.py --identity-store-id d-9067446aaa --user-name 5155280
```

> principalId: 74c8d408-40a1-7011-be7b-c87b8dc897ff

> instance: {'InstanceArn': 'arn:aws:sso:::instance/ssoins-7223ea8246eb4298', 'IdentityStoreId': 'd-9067446aaa'}

> USER 74c8d408-40a1-7011-be7b-c87b8dc897ff

> {'Name': 'AdministratorAccess', 'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223ea8246eb4298/ps-a47e33be4456e489', 'CreatedDate': datetime.datetime(2022, 4, 4, 21, 54, 56, 569000, tzinfo=tzlocal()), 'SessionDuration': 'PT1H'}
