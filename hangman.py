import random, re #, irc
import time

BASE_TIME = 10
TIME_INCREMENT = 5
POLL_RATE = 1

class Hangman():
    def __init__(self, mysteries):
        self.mystery_dict = mysteries
        self.mystery_name = None
        self.mystery = None
        self.last_clue = 0
        self.next_timedelay = BASE_TIME
        self.num_mysteries = 0

    def _match(self, connection, env, message, pattern):
        if not pattern:
            return False
        # match string, regex
        print "Attempting to match %r with %r" % (message, pattern)
        keep_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        # Canonicalize both strings
        message = message.strip().lower()
        pattern = pattern.strip().lower()
        message = filter(lambda x: x in keep_chars, message)
        pattern = filter(lambda x: x in keep_chars, pattern)
        return message == pattern
        
    def _say(self, connection, env, msg): 
        # say message
        # send a message to the channel from which
        # the event came, which is in env["channel"]

        if len(msg) > 500:
            msg = msg[:500]
        chan = env["channel"]
        connection.privmsg(chan, msg)
        #print "Saying %r to %r" % (msg, chan)
        print msg
        return 
       
    def random_key(self, dictionary): #pick a random key from a dictionary's keys
        print "selecting random key"
        if (len(dictionary) > 0):
            return dictionary.keys()[random.randint(0, len(dictionary) - 1)]
        else:
            return None
        
    def pick_mystery(self, connection, env):
        self.mystery_name = self.random_key(self.mystery_dict)
        if (self.mystery_name != None):
            self.mystery = self.mystery_dict[self.mystery_name]
            print "Mystery is ", self.mystery_name
            self._say(connection, env, "I am thinking of a card.")
            self.next_timedelay = BASE_TIME
            self.add_clue(connection, env)
            return True
        else:
            print "No more cards left!"
            return False

    def add_clue(self, connection, env): 
        cur_time = time.time()
        connection.execute_delayed(POLL_RATE, self.add_clue, (connection, env))
        if cur_time > self.last_clue + self.next_timedelay:
            new_attribute = self.random_key(self.mystery)
            if (new_attribute != None):
                new_clue = self.mystery.pop(new_attribute)
                msg = "New clue: "+ str(new_attribute)+ " is " + str(new_clue)+ "."
                self._say(connection, env, msg)
                self.last_clue = cur_time
                self.next_timedelay += TIME_INCREMENT
                return True
            else:
                msg = "Nobody got it! The card was %s" % self.mystery_name
                self._say(connection, env, msg)
                self.pick_mystery(connection, env)
                return False

    def mystery_solved(self, connection, env): #should be called upon each new chat entry
        if (self._match(connection, env, env["message"], self.mystery_name)): #connection, env, message, self.mystery)): #idk what to pass in for "message"
            print "match found!"
            self.mystery_dict.pop(self.mystery_name) #if so, pop current mystery off mystery_dict
            # say who won and what the card was
            self._say(connection, env, "%s was correct. The card was %s" % (env["user"], self.mystery_name))
            self.num_mysteries -= 1
            if self.num_mysteries > 0:
                self.pick_mystery(connection, env)
        return
