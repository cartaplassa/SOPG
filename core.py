import secrets
import os
import logging


class Password():
    def leetify(self, word: str) -> str():
        """Iterates through the leetrules dictionary, replaces keys with values
        in a given string.
        """
        leetified = word.replace('-','')
        for before, after in self.leetrules.items():
            leetified = leetified.replace(before, after)
        return leetified

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
        
        If the parser doesn't recognize the pattern, default string is used
        """
        self.sequence = self.new_sequence(source) if self.new_sequence(source) \
            else self.new_sequence('adj nou ver adv')

    def generate(self, source: list[str]) -> str:
        """Picks a random word in a given wordlist.
        
        No error handling is implemented. Should only be given a valid source. 
        """
        if self.case == 'lower':
            return self.leetify(secrets.choice(self.pool[source]).lower())
        elif self.case == 'capital':
            return self.leetify(secrets.choice(self.pool[source]).lower().capitalize())
        elif self.case == 'upper':
            return self.leetify(secrets.choice(self.pool[source]).upper())

    def set_case(self, new_case):
        """Also changes case of current password. Will override leetrules.

        May not be useful, but it's better to have it as an option.
        """
        self.case = new_case
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
        if self.header_flag == 'random':
            self.header = secrets.choice(self.special_chars)
        # Dividers
        if self.divider_flag == 'random':
            self.divider = secrets.choice(self.special_chars)
        elif self.divider_flag == 'match header':
            self.divider = self.header
        # Tail
        if self.tail_flag == 'random':
            self.tail = secrets.choice(self.special_chars)
        elif self.tail_flag == 'match header':
            self.tail = self.header

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
        for each in os.listdir('wordlists'):
            with open(f'wordlists/{each}', 'r') as file:
                self.pool[str(os.path.splitext(each)[0])] = []
                for line in file:
                    self.pool[str(os.path.splitext(each)[0])].append(line.strip())

        # Defaults. They should be grouped somewhere else, but how exactly?
        # In a dictionary, nested class or something else?
        # Default sequence is set in set_sequence()
        self.leetrules = {
            'O': '0',
            'o': '0',
            'I': '1',
            'i': '1',
            'B': '8',
            'b': '8',
            'S': '$',
            's': '$',
            'L': '!',
            'l': '!'
        }
        self.special_chars = r"~!@#$%^&*/|\-+="
        self.header_flag = 'custom'
        self.header = '~'
        self.divider_flag = 'custom'
        self.divider = '-'
        self.tail_flag = 'custom'
        self.tail = '#'
        self.case = 'capital'
        self.passphrase = 'Custom passphrase goes here'
        # Every `sequence` item corresponds to some key in pool dict
        # That means also to a filename in `wordlists/`
        self.set_sequence('')
        self.regen_whole()

    # Used in main.py to CB copy, might require attention later
    def get(self):
        return ''.join([self.header, self.divider.join(self.words), self.tail])

    def __str__(self):
        return self.get()


def print_help(password):
    print('To regenerate a word, enter its number')
    print('r: Regenerate the whole password')
    print('s: Change the words sequence')
    print(f"current sequence: {', '.join(password.sequence)}")
    print('p: Use a passphrase, ps: Set a passphrase')
    print(f"current passphrase: {password.passphrase}")
    print('Change the case:')
    # print('l: lowercase      (example)')
    # print('c: capitalized    (Example)')
    # print('u: uppercase/caps (EXAMPLE)')
    print(f"current case: {password.case}")
    print('sc: Change the special characters pool')
    print(f"current pool: {password.special_chars}")
    print('h: Change the header sequence, hr: Randomize from pool')
    print(f"current header:   {password.header if password.header_flag == 'custom' else 'random'}")
    print('d: Change the divider sequence, dr: Randomize from pool, dm: Match the header sequence')
    print(f"current divider: {password.divider if password.divider_flag == 'custom' else password.divider_flag}")
    print('t: Change the tail sequence, tr: Randomize from pool, tm: Match the header sequence')
    print(f"current tail:     {password.tail if password.tail_flag == 'custom' else password.tail_flag}")
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
            password.use_passphrase(password.passphrase)
        
        elif choice == 'ps':
            password.passphrase = input('New passphrase: ')
            password.use_passphrase(password.passphrase)
        
        elif choice == 'l':
            password.set_case('lower')
        
        elif choice == 'c':
            password.set_case('capital')
        
        elif choice == 'u':
            password.set_case('upper')
        
        elif choice == 'h':
            password.header_flag = 'custom'
            password.header = input('New header sequence: ')
        
        elif choice == 'hr':
            password.header_flag = 'random'
            password.header = secrets.choice(password.special_chars)
            if password.divider_flag == 'match header':
                password.divider = password.header
            if password.tail_flag == 'match header':
                password.tail = password.header
        
        elif choice == 'd':
            password.divider_flag = 'custom'
            password.divider = input('New division sequence: ')
        
        elif choice == 'dr':
            password.divider_flag = 'random'
            password.divider = secrets.choice(password.special_chars)
        
        elif choice == 'dm':
            password.divider_flag = 'match header'
            password.divider = password.header
        
        elif choice == 't':
            password.tail_flag = 'custom'
            password.tail = input('New tail sequence: ')
        
        elif choice == 'tr':
            password.tail_flag = 'random'
            password.tail = secrets.choice(password.special_chars)
        
        elif choice == 'tm':
            password.tail_flag = 'match header'
            password.tail = password.header
        
        elif choice == 'sc':
            password.special_chars = input('New special characters pool: ')
        
        else:
            try:
                # If it's not one of mgmt chars,
                # then check if it's number of word to regen
                password.regen_one(int(choice) - 1)
                print(password)
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
