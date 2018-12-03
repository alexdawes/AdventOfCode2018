def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  values = [l.strip() for l in lines]
  return values

def run1():
  alphabet = 'abcdefghijklmnopqrstuvwxyz'
  twos = 0
  threes = 0
  ids = parseInput()

  for id in ids:
    counter = { l: 0 for l in alphabet }
    for l in id:
      counter[l] += 1
    counts = counter.values()
    if 2 in counts:
      twos += 1
    if 3 in counts:
      threes += 1
  return twos * threes

def similar(id1, id2):
  count = 0
  if len(id1) != len(id2):
    return False
  for idx in range(len(id1)):
    if id1[idx] != id2[idx]:
      count += 1
    if count > 1:
      return False
  return True

def common(id1, id2):
  l = min([len(id1), len(id2)])
  result = ''
  for i in range(l):
    if id1[i] == id2[i]:
      result += id1[i]
  return result

def run2():
  ids = parseInput()
  for i in range(len(ids)):
    for j in range(i - 1):
      if similar(ids[i], ids[j]):
        return common(ids[i], ids[j])


if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))