#!/usr/bin/env python
import requests
import logging
import Colorer

def main():
    logging.basicConfig(format="%(asctime)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    client = Client("http://localhost:6969")
    client.connect() # this will block until the game starts
    logging.debug(str(client.game_status()))

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
        r = requests.post(self.endpoint, data=payload)
        return r.json

if __name__ == "__main__":
    main()