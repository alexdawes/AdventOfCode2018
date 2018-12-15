from enum import Enum

class Team(Enum):
  ELF = 1
  GOBLIN = 2

class Unit(object):
  def __init__(self, x, y, hp, atk, team):
    self.x = x
    self.y = y
    self.pos = (self.x,self.y)
    self.hp = hp
    self.atk = atk
    self.team = team

  def move(self, x, y):
    self.x, self.y, self.pos = x, y, (x,y)

  def wound(self, dmg):
    self.hp -= dmg
    
  def attack(self, unit):
    unit.wound(self.atk)

  def isAlive(self):
    return self.hp > 0
  
  def isDead(self):
    return not self.isAlive()

  def neighbours(self):
    return [(self.x-1,self.y),(self.x+1,self.y),(self.x,self.y-1),(self.x,self.y+1)]

class Goblin(Unit):
  def __init__(self, x, y):
    super().__init__(x, y, 200, 3, Team.GOBLIN)
  def __str__(self):
    return 'G({})'.format(self.hp)

class Elf(Unit):
  def __init__(self, x, y, atk=200):
    super().__init__(x, y, 200, atk, Team.ELF)
  def __str__(self):
    return 'E({})'.format(self.hp)

class Wall(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.pos = (x,y)

class Map(object):
  def __init__(self, units, walls):
    self.units = units
    self.walls = walls
  def __str__(self):
    minX = min([u.x for u in self.units] + [w.x for w in self.walls])
    maxX = max([u.x for u in self.units] + [w.x for w in self.walls])
    minY = min([u.y for u in self.units] + [w.y for w in self.walls])
    maxY = max([u.y for u in self.units] + [w.y for w in self.walls])
    grid = [['.' for x in range(minX, maxX+1)] for y in range(minY, maxY+1)]
    for wall in self.walls:
      grid[wall.y][wall.x] = '#'
    for unit in self.units:
      letter = 'U'
      if unit.team == Team.ELF:
        letter = 'E'
      if unit.team == Team.GOBLIN:
        letter = 'G'
      grid[unit.y][unit.x] = letter
    return '\n'.join(
      [''.join([grid[y][x] for x in range(minX, maxX+1)]) + '   ' + ', '.join([str(u) for u in sorted(self.units, key=lambda v: v.x) if u.y == y]) for y in range(minY, maxY+1)])

  def isBlocked(self, p):
    blockingWalls = [w for w in self.walls if w.pos == p]
    blockingUnits = [u for u in self.units if u.pos == p]
    return len(blockingWalls + blockingUnits) > 0

  # def L1(self, start, end):
  #   return abs(start[0] - end[0]) + abs(start[1] - end[1])

  # def aStar(self, start, end):
  #   l1 = self.L1(start,end)
  #   if l1 == 0:
  #     return 0, [start]
  #   if l1 == 1:
  #     return 1, [start, end]
  #   closedSet = []
  #   openSet = [start]
  #   gScore = { start: 0 }
  #   fScore = { start: self.L1(start,end) }
  #   cameFrom = {}
  #   while len(openSet) > 0:
  #     current = min(openSet, key=lambda p: fScore[p])
  #     if current == end:
  #       path = [current]
  #       while current in cameFrom:
  #           current = cameFrom[current]
  #           path.append(current)
  #       path.reverse()
  #       return fScore[end], path
  #     openSet.remove(current)
  #     closedSet.append(current)
  #     cX, cY = current[0], current[1]
  #     neighbours = [n for n in [(cX-1,cY),(cX+1,cY),(cX,cY-1),(cX,cY+1)] if not self.isBlocked(n) or n == start or n == end]
  #     for n in neighbours:
  #       if n in closedSet:
  #         continue
  #       g = gScore[current] + 1
  #       if n not in openSet:
  #         openSet.append(n)
  #       elif n in gScore and g >= gScore[n]:
  #         continue
  #       gScore[n] = g
  #       fScore[n] = g + self.L1(n, end)
  #       cameFrom[n] = current
  #   return None, None

  def getFreeNeighbours(self, point):
    (x,y) = point
    neighbours = [
      (x-1,y),
      (x+1,y),
      (x,y-1),
      (x,y+1)
    ]
    return [n for n in neighbours if not self.isBlocked(n)]

  def getClosestPoint(self, source, points):
    if source in points:
      return source
    forgottenPoints = set()
    prevPoints = set([source])
    while True:
      nextPoints = [n for p in prevPoints for n in self.getFreeNeighbours(p) if n not in forgottenPoints and n not in prevPoints]
      if len(nextPoints) == 0:
        return None
      found = [p for p in points if p in nextPoints]
      if len(found) > 0:
        point = sorted(found, key=lambda p: (p[1],p[0]))[0]
        return point
      forgottenPoints = set(list(prevPoints) + list(forgottenPoints))
      prevPoints = set(nextPoints)  

  def iterate(self):
    sortedUnits = sorted(self.units, key=lambda u: (u.y,u.x))
    for unit in sortedUnits:
      if unit.isDead():
        continue
      enemies = [u for u in self.units if u.team != unit.team]

      if len(enemies) == 0:
        return False

      enemyInRange = (min([self.L1(unit.pos, enemy.pos) for enemy in enemies]) == 1)
      
      if not enemyInRange:
        attackPositions = list(set([n for enemy in enemies for n in self.getFreeNeighbours(enemy.pos)]))
        closestAttackPosition = self.getClosestPoint(unit.pos, attackPositions)
        
        if closestAttackPosition is None:
          continue

        possibleSteps = [n for n in self.getFreeNeighbours(unit.pos)]
        nextStep = self.getClosestPoint(closestAttackPosition, possibleSteps)
        if nextStep:
          unit.move(*nextStep)

      enemyInRange = (min([self.L1(unit.pos, enemy.pos) for enemy in enemies]) == 1)
      if enemyInRange:
        target = sorted([enemy for enemy in enemies if self.L1(unit.pos, enemy.pos) == 1], key=lambda e: (e.hp,e.y,e.x))[0]
        unit.attack(target)
        if target.isDead():
          self.units.remove(target)
    return True
  
  def remainingTeams(self):
    return list(set([u.team for u in self.units]))


def parseInput(elfAtk=3):
  with open('input', 'r') as f:
    lines = f.readlines()
  walls = []
  units = []
  for y in range(len(lines)):
    for x in range(len(lines[y])):
      c = lines[y][x]
      if c == '#':
        walls.append(Wall(x, y))
      elif c == 'G':
        units.append(Goblin(x,y))
      elif c == 'E':
        units.append(Elf(x,y,elfAtk))
  return Map(units, walls)

def run1():
  map = parseInput()
  turnCount = 0
  while len(map.remainingTeams()) > 1:
    print('Round {}: Goblins: {}, Elves: {}'.format(
      turnCount + 1,
      len([u for u in map.units if u.team == Team.GOBLIN]),
      len([u for u in map.units if u.team == Team.ELF])))
    fullRound = map.iterate()
    print('Round {}: Goblins: {}, Elves: {}'.format(
      turnCount + 1,
      len([u for u in map.units if u.team == Team.GOBLIN]),
      len([u for u in map.units if u.team == Team.ELF])))
    if fullRound:
      turnCount += 1
    print(map)
    print()
  return sum([u.hp for u in map.units]) * turnCount

def run2():
  elfAtk = 4
  while True:
    turnCount = 0
    map = parseInput(elfAtk)
    numElves = len([u for u in map.units if u.team == Team.ELF])
    while len(map.remainingTeams()) > 1:
      fullRound = map.iterate()
      print('Atk: {} - Round {}: Goblins: {}, Elves: {}'.format(
        elfAtk,
        turnCount + 1,
        len([u for u in map.units if u.team == Team.GOBLIN]),
        len([u for u in map.units if u.team == Team.ELF])))
      if fullRound:
        turnCount += 1
      print(map)
      print()
      numElvesRemaining = len([u for u in map.units if u.team == Team.ELF])
      if numElvesRemaining < numElves:
        break
    if numElvesRemaining == numElves:
      return sum([u.hp for u in map.units]) * turnCount
    elfAtk += 1

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))