import json, os
import boto3
from .real_ticket import RealTicket

class MainTicket():
  def __init__(self):
    self.gamelift = boto3.client('gamelift')
    self.realtickets = []
    self.realtickets.append(RealTicket('benchmark-configuration-001'))
    pass

  def call(self):
    RealTicket().call()

  def startMatchmaking(self):
    for realtikcet in self.realtickets:
      realtikcet.startMatchmaking(10)
    

main_ticket = MainTicket()