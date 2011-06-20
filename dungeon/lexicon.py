import string

class Lexicon(object):
    
    def __init__(self):
        self.directions = ["north", "south", "east", "west"]
        self.verbs = ["go", "kill", "eat", "pick", "pickup", "grab", "look", "search", "open", "attack"]
        self.stops = ["the", "in", "of"]
        self.nouns = ["bear", "princess", "door", "sword", "key", "torch"]
        self.joins = ["with"]
        
        
    def scan(self, sentence):
        
        sentence = str(sentence)
        no_punctuation = sentence.translate(string.maketrans("",""),string.punctuation)

        words = no_punctuation.split()
        word_list = []

        for word in words:
            if word.lower() in self.directions:
                description = ('direction', word)
    
            elif word.lower() in self.verbs:
                description = ('verb', word)
        
            elif word.lower() in self.stops:
                description = ('stop', word)
            
            elif word.lower() in self.nouns:
                description = ('noun', word)
        
            elif word.lower() in self.joins:
                description = ('join', word)
        
            elif word.isdigit():
                description = ('number', word)
    
            else:
                description = ('error', word)
    
            word_list.append(description)

        return word_list



    def peek(self, word_list):
        if word_list:
            word = word_list[0]
            return word[0]
        else:
            return None

    def match(self, word_list, expecting):
        if word_list:
            word = word_list.pop(0)
    
            if word[0] == expecting:
                return word
            else:
                return None
        else:
            return None

    def skip(self, word_list, word_type):
        while self.peek(word_list) == word_type:
            self.match(word_list, word_type)
    
    def skip_all(self, word_list):
        while True:
            if self.peek(word_list) == 'stop':
                self.match(word_list, 'stop')
            elif self.peek(word_list) == 'error':
                self.match(word_list, 'error')
            else:
                return
                    
    def parse_verb(self, word_list):
        self.skip_all(word_list)

        if self.peek(word_list) == 'verb':
            return self.match(word_list, 'verb')
        else:
            raise ParseError("Expected a verb next.")
        
    def parse_object(self, word_list):
        self.skip_all(word_list)
        next = self.peek(word_list)

        if next == 'noun':
            return self.match(word_list, 'noun')
        elif next == 'direction':
            return self.match(word_list, 'direction')
        else:
            return ('noun', 'room')
    
    def parse_item(self, word_list):
        self.skip(word_list, 'join')
        self.skip_all(word_list)

        if self.peek(word_list) == 'noun':
            return self.match(word_list, 'noun')
        else:
            raise ParseError("Expected a noun next.")

    def parse_subject(self, word_list, subj):
        verb = self.parse_verb(word_list)
        obj = self.parse_object(word_list)
        
        if self.peek(word_list) == 'join':
            item = self.parse_item(word_list)
            return Sentence(subj, verb, obj, item)
        else:
            return Sentence(subj, verb, obj)

    def parse_sentence(self, sentence):

        word_list = self.scan(sentence)

        self.skip_all(word_list)

        start = self.peek(word_list)

        if start == 'noun':
            subj = self.match(word_list, 'noun')
            return self.parse_subject(word_list, subj)
        elif start == 'verb':
            # assume the subject is the player then
            return self.parse_subject(word_list, ('noun', 'player'))
        else:
            raise ParseError("Must start with subject, object, or verb not: %s" % start)

class ParseError(Exception):
    pass

class Sentence(object):
    
    
    def __init__(self, subject, verb, object, item=False):
        # remember we take ('noun', 'princess') tuples and convert them
        self.subject = subject[1]
        self.verb = verb[1]
        self.object = object[1]
        if item:
            self.item = item[1]

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
            
       