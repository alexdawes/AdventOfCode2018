from collections import defaultdict

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  grid = [[c for c in line] for line in lines]
  return Grid(grid)

def getGrid(grid):
  res = []
  for y in range(len(grid)):
    row = []
    for x in range(len(grid[y])):
      v = grid[y][x]
      if v == '>' or v == '<':
        row.append('-')
      elif x == '^' or v == 'v':
        row.append('|')
      else:
        row.append(v)
    res.append(row)
  return res

cartDirections = [
  '<',
  '|',
  '>'
]

class Cart(object):
  def __init__(self, x, y, d):
    self.x = x
    self.y = y
    self.d = d
    self.i = 0

  def move(self, grid):
    if self.d == '^':
      self.y -= 1
    elif self.d == 'v':
      self.y += 1
    elif self.d == '<':
      self.x -= 1
    elif self.d == '>':
      self.x += 1

    newPos = grid[self.y][self.x]

    if newPos == '/':
      if self.d == '<' or self.d == '>':
        self.turnLeft()
      elif self.d == '^' or self.d == 'v':
        self.turnRight()
    elif newPos == '\\':
      if self.d == '<' or self.d == '>':
        self.turnRight()
      elif self.d == '^' or self.d == 'v':
        self.turnLeft()
    elif newPos == '+':
      turn = cartDirections[self.i]
      self.i = (self.i + 1) % len(cartDirections)
      if turn == '<':
        self.turnLeft()
      elif turn == '>':
        self.turnRight()


  def turnLeft(self):
    transitions = {
      '^': '<',
      '<': 'v',
      'v': '>',
      '>': '^'
    }
    self.d = transitions[self.d]
    
  def turnRight(self):
    transitions = {
      '^': '>',
      '>': 'v',
      'v': '<',
      '<': '^'
    }
    self.d = transitions[self.d]

def getCarts(grid):
  carts = []
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      if grid[y][x] in ['v','^','<','>']:
        carts.append(Cart(x, y, grid[y][x]))
  return carts
  

class Grid(object):
  def __init__(self, grid):
    self.grid = getGrid(grid)
    self.carts = sorted(getCarts(grid), key = lambda c: (c.y,c.x))

  def runToCrash(self):
    while True:
      crash, unused = self.iterate()
      if crash:
        return crash

  def runWithCartRemoval(self):
    while True:
      i = 0
      while True:
        crash, i = self.iterate(i)
        if not crash:
          break
        
        newCarts = []
        for j in range(len(self.carts)):
          cart = self.carts[j]
          if (cart.x, cart.y) == crash:
            if j < i:
              i =- 1
          else:
            newCarts.append(cart)
        self.carts = newCarts
        i += 1
      
      if len(self.carts) == 1:
        return (self.carts[0].x, self.carts[0].y)
      

  def iterate(self, start = 0):
    for i in range(start, len(self.carts)):
      cart = self.carts[i]
      cart.move(self.grid)
      crash = self.crash()
      if crash:
        return crash, i
    self.carts.sort(key=lambda c: (c.y, c.x))
    return (None, None)

  def crash(self):
    counts = defaultdict(int)
    for cart in self.carts:
      counts[(cart.x, cart.y)] += 1
    crashes = [k for k in counts.keys() if counts[k] > 1]
    return crashes[0] if len(crashes) > 0 else None

def run1():
  grid = parseInput()
  crash = grid.runToCrash()
  return '{},{}'.format(*crash)

def run2():
  grid = parseInput()
  lastCart = grid.runWithCartRemoval()
  return '{},{}'.format(*lastCart)

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))