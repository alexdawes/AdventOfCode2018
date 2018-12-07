import re

regex = r'Step ([A-Z]{1}) must be finished before step ([A-Z]{1}) can begin\.'

class Node(object):
  def __init__(self, id, before, after):
    self.id = id
    self.before = before
    self.after = after

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  edges = [re.match(regex, line).groups() for line in lines]
  ids = list(set([e[0] for e in edges] + [e[1] for e in edges]))
  nodes = [Node(id, list(set([e[0] for e in edges if e[1] == id])), list(set([e[1] for e in edges if e[0] == id]))) for id in ids]
  return { n.id: n for n in nodes }

def nodeIsAvailable(node, path):
  return node.id not in path and len([n for n in node.before if n not in path]) == 0

def getAvailable(nodes, path):
  return sorted([n.id for n in nodes.values() if nodeIsAvailable(n, path)], key=lambda n: n)

def getNext(nodes, path):
  available = getAvailable(nodes, path)
  return available[0] if len(available) > 0 else None

def run1():
  nodes = parseInput()
  path = []
  while True:
    nextNode = getNext(nodes, path)
    if nextNode:
      path.append(nextNode)
    else:
      break
  return ''.join(path)

def getTimeRequired(nodeId):
  return ord(nodeId) - 4

class Worker(object):
  def __init__(self):
    self.node = None
    self.time = None

  def startTask(self, node):
    self.node = node
    self.time = 0

  def logWork(self):
    self.time += 1

  def completeTask(self):
    self.node = None
    self.time = None

  def isIdle(self):
    return self.node is None

  def __str__(self):
    return '.' if self.isIdle() else self.node

def run2():
  nodes = parseInput()
  path = []
  workers = [Worker(), Worker(), Worker(), Worker(), Worker()]
  timeCount = 0
  while True:
    for worker in workers:
      if not worker.isIdle():
        if worker.time >= getTimeRequired(worker.node):
          path.append(worker.node)
          worker.completeTask()
        else:
          worker.logWork()
    for worker in workers:
      if worker.isIdle():
        availableNodes = getAvailable(nodes, path)
        actualAvailableNodes = [n for n in availableNodes if n not in [w.node for w in workers if not w.isIdle()]]
        if len(actualAvailableNodes) > 0:
          worker.startTask(actualAvailableNodes[0])
          worker.logWork()

    # print('{}: {} {}'.format(timeCount, ' '.join([str(w) for w in workers]), ''.join(path)))

    if len([w for w in workers if not w.isIdle()]) == 0:
      break
    timeCount += 1
  return timeCount


if __name__ == '__main__':
  print('Part 1: {}'.format(run1()))
  print('Part 2: {}'.format(run2()))

