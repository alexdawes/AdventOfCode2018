def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  values = [int(l.strip()) for l in lines]
  return values

def run1():
  values = parseInput()
  return sum(values)
  print('Part 1: {}'.format(result))

def run2():
  values = parseInput()

  counter = 0
  summations = []
  for i in range(len(values)):
    summations.append(counter)
    counter += values[i]
    if counter in summations:
      return counter

  total = run1()

  newSummations = [s for s in summations]
  while(True):
    newSummations = [summand + total for summand in newSummations]
    intersection = [s for s in newSummations if s in summations]
    if len(intersection) > 0:
      return intersection[0]

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))
