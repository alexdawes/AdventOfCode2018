import re

class Square(object):
  def __init__(self, id, x, y, width, height):
    self.id = id
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def __str__(self):
    return '#{} @ {},{}: {}x{}'.format(self.id, self.x, self.y, self.width, self.height)

def parseLine(line):
  return Square(*[int(g) for g in re.match('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line).groups()])

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  return [parseLine(line) for line in lines]

def getCloth(squares):
  width = max([s.x + s.width for s in squares])
  height = max([s.y + s.height for s in squares])
  return [[0 for j in range(height)] for i in range(width)]

def overlay(squares, cloth):
  for s in squares:
    for i in range(s.x, s.x + s.width):
      for j in range(s.y, s.y + s.height):
        cloth[i][j] += 1

def countOverlaps(cloth):
  return len([i for i in range(len(cloth)) for j in range(len(cloth[0])) if cloth[i][j] > 1])

def run1():
  squares = parseInput()
  cloth = getCloth(squares)
  overlay(squares, cloth)
  return countOverlaps(cloth)

def collidesSingle(s1, s2):
  return s1.x < (s2.x + s2.width) and s2.x < (s1.x + s1.width) \
    and s1.y < (s2.y + s2.height) and s2.y < (s1.y + s1.height)

def collides(square, otherSquares):
  for i in range(len(otherSquares)):
    otherSquare = otherSquares[i]
    if collidesSingle(square, otherSquare):
      return True
  return False

def run2():
  squares = parseInput()
  for i in range(len(squares)):
    square = squares[i]
    otherSquares = [squares[j] for j in range(len(squares)) if i != j]
    if not collides(square, otherSquares):
      return square.id

def run2_2():
  squares = parseInput()
  cloth = getCloth(squares)
  overlay(squares, cloth)
  result = None
  for s in squares:
    collision = False
    for i in range(s.x, s.x + s.width):
      for j in range(s.y, s.y + s.height):
        if cloth[i][j] > 1:
          collision = True
          break
    if not collision:
      result = s.id
      break
  return result

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run22()))
