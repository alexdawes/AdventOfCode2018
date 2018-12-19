class Coord(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def dist(self, otherCoord):
    return abs(self.x - otherCoord.x) + abs(self.y - otherCoord.y)

  def shift(self, x, y):
    return Coord(self.x + x, self.y + y)


def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  split = [s.split(',') for s in lines]
  coords = [(int(s[0].strip()), int(s[1].strip())) for s in split]
  return [Coord(s[0], s[1]) for s in coords]

def getShift(coords):
  minX, minY = min([c.x for c in coords]), min([c.y for c in coords])
  shiftX, shiftY = -minX, -minX 
  return Coord(shiftX, shiftY)

def shift(coords, shift):
  return [c.shift(shift.x, shift.y) for c in coords]

def getGrid(coords):
  maxX, maxY = max([c.x for c in coords]), max([c.y for c in coords])
  return [[None for y in range(maxY)] for x in range(maxX)]

def populateAreas(grid, coords):
  width = len(grid)
  height = len(grid[0])
  for x in range(width):
    for y in range(height):
      gc = Coord(x, y)
      dists = { c: gc.dist(c) for c in coords }
      minValue = min(dists.values())
      minCoords = [ c for c in coords if dists[c] == minValue ]
      count = len(minCoords)
      if count == 1:
        grid[x][y] = minCoords[0]

def populateTotalDists(grid, coords):
  width = len(grid)
  height = len(grid[0])
  for x in range(width):
    for y in range(height):
      gc = Coord(x, y)
      dists = [gc.dist(c) for c in coords]
      totalDist = sum(dists)
      grid[x][y] = totalDist

def getBoundary(grid):
  return grid[0] + grid[len(grid) - 1] + [c[0] for c in grid] + [c[len(c) - 1] for c in grid]

def getAreaSizes(grid):
  results = {}
  width = len(grid)
  height = len(grid[0])
  for x in range(width):
    for y in range(height):
      if grid[x][y] is not None:
        coord = grid[x][y]
        if coord not in results:
          results[coord] = 0
        results[coord] += 1
  return results


def run1():
  coords = parseInput()
  shft = getShift(coords)
  coords = shift(coords, shft)
  grid = getGrid(coords)
  populateAreas(grid, coords)
  boundaryCoords = list(set(getBoundary(grid)))
  nonBoundaryCoords = [c for c in coords if c not in boundaryCoords]
  areaSizes = getAreaSizes(grid)
  return max([areaSizes[c] for c in nonBoundaryCoords])

def run2():
  coords = parseInput()
  shft = getShift(coords)
  coords = shift(coords, shft)
  grid = getGrid(coords)
  populateTotalDists(grid, coords)
  return len([grid[x][y] for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] < 10000])


if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
