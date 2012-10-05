#!/usr/bin/env python
import json
import requests
import logging
import Colorer
import random

def main():
    logging.basicConfig(format="%(asctime)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    client = Client("http://localhost:6969")
    client.connect() # this will block until the game starts
    logging.debug(str(client.game_status()))
    while client.alive():
        client.attack(1,0, random.randrange(1,4), random.randrange(0,4))

class Client(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.player_id = None
        self.auth = None


    def connect(self):
        """ Connect to the game server.
        This function will BLOCK until the game starts. Don't freak out.
        """
        logging.info("Connecting to server, waiting response for game to begin...")
        r = requests.post(self.endpoint + '/connect')
        logging.debug(str(r.json))
        logging.info("Connected! player id: %s, auth: %s", r.json['id'], r.json['auth'])
        self.player_id, self.auth = r.json['id'], r.json['auth']

    def game_status(self):
        """ Get the status of the current game.
        Returns back a list of tuples [(id,health),...] where id is the player_id,
        and health is that player's current health.
        """
        payload = {'id': self.player_id, 'auth': self.auth}
        r = requests.post(self.endpoint + '/game/status', data=json.dumps(payload))
        return r.json

    def attack(self, level, spec, target_id, path):
        payload = {'id': self.player_id, 'auth': self.auth, 'level': level, 'spec': spec, 'target_id': target_id, 'path': path}
        r = requests.post(self.endpoint + '/unit/create', data=json.dumps(payload))

    def alive(self):
        payload = {'id': self.player_id, 'auth': self.auth}
        r = requests.post(self.endpoint + '/player/'+str(self.player_id), data=json.dumps(payload))
        print str(r.json)
        return r.json['health']>0

if __name__ == "__main__":
    main()
