class Node(object):
  def __init__(self, children, metadata):
    self.children = children
    self.metadata = metadata
  def metadataSum(self):
    return sum(self.metadata) + sum([child.metadataSum() for child in self.children])
  def getValue(self):
    if len(self.children) == 0:
      return sum(self.metadata)
    return sum([
      0 if m == 0 or m-1 >= len(self.children) else self.children[m-1].getValue()
      for m in self.metadata
    ])

class Queue(object):
  def __init__(self, arr):
    self.arr = arr
    self.idx = 0
  def next(self):
    ret = self.arr[self.idx]
    self.idx += 1
    return ret
  def __len__(self):
    return len(self.arr)

def getNode(numbers):
  numChildren = numbers.next()
  numMetadata = numbers.next()
  children = [getNode(numbers) for n in range(numChildren)]
  metadata = [numbers.next() for n in range(numMetadata)]
  return Node(children, metadata)

def parseInput():
  with open('input', 'r') as f:
    line = f.read()
  numbers = Queue([int(i) for i in line.split(' ')])
  return getNode(numbers)

def run1():
  root = parseInput()
  return root.metadataSum()

def run2():
  root = parseInput()
  return root.getValue()

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')


