import re
import math

lineRegex = r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)'

def L1(p1, p2):
  (x1,y1,z1) = p1
  (x2,y2,z2) = p2
  return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

class NanoBot(object):
  def __init__(self, x, y, z, r):
    self.pos = (x,y,z)
    self.radius = r

  def inRange(self, other):
    return self.pointInRange(other.pos)

  def pointInRange(self, point, mod=0):
    return L1(self.pos, point) <= self.radius + mod

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()

  return [NanoBot(*[int(g) for g in re.match(lineRegex, line.strip()).groups()]) for line in lines]

def run1():
  nanobots = parseInput()
  strongest = max(nanobots, key=lambda nb: nb.radius)
  inRange = [n for n in nanobots if strongest.inRange(n)]
  return len(inRange)

def run2():
  nanobots = parseInput()
  xs, ys, zs = [n.pos[0] for n in nanobots], [n.pos[1] for n in nanobots], [n.pos[2] for n in nanobots]

  minX, maxX, minY, maxY, minZ, maxZ = min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
  minSide = min([maxX-minX, maxY-minY, maxZ-minZ])
  step = int(math.pow(2, int(math.log(minSide, 2)) - 1))

  while step > 1:
    points = [
      (x,y,z)
      for x in range(minX, maxX+1, step)
      for y in range(minY, maxY+1, step)
      for z in range(minZ, maxZ+1, step)
    ]

    best = None
    for point in points:
      numInRange = len([n for n in nanobots if n.pointInRange(point)])
      if best is None or (numInRange > best[0]) or (numInRange == best[0] and L1(point, (0,0,0)) < L1(best[1], (0,0,0))):
        best = (numInRange, point)

    minX, maxX = best[1][0] - step, best[1][0] + step
    minY, maxY = best[1][1] - step, best[1][1] + step
    minZ, maxZ = best[1][2] - step, best[1][2] + step
    step = int(step / 2)

  return L1(best[1], (0,0,0))

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')