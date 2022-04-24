import random

# List of rules, key is replaced with value
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

# v3 Generator Formula: ADJ + NOU + VER + ADV
## Deprecated, might be returned later
## Custom separators w/ random chance:
# separators = ["_", "/", "-"]
# result = random.choice(separators).join(random.sample(dictlist, 3))

# INIT: 
adjectives, adverbs, nouns, verbs = [], [], [], []
with open("./adj.txt") as f:
  for line in f:
    adjectives.append(line.strip())
with open("./adv.txt") as f:
  for line in f:
    adverbs.append(line.strip())
with open("./nou.txt") as f:
  for line in f:
    nouns.append(line.strip())
with open("./ver.txt") as f:
  for line in f:
    verbs.append(line.strip())

# HELP:
def printhelp():
  print('Regenerate first word: 1')
  print('Regenerate second word: 2')
  print('Regenerate third word: 3')
  print('Regenerate fourth word: 4')
  print('Regenerate whole password: 5')
  print('Exit the program: 0')

# EXEC:
choice = 5
pword = []
printhelp()
while choice != 0:
  if choice == 5:
    pword = []
    pword.append(passgen(adjectives))
    pword.append(passgen(nouns))
    pword.append(passgen(verbs))
    pword.append(passgen(adverbs))
    print('New password generated: ', '-'.join(pword))
  elif choice == 1:
    pword[0] = passgen(adjectives)
    print('New adjective generated:', '-'.join(pword))
  elif choice == 2:
    pword[1] = passgen(nouns)
    print('New noun generated:     ', '-'.join(pword))
  elif choice == 3:
    pword[2] = passgen(verbs)
    print('New verb generated:     ', '-'.join(pword))
  elif choice == 4:
    pword[3] = passgen(adverbs)
    print('New adverb generated:   ', '-'.join(pword))
  else:
    printhelp()
  print('---')
  try:
    choice = int(input('User input: '))
  except:
    print('Error: number expected, letter found')
    printhelp()
