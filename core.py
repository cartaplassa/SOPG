import secrets
import os
import logging


class Password():
    def leetify(self, word: str) -> str():
        leetified = word.replace('-','')
        for before, after in self.leetrules.items():
            leetified = leetified.replace(before, after)
        return leetified

    def new_sequence(self, source: str) -> list:
        return [each for each in source.lower().split() \
            if each in list(self.pool.keys())]

    def set_sequence(self, source: str):
        self.sequence = self.new_sequence(source) if self.new_sequence(source) \
            else self.new_sequence('adj nou ver adv')

    def generate(self, source: list[str]) -> str:
        if self.case == 'lower':
            return self.leetify(secrets.choice(self.pool[source]).lower())
        elif self.case == 'capital':
            return self.leetify(secrets.choice(self.pool[source]).lower().capitalize())
        elif self.case == 'upper':
            return self.leetify(secrets.choice(self.pool[source]).upper())

    # Changes case of existing password. Will override leetrules.
    # May not be useful, but it's better to have it as an option.
    def set_case(self, new_case):
        self.case = new_case
        if new_case == 'lower':
            self.words = [word.lower() for word in self.words]
        elif new_case == 'capital':
            self.words = [word.lower().capitalize() for word in self.words]
        elif new_case == 'upper':
            self.words = [word.upper() for word in self.words]

    def update_dividers(self):
        if self.header_flag == 'random':
            self.header = secrets.choice(self.special_chars)
        if self.divider_flag == 'random':
            self.divider = secrets.choice(self.special_chars)
        elif self.divider_flag == 'match header':
            self.divider = self.header
        if self.tail_flag == 'random':
            self.tail = secrets.choice(self.special_chars)
        elif self.tail_flag == 'match header':
            self.tail = self.header

    # Operates w/ indices, not w/ numbers
    def regen_one(self, which: int):
        self.words[which] = self.generate(self.sequence[which])

    def regen_whole(self):
        self.words = []
        for each in self.sequence:
            self.words.append(self.generate(each))
        # Dividers don't regen when a single is regened, UX-motivated choice
        self.update_dividers()

    # Default sequence is set in set_sequence()
    def __init__(self):
        self.pool = {}
        for each in os.listdir('wordlists'):
            with open(f'wordlists/{each}', 'r') as file:
                self.pool[str(os.path.splitext(each)[0])] = []
                for line in file:
                    self.pool[str(os.path.splitext(each)[0])].append(line.strip())

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
        # Every 'sequence' item corresponds to some key in pool dict
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
    print('Change the case:')
    print('l: lowercase      (example)')
    print('c: capitalized    (Example)')
    print('u: uppercase/caps (EXAMPLE)')
    print(f"current case: {password.case}")
    print('p: Change the special characters pool')
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
        
        elif choice == 'p':
            password.special_chars = input('New special characters pool: ')
        
        else:
            try:
                # If it's not one of mgmt chars,
                # then check if it's number of word to regen
                password.regen_one(int(choice) - 1)
                print(password)
            #TD: Specify error case
            except:
                print(f'Input "{choice}" unrecognized')
                print_help(password)
        
        print(password)
        choice = input('User input: ')


if __name__ == '__main__':
    main()
