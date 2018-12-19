from collections import defaultdict
import re

regex1 = 'initial state: ([#\.]+)'
regex2 = '([#\.]{5}) => ([#\.])'

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()

  firstLine, otherLines = lines[0], lines[2:]

  initialState = defaultdict(bool)
  initialStateStr = re.match(regex1, firstLine).group(1)
  for i in range(len(initialStateStr)):
    initialState[i] = (initialStateStr[i] == '#')

  rules = { tuple([(l == '#') for l in re.match(regex2, line).group(1)]): re.match(regex2, line).group(2) == '#' for line in otherLines }

  return initialState, rules

def getActiveKeys(state):
  return [k for k in state.keys() if state[k]]

def iterate(state, rules):
  newState = defaultdict(bool)
  keys = getActiveKeys(state)
  idxs = [i for k in keys for i in range(k-2, k+2+1)]
  for idx in idxs:
    newState[idx] = rules[tuple([state[j] for j in range(idx-2, idx+2+1)])]
  return newState

def sumState(state):
  keys = getActiveKeys(state)
  return sum(keys)

def run1():
  state, rules = parseInput()
  for i in range(20):
    state = iterate(state, rules)
  return sumState(state)

def getStateKeyAndOffset(state):
  keys = sorted(getActiveKeys(state))
  minKey = min(keys)
  return tuple([k - minKey for k in keys]), minKey

def offsetState(state, offset):
  newState = defaultdict(bool)
  for k in state.keys():
    newState[k + offset] = state[k]
  return newState

def run2():
  cache = {}
  state, rules = parseInput()
  numIterations = 50000000000
  for it in range(numIterations):
    key, offset = getStateKeyAndOffset(state)
    if key in cache:
      prevIt, prevOffset = cache[key]
      cycleLength = it - prevIt
      cycleOffset = offset - prevOffset

      numCycles = int((numIterations - prevIt) / cycleLength)
      itsRemaining = (numIterations - prevIt) % cycleLength
      state = offsetState(state, numCycles - 1)
      for jit in range(itsRemaining):
        state = iterate(state, rules)
      return sumState(state)

    cache[key] = (it, offset)
    state = iterate(state, rules)
  return sumState(state)


if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')