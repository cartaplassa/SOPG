import random


def leetify(word):
    return (word
    .replace('-','')
    .lower()
    .capitalize()
    .replace('O','0')
    .replace('o','0')
    .replace('I','1')
    .replace('i','1')
    .replace('B','8')
    .replace('b','8')
    .replace('S','$')
    .replace('s','$')
    .replace('L','!')
    .replace('l','!'))

def passgen(source):
    return leetify(random.choice(source))

# v3 Generator Formula: ADJ + NOU + VER + ADV
# Custom separators w/ random chance
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

# EXEC:
choice = 5
pword = []
print('1-4 - NEW WORD, 5 - NEW PASSWORD, 0 - EXIT')
while choice != 0:
  if choice == 5:
    pword = []
    pword.append(passgen(adjectives))
    pword.append(passgen(nouns))
    pword.append(passgen(verbs))
    pword.append(passgen(adverbs))
    print('GENERATED NEW PASSWORD:')
    print('-'.join(pword))
  elif choice == 1:
    pword[0] = passgen(adjectives)
    print('GENERATED NEW ADJECTIVE:')
    print('-'.join(pword))
  elif choice == 2:
    pword[1] = passgen(nouns)
    print('GENERATED NEW NOUN:')
    print('-'.join(pword))
  elif choice == 3:
    pword[2] = passgen(verbs)
    print('GENERATED NEW VERB:')
    print('-'.join(pword))
  elif choice == 4:
    pword[3] = passgen(adverbs)
    print('GENERATED NEW ADVERB:')
    print('-'.join(pword))
  else:
    print('1-4 - NEW WORD, 5 - NEW PASSWORD, 0 - EXIT')
  choice = int(input())
