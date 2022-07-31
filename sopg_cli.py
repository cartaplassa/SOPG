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

    # IMPORTANT: operates w/ indices, not w/ numbers
    def regen_one(self, which: int):
        self.words[which] = self.generate(self.sequence[which])

    def regen_whole(self):
        self.words = []
        for each in self.sequence:
            self.words.append(self.generate(each))

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
        self.divider = '-'
        self.case = 1
        # Every 'sequence' item corresponds to some key in pool dict
        self.set_sequence('')
        self.regen_whole()

    def __str__(self):
        return self.divider.join(self.words)

    def get(self):
        return self.divider.join(self.words)


def print_help(password):
    print('To regenerate a word, enter its number')
    print('r: Regenerate the whole password')
    print('d: Change the divider sequence')
    print(f'current divider: "{password.divider}"')
    print('s: Change the words sequence')
    print(f"current sequence: \"{', '.join(password.sequence)}\"")
    print('Change the case:')
    print('l: lowercase      (example)')
    print('c: capitalized    (Example)')
    print('u: uppercase/caps (EXAMPLE)')
    print(f"current case: {('lowercase', 'capitalize', 'uppercase')[password.case]}")
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
            print(password)
        elif choice == 'd':
            divider = input('New division sequence: ')
            password.divider = divider
            print(f'Divider set to "{divider}",')
            print(password)
        elif choice == 's':
            sequence = input('New words sequence: ')
            password.set_sequence(sequence)
            print(f"New sequence is \"{', '.join(password.sequence)}\"")
            password.regen_whole()
            print(password)
        elif choice == 'l':
            password.set_case(0)
            print("Case set to lowercase")
            print(password)
        elif choice == 'c':
            password.set_case(1)
            print("Case set to capitalized")
            print(password)
        elif choice == 'u':
            password.set_case(2)
            print("Case set to uppercase")
            print(password)
        else:
            try:
                # If it's not one of mgmt chars,
                # then check if it's number of word to regen
                password.regen_one(int(choice) - 1)
                print(password)
            except:
                print(f'Input "{choice}" unrecognized')
                print_help(password)
        print('---')
        choice = input('User input: ')


if __name__ == '__main__':
    main()
