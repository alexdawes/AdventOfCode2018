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
      if current == nxt.swapcase() and idx > 0:
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
  return s.replace(letter, '').replace(letter.swapcase(), '')

def run1():
  s = parseInput()
  return getReducedLength(s)

def run2():
  s = parseInput()
  return min([getReducedLength(removeLetter(s, l)) for l in alphabet])

def quickReduce(s):
  stack = []
  for l in s:
    if len(stack) == 0:
      stack.append(l)
    else:
      if l == stack[-1].swapcase():
        stack.pop()
      else:
        stack.append(l)
  return ''.join(stack)

def run1_1():
  s = parseInput()
  r = quickReduce(s)
  return len(r)

def run2_1():
  s = parseInput()
  return min([len(quickReduce(s.replace(l, '').replace(l.swapcase(), ''))) for l in alphabet])

import time

if __name__ == '__main__':
  start1 = time.time()
  print('Part 1: {}'.format(run1()))
  end1 = time.time()
  start2 = time.time()
  print('Part 1: {}'.format(run1_1()))
  end2 = time.time()
  start3 = time.time()
  print('Part 2: {}'.format(run2()))
  end3 = time.time()
  start4 = time.time()
  print('Part 2: {}'.format(run2_1()))
  end4 = time.time()
  print('Times: {}ms, {}ms, {}ms, {}ms'.format(int((end1-start1)*1000), int((end2-start2)*1000), int((end3-start3)*1000), int((end4-start4)*1000)))