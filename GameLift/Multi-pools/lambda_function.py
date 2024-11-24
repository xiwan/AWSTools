import json, os, time

from ticket import main_ticket

def lambda_handler(event, context):
    main_ticket.startMatchmaking()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }