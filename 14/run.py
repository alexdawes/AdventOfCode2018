def parseInput():
  with open('input', 'r') as f:
    return int(f.read())

class Scoreboard(object):
  def __init__(self, values, idx1, idx2):
    self.values = values
    self.idx1 = idx1
    self.idx2 = idx2

  def iterate(self):
    value1 = self.values[self.idx1]
    value2 = self.values[self.idx2]
    newValues = [int(c) for c in str(value1+value2)]
    self.values += newValues
    self.idx1 = (self.idx1 + value1 + 1) % len(self.values)
    self.idx2 = (self.idx2 + value2 + 1) % len(self.values)

def run1():
  numRecipes = parseInput()
  scoreboard = Scoreboard([3,7], 0, 1)
  while len(scoreboard.values) < (numRecipes + 10):
    scoreboard.iterate()
  recipes = scoreboard.values
  return ''.join([str(recipes[i]) for i in range(numRecipes, numRecipes+10)])

def run2():
  recipeStr = str(parseInput())
  scoreboard = Scoreboard([3,7], 0, 1)

  tail = ''.join([str(r) for r in scoreboard.values[-(min([len(scoreboard.values), len(recipeStr)+2])):]])
  while recipeStr not in tail:
    scoreboard.iterate()
    tail = ''.join([str(r) for r in scoreboard.values[-(min([len(scoreboard.values), len(recipeStr)+2])):]])
  return ''.join([str(r) for r in scoreboard.values]).index(recipeStr)

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')