#!/bin/python
# Passes recognized commands from the chat to a web api.
# The web script handles the command in some way and issues a response.
# This bot posts the response in chat (or uses it to answer the private message).

import mumble
import sys
import requests


class HTTPBot(mumble.Bot):
    def __init__(self, script_url):
        mumble.Bot.__init__(self)
        self.script_url = script_url

    def stopping(self):
        self.thread.keep_going = False

    def on_text_message(self, from_user, to_users, to_channels, tree_ids, message):
        private_message = to_channels == []
        response_target = from_user if private_message else to_channels[0]  # self.state.channel

        # THIS WOULD BE THE NOT-SO-CLEVER COMMAND BOT
        # is_command = message[0] == '/' or message[0] == '!'

        # if is_command:
        #    self.execute_http_command(response_target, message[1:], from_user, private_message)

        self.execute_http_command(response_target, message, from_user, private_message)

    def execute_http_command(self, response_target, command, from_user, private_message):
        url = 'http://' + self.script_url
        form = {'command': command, 'user': from_user.name, 'private': private_message}
        r = requests.post(url, data=form)
        if r.text:
            print r.text
            self.send_message(r.text, channel=response_target)
        # else:
        #    print "No Response."


if __name__ == '__main__':
    server = sys.argv[1]
    script = sys.argv[2]
    r1 = requests.get('http://' + script)
    script_data = r1.json()

    # Start the bot
    bot = HTTPBot(script)
    bot.start(mumble.Server(server), script_data["name"])
    bot.join() # This will wait until the bot is kicked or leave.
