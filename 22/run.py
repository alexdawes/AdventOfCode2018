import re

line1Regex = r'depth: (\d+)'
line2Regex = r'target: (\d+),(\d+)'

def parseInput():
  with open('input', 'r') as f:
    line1, line2 = [l.strip() for l in f.readlines()]
  depth = int(re.match(line1Regex, line1).group(1))
  targetMatch = re.match(line2Regex, line2)
  target = (int(targetMatch.group(1)), int(targetMatch.group(2)))
  return Cave(depth, target)

class Cave(object):
  def __init__(self, depth, target):
    self.depth = depth
    self.target = target
    self.erosionLevels = { }
    self.geologicalIndexes = { (0,0): 0, target: 0 }

  def __str__(self):
    return self.getStr(self.target)

  def getStr(self, coord):
    rows = []
    for y in range(coord[1]):
      row = []
      for x in range(coord[0]):
        rl = self.getRiskLevel((x, y))
        if rl == 0:
          row.append('.')
        elif rl == 1:
          row.append('=')
        elif rl == 2:
          row.append('|')
      rows.append(row)

    return '\n'.join([''.join([r for r in row]) for row in rows])

  def getGeologicalIndex(self, coord):
    if coord not in self.geologicalIndexes:
      self.geologicalIndexes[coord] = self.calcGeologicalIndex(coord)
    return self.geologicalIndexes[coord]

  def calcGeologicalIndex(self, coord):
    (x,y) = coord
    if (x,y) == (0,0) or (x,y) == self.target:
      return 0
    if y == 0:
      return x * 16807
    if x == 0:
      return y * 48271
    return self.getErosionLevel((x-1,y)) * self.getErosionLevel((x,y-1))
    
  def getErosionLevel(self, coord):
    if coord not in self.erosionLevels:
      self.erosionLevels[coord] = self.calcErosionLevel(coord)
    return self.erosionLevels[coord]

  def calcErosionLevel(self, coord):
    return (self.getGeologicalIndex(coord) + self.depth) % 20183

  def getRiskLevel(self, coord):
    return self.getErosionLevel(coord) % 3

EQ_TORCH = 0
EQ_CLIMBING = 1
EQ_NEITHER = 2

RL_ROCKY = 0
RL_WET = 1
RL_NARROW = 2

class Topology(object):
  def __init__(self, cave):
    self.cave = cave

  def hDist(self, p1, p2):
    (x1,y1,e1) = p1
    (x2,y2,e2) = p2
    xDist = abs(x1-x2)
    yDist = abs(y1-y2)
    eDist = 7 if e1 != e2 else 0
    return xDist + yDist + eDist

  def aStar(self, start, end):
    h = self.hDist(start, end)
    if h == 0:
      return h, [start]
    if h == 1:
      return h, [start, end]
    if (start[0], start[1]) == (end[0], end[1]):
      return 7, [start, end]

    closedSet = set()
    openSet = set([start])
    gScore = { start: 0 }
    fScore = { start: h }
    cameFrom = {}
    while len(openSet) > 0:
      current = min(openSet, key=lambda p: fScore[p])
      if current == end:
        path = [current]
        while current in cameFrom:
            current = cameFrom[current]
            path.append(current)
        path.reverse()
        return fScore[end], path
      openSet.remove(current)
      closedSet.add(current)

      currentEquipment = current[2]
      neighbours = []
      rl = self.cave.getRiskLevel((current[0], current[1]))
      if rl == RL_ROCKY:
        if currentEquipment != EQ_TORCH:
          neighbours.append((current[0], current[1], EQ_TORCH))
        if currentEquipment != EQ_CLIMBING:
          neighbours.append((current[0], current[1], EQ_CLIMBING))
      if rl == RL_WET:
        if currentEquipment != EQ_NEITHER:
          neighbours.append((current[0], current[1], EQ_NEITHER))
        if currentEquipment != EQ_CLIMBING:
          neighbours.append((current[0], current[1], EQ_CLIMBING))
      if rl == RL_NARROW:
        if currentEquipment != EQ_TORCH:
          neighbours.append((current[0], current[1], EQ_TORCH))
        if currentEquipment != EQ_NEITHER:
          neighbours.append((current[0], current[1], EQ_NEITHER))

      x, y, = current[0], current[1]
      neighbourNodes = [p for p in [(x,y+1),(x,y-1),(x-1,y),(x+1,y)] if p[0] >= 0 and p[1] >= 0]
      for n in neighbourNodes:
        rl = self.cave.getRiskLevel(n)
        if currentEquipment == EQ_TORCH:
          if rl == RL_ROCKY or rl == RL_NARROW:
            neighbours.append((n[0], n[1], currentEquipment))
        if currentEquipment == EQ_CLIMBING:
          if rl == RL_ROCKY or rl == RL_WET:
            neighbours.append((n[0], n[1], currentEquipment))
        if currentEquipment == EQ_NEITHER:
          if rl == RL_WET or rl == RL_NARROW:
            neighbours.append((n[0], n[1], currentEquipment))

      for n in neighbours:
        if n in closedSet:
          continue
        gTentative = gScore[current] + self.hDist(current, n)
        if n not in openSet:
          openSet.add(n)
        elif n in gScore and gTentative >= gScore[n]:
          continue
        gScore[n] = gTentative
        fScore[n] = gScore[n] + self.hDist(n, end)
        cameFrom[n] = current
    return None, None

def run1():
  cave = parseInput()
  return sum([cave.getRiskLevel((x,y)) for x in range(cave.target[0] + 1) for y in range(cave.target[1] + 1)])

def run2():
  cave = parseInput()
  topology = Topology(cave)
  start = (0, 0, EQ_TORCH)
  end = (cave.target[0], cave.target[1], EQ_TORCH)
  dist, path = topology.aStar(start, end)
  return dist

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')