def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  return [Star(*[int(i) for i in line.strip().split(',')]) for line in lines]

def L1(t1, t2):
  return sum([abs(n-m) for n,m in zip(t1, t2)])

class Star(object):
  def __init__(self, x, y, z, t):
    self.pos = (x,y,z,t)
  
  def __str__(self):
    return str(self.pos)

  def isInRangeOfStar(self, star):
    return L1(self.pos, star.pos) <= 3

  def isInRangeOfConstellation(self, constellation):
    for star in constellation.stars:
      if self.isInRangeOfStar(star):
        return True
    return False

  def isInRange(self, thing):
    if isinstance(thing, Star):
      return self.isInRangeOfStar(thing)
    elif isinstance(thing, Constellation):
      return self.isInRangeOfConstellation(thing)


class Constellation(object):
  def __init__(self, stars = []):
    self.stars = set(stars)
  
  def __str__(self):
    strs = ','.join([str(s) for s in self.stars])
    return f'[{strs}]'

  def isInRangeOfStar(self, star):
    for s in self.stars:
      if s.isInRangeOfStar(star):
        return True
    return False

  def isInRangeOfConstellation(self, constellation):
    for star in constellation.stars:
      if self.isInRangeOfStar(star):
        return True
    return False

  def isInRange(self, thing):
    if isinstance(thing, Star):
      return self.isInRangeOfStar(thing)
    elif isinstance(thing, Constellation):
      return self.isInRangeOfConstellation(thing)

  def addStar(self, star):
    self.stars.add(star)

  def addConstellation(self, constellation):
    for star in constellation.stars:
      self.addStar(star)

  def add(self, thing):
    if isinstance(thing, Star):
      return self.addStar(thing)
    elif isinstance(thing, Constellation):
      return self.addConstellation(thing)

def formConstellatons(stars):
  constellations = [Constellation([star]) for star in stars]
  numConstellations = len(constellations)
  while True:
    newConstellations = set()
    for c1 in constellations:
      merged = False
      for c2 in newConstellations:
        if c1.isInRange(c2):
          c2.addConstellation(c1)
          merged = True
          break
      if not merged:
        newConstellations.add(c1)
    constellations = newConstellations

    if len(constellations) == numConstellations:
      break
    numConstellations = len(constellations)
  
  return constellations

def run1():
  stars = parseInput()
  constellations = formConstellatons(stars)
  return len(constellations)

if __name__ == '__main__':
  print(f'Part 1: {run1()}')