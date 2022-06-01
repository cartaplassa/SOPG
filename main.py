import random


leetrules = {
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


def leetify(word: str) -> str():
    leetified = word.replace('-','').lower().capitalize()
    for rule in leetrules:
        leetified = leetified.replace(rule, leetrules[rule])
    return leetified


def passgen(source: list[str]) -> str:
    return leetify(random.choice(source))


# Default generator formula: ADJ + NOU + VER + ADV
# Initialization: 
adjectives, adverbs, nouns, verbs = [], [], [], []
with open("./adj.txt") as f:
    for line in f:
        adjectives.append(line.strip())
f.close()
with open("./adv.txt") as f:
    for line in f:
        adverbs.append(line.strip())
f.close()
with open("./nou.txt") as f:
    for line in f:
        nouns.append(line.strip())
f.close()
with open("./ver.txt") as f:
    for line in f:
        verbs.append(line.strip())
f.close()


# Help:
def printhelp():
    print('1: Regenerate first word')
    print('2: Regenerate second word')
    print('3: Regenerate third word')
    print('4: Regenerate fourth word')
    print('5: Regenerate whole password')
    print('6: Change the divider sequence')
    print(f'current divider: "{divider}"')
    # print('7: Copy to clipboard')
    print('0: Exit the program')


# Execution:
choice = 5
pword = []
divider = '-'
printhelp()
while choice != 0:
    if choice == 5:
        pword = []
        pword.append(passgen(adjectives))
        pword.append(passgen(nouns))
        pword.append(passgen(verbs))
        pword.append(passgen(adverbs))
        print('New password generated:   ', divider.join(pword))
    elif choice == 1:
        pword[0] = passgen(adjectives)
        print('New adjective generated:  ', divider.join(pword))
    elif choice == 2:
        pword[1] = passgen(nouns)
        print('New noun generated:       ', divider.join(pword))
    elif choice == 3:
        pword[2] = passgen(verbs)
        print('New verb generated:       ', divider.join(pword))
    elif choice == 4:
        pword[3] = passgen(adverbs)
        print('New adverb generated:     ', divider.join(pword))
    elif choice == 6:
        divider = input('New division sequence:')
        print(f'Divider set to "{divider}",', divider.join(pword))
    # elif choice == 7: # Might add copying later
    else:
        printhelp()
    print('---')
    try:
        choice = int(input('User input: '))
    except:
        print('Error: number expected, letter found')
        printhelp()
