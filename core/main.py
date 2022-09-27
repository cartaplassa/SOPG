import secrets
import os
import logging
import json


class Password():
    class Rule:
        def __init__(self, rule_from='', rule_to=''):
            self.rule_from = rule_from
            self.rule_to = rule_to
        
        def get(self):
            return {rule: self.rule_to for rule in self.rule_from.split(',')}


    def leetify(self, word: str) -> str():
        """Iterates through the leetrules dictionary, replaces keys with values
        in a given string.
        """
        leetified = word.replace('-','')
        for before, after in self.result(self.rule_list).items():
            leetified = leetified.replace(before, after)
        return leetified

    def result(self, rule_list: list[Rule]) -> dict[str, str]:
        """Iterates through all replacement rules and combines them to a single
        dictionary. Uses `Rule`'s .get() method.
        """
        result_dict = {}
        if self.config['leetify_var']:
            for each in rule_list:
                result_dict = {**result_dict, **each.get()}
        return result_dict

    def new_sequence(self, source: str) -> list:
        """Checks each word (symbol sequence inside spaces) on whether a
        wordlist with the same name exists. Appends it to a returned list if so
        and ignores it otherwise.
        """
        return [each for each in source.lower().split() \
            if each in list(self.pool.keys())]

    def set_sequence(self, source: str):
        """Expects a string of filenames in `wordlists` folder separated by
        spaces
        
        If the parser doesn't recognize the pattern, no changes occur
        """
        if self.new_sequence(source):
            self.config['sequence'] = source
            self.sequence = self.new_sequence(source)

    def set_special_chars(self, source: str):
        """Expects a string of filenames in `wordlists` folder separated by
        spaces
        
        If the parser doesn't recognize the pattern, no changes occur
        """
        if source:
            self.config['special_chars'] = source

    def generate(self, source: list[str]) -> str:
        """Picks a random word in a given wordlist.
        
        No error handling is implemented. Should only be given a valid source. 
        """
        if self.config['case'] == 'lower':
            return self.leetify(secrets.choice(self.pool[source]).lower())
        elif self.config['case'] == 'capital':
            return self.leetify(secrets.choice(self.pool[source]).lower().capitalize())
        elif self.config['case'] == 'upper':
            return self.leetify(secrets.choice(self.pool[source]).upper())

    def set_case(self, new_case):
        """Also changes case of current password. Will override leetrules.

        May not be useful, but it's better to have it as an option.
        """
        self.config['case'] = new_case
        if new_case == 'lower':
            self.words = [word.lower() for word in self.words]
        elif new_case == 'capital':
            self.words = [word.lower().capitalize() for word in self.words]
        elif new_case == 'upper':
            self.words = [word.upper() for word in self.words]

    def update_dividers(self):
        """Regenerates  only header, dividers, tail
        """
        # Header
        if self.config['header_flag'] == 'random':
            self.config['header'] = secrets.choice(self.config['special_chars'])
        # Dividers
        if self.config['divider_flag'] == 'random':
            self.config['divider'] = secrets.choice(self.config['special_chars'])
        elif self.config['divider_flag'] == 'match header':
            self.config['divider'] = self.config['header']
        # Tail
        if self.config['tail_flag'] == 'random':
            self.config['tail'] = secrets.choice(self.config['special_chars'])
        elif self.config['tail_flag'] == 'match header':
            self.config['tail'] = self.config['header']

    def regen_one(self, which: int):
        """Regenerates the word with the index specified in the attribute.

        Operates w/ indices, not w/ numbers.

        Dividers only regen with the whole sequence, UX-motivated choice
        """
        self.words[which] = self.generate(self.sequence[which])

    def regen_whole(self):
        """Regenerates the whole sequence (every word + header, dividers, tail)
        """
        self.words = []
        for each in self.sequence:
            self.words.append(self.generate(each))
        self.update_dividers()
    
    def use_passphrase(self, passphrase: str):
        self.words = []
        for each in passphrase.split():
            self.words.append(self.leetify(each))
        self.update_dividers()

    def __init__(self):
        self.pool = {}
        # Opening files, populating pool
        for each in os.listdir('./wordlists'):
            with open(f'./wordlists/{each}', 'r') as file:
                self.pool[str(os.path.splitext(each)[0])] = []
                for line in file:
                    self.pool[str(os.path.splitext(each)[0])].append(line.strip())
        with open("./config.json", "r") as file:
            self.config = json.load(file)
        self.sequence = self.new_sequence(self.config['sequence'])
        self.rule_list = []
        for each_from, each_to in self.config["rules_init"].items():
            self.rule_list.append(self.Rule(each_from, each_to))
        # Every `sequence` item corresponds to some key in pool dict
        # That means also to a filename in `wordlists/`
        self.set_sequence('')
        self.regen_whole()

    # Used in legacy main.py to CB copy, might require attention later
    def get(self):
        return ''.join([
            self.config['header'], 
            self.config['divider'].join(self.words), 
            self.config['tail']
        ])

    def __str__(self):
        return self.get()


