import json

def parseInput():
  with open('input', 'r') as f:
    line = f.read().strip()
  return json.loads(
    line
      .replace('^','["')
      .replace('$','"]')
      .replace('|','"],["')
      .replace('(','",[["')
      .replace(')','"]],"')
  )

def getNextNode(current, direction):
  x,y = current
  if direction == 'N':
    return (x,y+1)
  if direction == 'E':
    return (x+1,y)
  if direction == 'S':
    return (x,y-1)
  if direction == 'W':
    return (x-1,y)
  return current

def exploreSegment(graph, start, segment):
  if isinstance(segment, str):
    return set([explorePath(graph, start, segment)])
  elif isinstance(segment, list):
    return set([end for seg in segment for end in explore(graph, start, seg)])

def explore(graph, start, segments):
  current = set([start])
  for segment in segments:
    current = set([n for c in current for n in exploreSegment(graph, c, segment)])
  return current

def explorePath(graph, start, path):
  if start not in graph.nodes:
    raise f'Cannot explore from {start}'
  current = start
  for d in path:
    nxt = getNextNode(current, d)
    graph.edges.add((current, nxt))
    graph.nodes.add(nxt)
    current = nxt
  return current

class Graph(object):
  def __init__(self):
    self.nodes = set([(0,0)])
    self.edges = set()

  def __str__(self):
    lines = []
    minX, maxX = min([n[0] for n in self.nodes]), max([n[0] for n in self.nodes])
    minY, maxY = min([n[1] for n in self.nodes]), max([n[1] for n in self.nodes])
    lines.append('#' * ((2*(1+maxX - minX))+1))
    for y in range(maxY, minY-1, -1):
      lines.append('#.' + '.'.join(['|' if ((x,y),(x+1,y)) in self.edges or ((x+1,y),(x,y)) in self.edges else '#' for x in range(minX, maxX)]) + '.#')
      lines.append('#' + '#'.join(['-' if ((x,y),(x,y-1)) in self.edges or ((x,y-1),(x,y)) in self.edges else '#' for x in range(minX, maxX+1)]) + '#')
    return '\n'.join(lines)


def getFurthestPoint(nodes, edges):
  prevNodes = set()
  currNodes = set([(0,0)])
  nextNodes = set()
  count = 0
  while True:
    nextNodes = [
      n
      for n in [m for m in nodes if m not in prevNodes and m not in currNodes]
      for c in currNodes
      if ((n,c) in edges or (c,n) in edges)]
    if len(nextNodes) == 0:
      return count
    
    count += 1
    prevNodes = set(list(prevNodes) + list(currNodes))
    currNodes = nextNodes

def getFarAway(nodes, edges, dist):
  prevNodes = set()
  currNodes = set([(0,0)])
  nextNodes = set()
  count = 0
  while count < 1000:
    nextNodes = [
      n
      for n in [m for m in nodes if m not in prevNodes and m not in currNodes]
      for c in currNodes
      if ((n,c) in edges or (c,n) in edges)]
    if len(nextNodes) == 0:
      return count
    
    count += 1
    prevNodes = set(list(prevNodes) + list(currNodes))
    currNodes = nextNodes
  return len(nodes) - len(prevNodes)


def run1():
  segments = parseInput()
  graph = Graph()
  explore(graph, (0,0), segments)
  return getFurthestPoint(graph.nodes, graph.edges)

def run2():
  segments = parseInput()
  graph = Graph()
  explore(graph, (0,0), segments)
  return getFarAway(graph.nodes, graph.edges, 1000)

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')