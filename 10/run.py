import re
import matplotlib.pyplot as plt
import numpy as np

regex = 'position=<([-\s]\d+), ([-\s]\d+)> velocity=<([-\s]\d+), ([-\s]\d+)>'

class Vector(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def add(self, vec):
    return Vector(self.x + vec.x, self.y + vec.y)
  def __str__(self):
    return '({}, {})'.format(self.x, self.y)

class Light(object):
  def __init__(self, x, y, vx, vy):
    self.position = Vector(x, y)
    self.velocity = Vector(vx, vy)
  def iterate(self):
    self.position = self.position.add(self.velocity)
  def __str__(self):
    return '{} [{}]'.format(str(self.position), str(self.velocity))
  

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  matches = [re.match(regex, l) for l in lines]
  return [Light(*[int(g.strip()) for g in m.groups()]) for m in matches]

def plot(lights):
  x = np.array([l.position.x for l in lights])
  y = np.array([-l.position.y for l in lights])
  plt.plot(x, y, 'o')
  plt.axes().set_aspect('equal', 'datalim')
  plt.show(block=True)

def run1():
  lights = parseInput()  
  while(True):
    if (max([l.position.x for l in lights]) - min([l.position.x for l in lights]) < 70) \
      and (max([l.position.y for l in lights]) - min([l.position.y for l in lights]) < 15):
      plot(lights)
      return 'See Image'
    for l in lights:
      l.iterate()
      
def run2():
  lights = parseInput()
  count = 0
  while(True):
    if (max([l.position.x for l in lights]) - min([l.position.x for l in lights]) < 70) \
      and (max([l.position.y for l in lights]) - min([l.position.y for l in lights]) < 15):
      return count
    for l in lights:
      l.iterate()
    count += 1

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))

  