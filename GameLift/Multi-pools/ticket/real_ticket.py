import json, os, random
import string
import uuid
import boto3

class RealTicket():
  players = []
  teams = ['cowboys', 'aliens']

  def __init__(self, name):
    self.gamelift = boto3.client('gamelift')
    self.machmakingConfigurationName = name
    pass

  def call(self):
    print("RealTicket")

  def mockPlayer(self):
    playerId = str(uuid.uuid4())
    skillVal = random.randint(1, 100)
    team = random.choice(self.teams)
    player = {
        'PlayerId': playerId,
        'PlayerAttributes': {
            'skill': {
                'N': skillVal
            }
        },
        'Team': team
    }
    return player

  def mockPlayers(self, size):
    for i in range(size):
      self.players.append(self.mockPlayer())
    pass

  def startMatchmaking(self, size):
    self.mockPlayers(size)
    response = self.gamelift.start_matchmaking(
      ConfigurationName=self.machmakingConfigurationName,
      Players=self.players
    )
    print(response)
