alphabet = 'abcdefghijklmnopqrstuvwxyz'

def parseInput():
  with open('input', 'r') as f:
    return f.read()

def reduce(s):
  stack = []
  for l in s:
    if len(stack) > 0 and l == stack[-1].swapcase():
      stack.pop()
    else:
      stack.append(l)
  return ''.join(stack)

def run1():
  s = parseInput()
  return len(reduce(s))

def run2():
  s = parseInput()
  return min([len(reduce(s.replace(l, '').replace(l.swapcase(), ''))) for l in alphabet])

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))