def print_help(password):
    print('To regenerate a word, enter its number')
    print('r: Regenerate the whole password')
    print('s: Change the words sequence')
    print(f"current sequence: {', '.join(password.sequence)}")
    print('p: Use a passphrase, ps: Set a passphrase')
    print(f"current passphrase: {password.config['passphrase']}")
    print('Change the case:')
    # print('l: lowercase      (example)')
    # print('c: capitalized    (Example)')
    # print('u: uppercase/caps (EXAMPLE)')
    print(f"current case: {password.config['case']}")
    print('sc: Change the special characters pool')
    print(f"current pool: {password.config['special_chars']}")
    print('h: Change the header sequence, hr: Randomize from pool')
    print(f"current header:   {password.config['header'] if password.config['header_flag'] == 'custom' else 'random'}")
    print('d: Change the divider sequence, dr: Randomize from pool, dm: Match the header sequence')
    print(f"current divider: {password.config['divider'] if password.config['divider_flag'] == 'custom' else password.config['divider_flag']}")
    print('t: Change the tail sequence, tr: Randomize from pool, tm: Match the header sequence')
    print(f"current tail:     {password.config['tail'] if password.config['tail_flag'] == 'custom' else password.config['tail_flag']}")
    print(f"l: Toggle leetify function, current state: {('on', 'off')[password.config['leetify_var']]}")
    print('dump: Save configuration')
    print('x: Exit the program')


def set_logger():
    global logger
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s,%(msecs)03d [%(levelname)s]: %(message)s'
    LOG_DATEFMT = "%M:%S"
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    log_handler = logging.StreamHandler()
    log_handler.setLevel(LOG_LEVEL)
    log_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT)
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)


def main():
    set_logger()
    choice = 'r'
    password = Password()
    print_help(password)
    while choice != 'x':

        if choice == 'r':
            password.regen_whole()
        
        elif choice == 's':
            password.set_sequence(input('New words sequence: '))
            password.regen_whole()
        
        elif choice == 'p':
            password.use_passphrase(password.config['passphrase'])
        
        elif choice == 'ps':
            password.config['passphrase'] = input('New passphrase: ')
            password.use_passphrase(password.config['passphrase'])
        
        elif choice == 'l':
            password.set_case('lower')
        
        elif choice == 'c':
            password.set_case('capital')
        
        elif choice == 'u':
            password.set_case('upper')
        
        elif choice == 'h':
            password.config['header_flag'] = 'custom'
            password.config['header'] = input('New header sequence: ')
        
        elif choice == 'hr':
            password.config['header_flag'] = 'random'
            password.config['header'] = secrets.choice(password.config['special_chars'])
            if password.config['divider_flag'] == 'match header':
                password.config['divider'] = password.config['header']
            if password.config['tail_flag'] == 'match header':
                password.config['tail'] = password.config['header']
        
        elif choice == 'd':
            password.config['divider_flag'] = 'custom'
            password.config['divider'] = input('New division sequence: ')
        
        elif choice == 'dr':
            password.config['divider_flag'] = 'random'
            password.config['divider'] = secrets.choice(password.config['special_chars'])
        
        elif choice == 'dm':
            password.config['divider_flag'] = 'match header'
            password.config['divider'] = password.config['header']
        
        elif choice == 't':
            password.config['tail_flag'] = 'custom'
            password.config['tail'] = input('New tail sequence: ')
        
        elif choice == 'tr':
            password.config['tail_flag'] = 'random'
            password.config['tail'] = secrets.choice(password.config['special_chars'])
        
        elif choice == 'tm':
            password.config['tail_flag'] = 'match header'
            password.config['tail'] = password.config['header']
        
        elif choice == 'sc':
            password.set_special_chars(input('New special characters pool: '))
        
        elif choice == 'l':
            password.config['leetify_var'] = not password.config['leetify_var']
        
        elif choice == 'dump':
            with open("./config.json", "w") as f:
                json.dump(password.config, f, indent=4)

        else:
            try:
                # If it's not one of mgmt chars,
                # then check if it's number of word to regen
                password.regen_one(int(choice) - 1)
            # Choice is an int, but out of range
            except IndexError:
                print(f'Tried to regen {choice} out of {len(password.words)} words')
            # Choice is a str, but not recognized
            except ValueError:
                print(f'Input "{choice}" unrecognized')
                print_help(password)
        
        print('Current password:')
        print(password)
        choice = input('User input: ')
        print('_____________________________________________________________')


if __name__ == '__main__':
    main()
