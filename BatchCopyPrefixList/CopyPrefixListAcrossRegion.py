import boto3
import json
import random
import time
import sys
import argparse

def script_handler(events, context):
  RegionFrom = events.RegionFrom
  RegionTo = events.RegionTo
  PrefixListIds = events.PrefixListIds
  #MaxEnties = events['MaxEnties']

  clientFrom = boto3.client('ec2', region_name=RegionFrom)
  clientTo = boto3.client('ec2', region_name=RegionTo)

  response = {}
  if not PrefixListIds:
    response = clientFrom.describe_managed_prefix_lists()
  else:
    response = clientFrom.describe_managed_prefix_lists(PrefixListIds=PrefixListIds.split(','))
  
  # print(json.dumps(response['PrefixLists'], indent=2))

  for prefix in response['PrefixLists']:
    if prefix['OwnerId'] != 'AWS':
      data = clientFrom.get_managed_prefix_list_entries(PrefixListId=prefix['PrefixListId'])

      res = clientTo.create_managed_prefix_list(
        # DryRun = True,
        PrefixListName = prefix['PrefixListName'],
        MaxEntries = prefix['MaxEntries'],
        AddressFamily = prefix['AddressFamily'],
        Entries = data['Entries']
      )

      print(json.dumps(res['PrefixList'], indent=2))

  pass

parser = argparse.ArgumentParser(description='copy prefix list to any aws region')
parser.add_argument('--RegionFrom', type=str, help='origin region: like us-east-1 or us-east-2')
parser.add_argument('--RegionTo', type=str, help='target region: like us-east-1 or us-east-2')
parser.add_argument('--PrefixListIds', type=str, help='prefix list max_entries', nargs='?')
args = parser.parse_args()

script_handler(args, context)

