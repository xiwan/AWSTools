import boto3
import json
import random
import os
import sys
import argparse
import time


def prefix_handler(region, filepath, filename, max_entries, target_prefix_list_id):
  client = boto3.client('ec2', region_name=region)

  csvfile = open(filepath,'r')
  lines = csvfile.readlines()
  entries = []
  row = 0

  for line in lines:
    if row > 0:
      if len(line.split(",")) < 2:
        line += ","
      entry = {
        'Cidr': line.split(",")[0].replace("\n", ""),
        'Description': line.split(",")[1].replace("\n", "")
      }
      entries.append(entry)
    row += 1
  print(entries)

  if (len(target_prefix_list_id) == 0):
    response = client.create_managed_prefix_list(
      # DryRun = True,
      PrefixListName = filename.split(".")[0],
      MaxEntries = max_entries,
      AddressFamily = 'IPv4',
      Entries = entries
    )
    print(json.dumps(response['PrefixList'], indent=2))

  else:
    response = client.get_managed_prefix_list_entries(
      PrefixListId=target_prefix_list_id
    )

    removeArry = []
    for entry in response['Entries']:
      removeArry.append({"Cidr": entry["Cidr"]})
    
    # remove old entries
    if len(removeArry) > 0:
      response = client.describe_managed_prefix_lists(
        PrefixListIds=[target_prefix_list_id]
      )
      state = response['PrefixLists'][0]['State']
      version = response['PrefixLists'][0]['Version']

      response = client.modify_managed_prefix_list(
        PrefixListId=target_prefix_list_id,
        #AddEntries=entries,
        RemoveEntries=removeArry,
        CurrentVersion=version
      )

    # check the state
    state = ''
    version = 0
    trytime = 0
    while state != 'modify-complete' and trytime <10:
      response = client.describe_managed_prefix_lists(
        PrefixListIds=[target_prefix_list_id]
      )
      state = response['PrefixLists'][0]['State']
      version = response['PrefixLists'][0]['Version']
      trytime += 1

    # add new entries
    response = client.modify_managed_prefix_list(
      PrefixListId=target_prefix_list_id,
      AddEntries=entries,
      #RemoveEntries=removeArry,
      CurrentVersion=version
    )

    print(json.dumps(response['PrefixList'], indent=2))


def script_handler(region, path, max_entries, target_prefix_list_id):

  if path.endswith(".csv"):
    filename = os.path.basename(path)
    prefix_handler(region, path, filename, max_entries, target_prefix_list_id)
  else:
    dir_list = os.listdir(path)
    for filename in dir_list:
      if filename.endswith(".csv"):
        filepath = os.path.join(path, filename)
        prefix_handler(region, filepath, filename, max_entries, target_prefix_list_id)

  pass

        
parser = argparse.ArgumentParser(description='create prefix list on any aws region')
parser.add_argument('--region', type=str, help='target region: like us-east-1 or us-east-2')
parser.add_argument('--path', type=str, help='the local folder path of csv files')
parser.add_argument('--max_entries', type=int, help='prefix list max_entries', nargs='?', default=50)
parser.add_argument('--target_prefix_list_id', type=str, help='target prefix list id', nargs='?', default='')
args = parser.parse_args()

# path="/Users/benxiwan/Downloads/us-east-2/"
script_handler(args.region, args.path, args.max_entries, args.target_prefix_list_id)