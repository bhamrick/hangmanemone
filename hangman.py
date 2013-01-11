import random, re #, irc

class Hangman():
    def __init__(self, mysteries):
        self.mystery_dict = mysteries
        self.mystery_name = None
        self.mystery = None

    def _match(self, connection, env, message, regex): 
        # match string, regex
        print "Attempting to match %r with %r" % (message, regex)
        return re.search(regex, message)
        
    def _say(self, connection, env, msg): 
        # say message
        # send a message to the channel from which
        # the event came, which is in env["channel"]

        #chan = env["channel"]
        #connection.privmsg(chan, msg)
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
            return True
        else:
            print "No more cards left!"
            return False

    def add_clue(self, connection, env): 
        new_attribute = self.random_key(self.mystery)
        if (new_attribute != None):
            new_clue = self.mystery.pop(new_attribute)
            msg = "New clue: "+ str(new_attribute)+ " is " + str(new_clue)+ "."
            self._say(connection, env, msg) #connection, env, msg)
            return True
        else:
            msg = "No hints left!"
            self._say(connection, env, msg) #connection, env, msg)
            return False

    def mystery_solved(self, message, connection, env): #should be called upon each new chat entry
        if (self._match(connection, env, message, self.mystery_name)): #connection, env, message, self.mystery)): #idk what to pass in for "message"
            print "match found!"
            self.mystery_dict.pop(self.mystery_name) #if so, pop current mystery off mystery_dict
            # say who won and what the card was
            self.pick_mystery() #go get new mystery
        return

hana_kami = {"Card Type": "Creature - Spirit", "CMC": "1", "Color": "Green", 
             "Rarity": "Uncommon", "Flavor Text": "It grew in lands lit by pride and watered by tears.", 
             "Artist": "Rebecca Guay", "Set": "Champions of Kamigawa", "Power/Toughness": "1/1"}

faerie_tauntings = {"Card Type": "Tribal Enchantment - Faerie", "CMC": "3", "Color": "Black",
                    "Rarity": "Uncommon", "Flavor Text": "Beneath the fae's constant pranks runs a subtler undercurrent of mockery: the unfluence of Oona, their hidden queen.",
                    "Artist": "Michael Sutfin", "Set": "Lorwyn"}

myr_incubator = {"Card Type": "Artifact", "CMC": "6", "Color": "Colorless", "Rarity": "Rare",
                 "Artist": "Alex Horley-Orlandelli", "Set": "Mirrodin"}

cards = {"Hana Kami": hana_kami, "Faerie Tauntings": faerie_tauntings, "Myr Incubator": myr_incubator}
test = Hangman(cards)
