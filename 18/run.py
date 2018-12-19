def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  return Map([[l for l in line.strip()] for line in lines])

class Map(object):
  def __init__(self, grid):
    self.grid = grid

  def __str__(self):
    return '\n'.join([''.join(row) for row in self.grid])

  def hash(self):
    return hash(tuple([self.grid[i][j] for i in range(len(self.grid)) for j in range(len(self.grid[i]))]))

  def countOpen(self):
    return len([self.grid[i][j] for i in range(len(self.grid)) for j in range(len(self.grid[i])) if self.grid[i][j] == '.'])

  def countTrees(self):
    return len([self.grid[i][j] for i in range(len(self.grid)) for j in range(len(self.grid[i])) if self.grid[i][j] == '|'])

  def countLumberyards(self):
    return len([self.grid[i][j] for i in range(len(self.grid)) for j in range(len(self.grid[i])) if self.grid[i][j] == '#'])

  def resourceValue(self):
    return self.countTrees() * self.countLumberyards()

  def iterate(self):
    self.grid = [
      [
        self.nextCell(i, j)
        for j in range(len(self.grid[i]))
      ]
      for i in range(len(self.grid))
    ]
        
  def nextCell(self, i, j):
    cell = self.grid[i][j]
    adjacent = [
      self.grid[x][y]
      for x in range(max(0,i-1), min(len(self.grid), i+2))
      for y in range(max(0,j-1), min(len(self.grid[i]),j+2))
      if x != i or y != j
    ]
    
    if cell == '.':
      numTrees = len([c for c in adjacent if c == '|'])
      return '|' if numTrees >= 3 else '.'
    if cell == '|':
      numLum = len([c for c in adjacent if c == '#'])
      return '#' if numLum >= 3 else '|'
    if cell == '#':
      numTrees = len([c for c in adjacent if c == '|'])
      numLum = len([c for c in adjacent if c == '#'])
      return '#' if numTrees >= 1 and numLum >= 1 else '.'
    return cell

def run1():
  mp = parseInput()
  for i in range(10):
    mp.iterate()
    # print('After {} minutes:'.format(i+1))
    # print(mp)
    # print()

  return mp.resourceValue()

def run2():
  mp = parseInput()
  hashes = { mp.hash(): 0 }
  for i in range(1000000000):
    mp.iterate()
    hsh = mp.hash()
    if hsh in hashes:
      idx = hashes[hsh]
      cycleLength = i - idx
      remaining = 1000000000 - i - 1
      actualRemaining = remaining % cycleLength
      for i in range(actualRemaining):
        mp.iterate()
      break
    hashes[hsh] = i
    
  return mp.resourceValue()

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')