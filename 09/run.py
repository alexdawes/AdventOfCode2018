import re

regex = r'(\d+) players; last marble is worth (\d+) points'

class Player(object):
  def __init__(self):
    self._score = 0

  def score(self, marble):
    self._score += marble

  def total(self):
    return self._score

class Marble(object):
  def __init__(self, value, nxt):
    self.value = value
    self.next = nxt

def runGame(numPlayers, numMarbles):
  players = [Player() for p in range(numPlayers)]
  
  firstMarble = Marble(0, None)
  firstMarble.next = firstMarble

  current = firstMarble
  playerIdx = 0
  marker = None

  for marble in range(1, numMarbles):
    if marble % 23 == 0:
      player = players[playerIdx]
      player.score(marble)
      removed = marker.next
      marker.next = removed.next
      player.score(removed.value)
      current = marker.next
    else:
      current = current.next
      newMarble = Marble(marble, current.next)
      current.next = newMarble
      current = newMarble
      
      if marble % 23 == 18:
        marker = newMarble

    playerIdx = (playerIdx + 1) % len(players)

  return players

def parseInput():
  with open('input', 'r') as f:
    line = f.read()

  numPlayers, maxMarble = [int(r) for r in re.match(regex, line).groups()]
  numMarbles = maxMarble + 1
  return numPlayers, numMarbles


def run1():
  numPlayers, numMarbles = parseInput()
  results = runGame(numPlayers, numMarbles)
  return max([r.total() for r in results])

def run2():
  numPlayers, numMarbles = parseInput()
  numMarbles = 100 * (numMarbles - 1) + 1
  results = runGame(numPlayers, numMarbles)
  return max([r.total() for r in results])


if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
