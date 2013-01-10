#!/usr/bin/env python
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

from conf import BotConfig

DEBUG = True

class Hangmanemone(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667, password=None):
        print "Initializing"
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + '_')

    def log_event(self,e):
        if DEBUG:
            print e.type
            print e.source
            print e.target
            print e.arguments
            print ""

    def on_welcome(self, c, e):
        self.log_event(e)
        c.execute_delayed(1, c.join, (self.channel,))

    def on_namreply(self, c, e):
        self.log_event(e)

    def on_endofnames(self, c, e):
        self.log_event(e)

    def on_join(self, c, e):
        self.log_event(e)

    def on_pubmsg(self, c, e):
        self.log_event(e)

    def on_privmsg(self, c, e):
        self.log_event(e)

    def on_pubnotice(self, c, e):
        self.log_event(e)

    def on_privnotice(self, c, e):
        self.log_event(e)

    def on_error(self, c, e):
        self.log_event(e)

    def on_ping(self, c, e):
        self.log_event(e)

    def on_pong(self, c, e):
        self.log_event(e)

    def on_mode(self, c, e):
        self.log_event(e)

    def on_disconnect(self, c, e):
        self.log_event(e)

def main():
    import sys
    if len(sys.argv) < 2:
        print "Usage: bot <config file>"

    conf = BotConfig()
    conf.parseFile(sys.argv[1])

    bot = Hangmanemone(conf.channel,
                    conf.nick,
                    conf.server,
                    conf.port,
                    conf.password)
    bot.start()

if __name__ == "__main__":
    main()
