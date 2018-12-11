def parseInput():
  with open('input', 'r') as f:
    return int(f.read())

def getValue(x, y, sn):
  rankId = x + 10                           # Find the fuel cell's rack ID, which is its X coordinate plus 10.
  powerLevel = rankId * y                   # Begin with a power level of the rack ID times the Y coordinate.
  powerLevel += sn                          # Increase the power level by the value of the grid serial number.
  powerLevel *= rankId                      # Set the power level to itself multiplied by the rack ID.
  powerLevel = int(powerLevel/100) % 10     # Keep only the hundreds digit of the power level.
  powerLevel -= 5                           # Subtract 5 from the power level.
  return powerLevel

def getValues(xDim, yDim, sn):
  return {(x,y): getValue(x, y, sn) for y in range(1, yDim+1) for x in range(1, xDim+1)}

def getTotal(x, y, n, zeroTotals):
  return zeroTotals[(x+n-1,y+n-1)] - zeroTotals[(x-1,y+n-1)] - zeroTotals[(x+n-1,y-1)] + zeroTotals[(x-1,y-1)]

def getZeroTotals(xDim, yDim, values):
  zeroTotals = { (0,0): 0, **{(i,0): 0 for i in range(1, xDim+1)}, **{(0,j): 0 for j in range(1, yDim+1)} }
  for x in range(1, xDim+1):
    for y in range(1, yDim+1):
      zeroTotals[(x,y)] = zeroTotals[(x,y-1)] + zeroTotals[(x-1,y)] - zeroTotals[(x-1,y-1)] + values[(x,y)]
  return zeroTotals

def run1():
  sn = parseInput()
  values = getValues(300, 300, sn)
  zeroTotals = getZeroTotals(300, 300, values)
  coord = max(
    [(x,y) for x in range(1,300-1) for y in range(1,300-1)],
    key=lambda t: getTotal(*t, 3, zeroTotals)
  )
  return '{},{}'.format(*coord)

def run2():
  sn = parseInput()
  values = getValues(300, 300, sn)
  zeroTotals = getZeroTotals(300, 300, values)
  coord = max(
    [(x,y,n) for x in range(1,300+1) for y in range(1,300+1) for n in range(1, min([300-x+1,300-y+1]))],
    key=lambda t: getTotal(*t, zeroTotals)
  )
  return '{},{},{}'.format(*coord)

if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))



