import boto3
import json
import random
import os
import sys
import argparse

def script_handler(region, path, max_entries):

  dir_list = os.listdir(path)
   
  # prints all files
  for filename in dir_list:
    if filename.endswith(".csv"):
      #print(filename)
      csvfile = open(os.path.join(path, filename))
      lines = csvfile.readlines()
      entries = []
      count = 0
      for line in lines:
        if count > 0:
          # print(line)
          entry = {
            'Cidr': line.split(",")[0],
            'Description': line.split(",")[1]
          }
          entries.append(entry)
        count += 1
      print(entries)
      client = boto3.client('ec2', region_name=region)
      response = client.create_managed_prefix_list(
        # DryRun = True,
        PrefixListName = filename.split(".")[0],
        MaxEntries = max_entries,
        AddressFamily = 'IPv4',
        Entries = entries
      )
      print(json.dumps(response['PrefixList'], indent=2))

parser = argparse.ArgumentParser(description='create prefix list on any aws region')
parser.add_argument('--region', type=str, help='target region: like us-east-1 or us-east-2')
parser.add_argument('--path', type=str, help='the local folder path of csv files')
parser.add_argument('--max_entries', type=int, help='prefix list max_entries', nargs='?', default=50)
args = parser.parse_args()

# path="/Users/benxiwan/Downloads/us-east-2/"
script_handler(args.region, args.path, args.max_entries)