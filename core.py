import random
import os
import logging


class Password():
    def leetify(self, word: str) -> str():
        leetified = word.replace('-','')
        for before, after in self.leetrules.items():
            leetified = leetified.replace(before, after)
        return leetified

    def new_sequence(self, source: str) -> list:
        return [each for each in source.replace(' ', '').lower().split(',') \
            if each in list(self.pool.keys())]

    def set_sequence(self, source: str):
        self.sequence = self.new_sequence(source) if self.new_sequence(source) \
            else self.new_sequence('adj,nou,ver,adv')

    def generate(self, source: list[str]) -> str:
        if self.case == 0:
            return self.leetify(random.choice(self.pool[source]).lower())
        elif self.case == 1:
            return self.leetify(random.choice(self.pool[source]).lower().capitalize())
        elif self.case == 2:
            return self.leetify(random.choice(self.pool[source]).upper())

    # Changes case of existing password. Will override leetrules.
    # May not be useful, but it's better to have it as an option.
    def set_case(self, new_case):
        self.case = new_case
        if new_case == 0:
            self.words = [word.lower() for word in self.words]
        elif new_case == 1:
            self.words = [word.lower().capitalize() for word in self.words]
        elif new_case == 2:
            self.words = [word.upper() for word in self.words]
        # self.words = [
        #     [word.lower() for word in self.words],
        #     [word.lower().capitalize() for word in self.words],
        #     [word.upper() for word in self.words]
        # ][new_case]
        # Same but blursed

    def update_dividers(self):
        if self.header_flag == 1:
            self.header = random.choice(self.special_chars)
        if self.divider_flag == 1:
            self.divider = random.choice(self.special_chars)
        elif self.divider_flag == 2:
            self.divider = self.header
        if self.tail_flag == 1:
            self.tail = random.choice(self.special_chars)
        elif self.tail_flag == 2:
            self.tail = self.header

    # Operates w/ indices, not w/ numbers
    def regen_one(self, which: int):
        self.words[which] = self.generate(self.sequence[which])

    def regen_whole(self):
        self.words = []
        for each in self.sequence:
            self.words.append(self.generate(each))
        # Dividers regen only when the whole pword regens, UX-motivated choice
        self.update_dividers()

    # Default sequence is set in set_sequence()
    def __init__(self):
        # Determiners (the, this, my, etc.) can be added as another key
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
        self.header_flag = 0
        self.header = '~'
        self.divider_flag = 0
        self.divider = '-'
        self.tail_flag = 0
        self.tail = '#'
        # self.case variable is int so it can be used as a tuple index
        self.case = 1
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
    print(f"current case: {('lowercase', 'capitalize', 'uppercase')[password.case]}")
    print('p: Change the special characters pool')
    print(f"current pool: {password.special_chars}")
    print('h: Change the header sequence, hr: Randomize from pool')
    print(f"current header:   {password.header if not password.header_flag else 'random'}")
    print('d: Change the divider sequence, dr: Randomize from pool, dm: Match the header sequence')
    print(f"current divider: {password.divider if not password.divider_flag else 'random' if password.divider_flag == 1 else 'matches header'}")
    print('t: Change the tail sequence, tr: Randomize from pool, tm: Match the header sequence')
    print(f"current tail:     {password.tail if not password.tail_flag else 'random' if password.tail_flag == 1 else 'matches header'}")
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
            password.set_case(0)
        elif choice == 'c':
            password.set_case(1)
        elif choice == 'u':
            password.set_case(2)
        elif choice == 'h':
            password.header_flag = 0
            password.header = input('New header sequence: ')
        elif choice == 'hr':
            password.header_flag = 1
            password.header = random.choice(password.special_chars)
            if password.divider_flag == 2:
                password.divider = password.header
            if password.tail_flag == 2:
                password.tail = password.header
        elif choice == 'd':
            password.divider_flag = 0
            password.divider = input('New division sequence: ')
        elif choice == 'dr':
            password.divider_flag = 1
            password.divider = random.choice(password.special_chars)
        elif choice == 'dm':
            password.divider_flag = 2
            password.divider = password.header
        elif choice == 't':
            password.tail_flag = 0
            password.tail = input('New tail sequence: ')
        elif choice == 'tr':
            password.tail_flag = 1
            password.tail = random.choice(password.special_chars)
        elif choice == 'tm':
            password.tail_flag = 2
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
