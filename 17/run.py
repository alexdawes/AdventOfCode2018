import re

regex = r'(x|y)=(\d+), (x|y)=(\d+)..(\d+)'

def parseLine(line):
  match = re.match(regex, line)
  if match.group(1) == 'x' and match.group(3) == 'y':
    x = int(match.group(2))
    y1, y2 = int(match.group(4)), int(match.group(5))
    return [(x,y) for y in range(y1,y2+1)]
  elif match.group(1) == 'y' and match.group(3) == 'x':
    x1, x2 = int(match.group(4)), int(match.group(5))
    y = int(match.group(2))
    return [(x,y) for x in range(x1,x2+1)]
  else:
    raise 'Failed.'

def parseInput():
  with open('input') as f:
    lines = f.readlines()
  return System((500,0), set([c for line in lines for c in parseLine(line)]))

class System(object):
  def __init__(self, source, clays):
    self.source = source
    self.clays = clays
    self.runningWaters = set()
    self.stillWaters = set()
    self.nodes = set([source])
    self.parentNodes = { source: None }

  def __str__(self):
    return self.getStr()

  def getStr(self, rng=None):
    minX = min([c[0] for c in self.clays]) if rng is None else min([c[0] for c in self.clays if c[1] >= rng[0] and c[1] < rng[1]])
    maxX = max([c[0] for c in self.clays]) if rng is None else max([c[0] for c in self.clays if c[1] >= rng[0] and c[1] < rng[1]])
    maxY = max([c[1] for c in self.clays])
    grid = []
    for j in range(maxY+1+2) if rng is None else range(*rng):
      row = []
      for i in range(minX-2, maxX+3):
        if (i,j) in self.nodes:
          row.append('o')
        elif (i,j) == (500,0):
          row.append('+')
        elif (i,j) in self.clays:
          row.append('#')
        elif (i,j) in self.runningWaters:
          row.append('|')
        elif (i,j) in self.stillWaters:
          row.append('~')
        else:
          row.append('.')
      grid.append(row)
    return '\n'.join([''.join(row) for row in grid])

  def getAbove(self, pos):
    return (pos[0], pos[1]-1)

  def getBelow(self, pos):
    return (pos[0], pos[1]+1)

  def getRight(self, pos):
    return (pos[0]+1, pos[1])

  def getLeft(self, pos):
    return (pos[0]-1, pos[1])

  def isSand(self, pos):
    return pos not in self.clays \
      and pos not in self.runningWaters \
      and pos not in self.stillWaters

  def isClay(self, pos):
    return pos in self.clays

  def isStillWater(self, pos):
    return pos in self.stillWaters

  def isRunningWater(self, pos):
    return pos in self.runningWaters

  def iterate(self):
    for node in [n for n in self.nodes]:
      below = (node[0], node[1]+1)
      if self.isRunningWater(node) or node == self.source:
        if self.isSand(below):
          self.runningWaters.add(below)
          self.nodes.remove(node)
          self.nodes.add(below)
          self.parentNodes[below] = node
        elif self.isClay(below) or self.isStillWater(below):
          if self.isRunningWater(node):
            self.runningWaters.remove(node)
          left = self.getLeft(node)
          right = self.getRight(node)
          while True:
            if self.isClay(left):
              leftContained = True
              break
            belowLeft = self.getBelow(left)
            if self.isClay(belowLeft) or self.isStillWater(belowLeft):
              left = self.getLeft(left)
            else:
              leftContained = False
              break
          while True:
            if self.isClay(right):
              rightContained = True
              break
            belowRight = self.getBelow(right)
            if self.isClay(belowRight) or self.isStillWater(belowRight):
              right = self.getRight(right)
            else:
              rightContained = False
              break
          if leftContained and rightContained:
            for i in range(left[0]+1, right[0]):
              if self.isRunningWater((i, node[1])):
                self.runningWaters.remove((i, node[1]))
              self.stillWaters.add((i,node[1]))
            self.nodes.remove(node)
            self.nodes.add(self.parentNodes[node])
          else:
            for i in range(left[0]+1, right[0]):
              self.runningWaters.add((i, node[1]))
            self.nodes.remove(node)
            if not leftContained:
              self.runningWaters.add(left)
              self.nodes.add(left)
              self.parentNodes[left] = node
            if not rightContained:
              self.runningWaters.add(right)
              self.nodes.add(right)
              self.parentNodes[right] = node
    for node in [n for n in self.nodes]:
      if self.isStillWater(node):
        self.nodes.remove(node)
        parentNode = self.parentNodes[node]
        while self.isStillWater(parentNode):
          parentNode = self.parentNodes[parentNode]
        self.nodes.add(parentNode)

        

def runSystem(system):
  minY = min([p[1] for p in system.clays])
  maxY = max([p[1] for p in system.clays])
  numStillWater = len([s for s in system.stillWaters if s[1] <= maxY])
  numRunningWater = len([s for s in system.runningWaters if s[1] <= maxY])
  while True:
    system.iterate()
    newNumStillWater = len([s for s in system.stillWaters if s[1] <= maxY])
    newNumRunningWater = len([s for s in system.runningWaters if s[1] <= maxY])
    if newNumStillWater == numStillWater and newNumRunningWater == numRunningWater:
      break
    else:
      numStillWater = newNumStillWater
      numRunningWater = newNumRunningWater
  numStillWater = len([s for s in system.stillWaters if minY <= s[1] and s[1] <= maxY])
  numRunningWater = len([s for s in system.runningWaters if minY <= s[1] and s[1] <= maxY])
  return (numStillWater, numRunningWater)

def run1():
  system = parseInput()
  (sw,rw) = runSystem(system)
  return sw + rw
    
def run2():
  system = parseInput()
  (sw,rw) = runSystem(system)
  return sw
    
if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
  