import re

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def parseInput():
  with open('input', 'r') as f:
    return f.read()

def getRegex():
  pairs = []
  for letter in alphabet:
    pairs.append('{}{}'.format(letter.upper(), letter.lower()))
    pairs.append('{}{}'.format(letter.lower(), letter.upper()))
  return r'({})'.format('|'.join(pairs))

def reduce(s):
  regex = getRegex()
  lastLength = None
  currentLength = len(s)
  while(lastLength != currentLength):
    s = re.sub(regex, '', s)
    lastLength, currentLength = currentLength, len(s)
  return s

def run1():
  s = parseInput()
  return len(reduce(s))

def removeAndReduce(s, letter):
  regex = '({}|{})'.format(letter.upper(), letter.lower())
  s = re.sub(regex, '', s)
  return reduce(s)

def run2():
  s = parseInput()
  return min([len(removeAndReduce(s, letter)) for letter in alphabet])

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))