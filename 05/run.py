alphabet = 'abcdefghijklmnopqrstuvwxyz'

def parseInput():
  with open('input', 'r') as f:
    return f.read()

def getLinks(s):
  return [i+1 if i+1 < len(s) else None for i in range(len(s))]

def reduce(links, s):
  idx = len(s) - 2
  while idx >= 0:
    current, nextIdx = s[idx], links[idx]
    if nextIdx is not None:
      nxt = s[nextIdx]
      if (current == current.lower() and nxt == current.upper()) \
       or (current == current.upper() and nxt == current.lower()) \
       and idx > 0:
        links[idx - 1] = links[nextIdx]
    idx -= 1

def getLength(links):
  idx, count = 0, 0
  while idx is not None:
    count, idx = count + 1, links[idx]
  return count

def getReducedLength(s):
  links = getLinks(s)
  reduce(links, s)
  return getLength(links)

def removeLetter(s, letter):
  return s.replace(letter.upper(), '').replace(letter.lower(), '')

def run1():
  s = parseInput()
  return getReducedLength(s)

def run2():
  s = parseInput()
  return min([getReducedLength(removeLetter(s, l)) for l in alphabet])

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))