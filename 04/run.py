import re
from datetime import datetime

eventRegex = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.*)'
guardIdRegex = r'Guard #(\d+) begins shift'

class Event(object):
  def __init__(self, timestamp, event):
    self.timestamp = timestamp
    self.event = event
  
  def __str__(self):
    return '[{}] {}'.format(datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M'), self.event)

class Period(object):
  def __init__(self, start, end):
    self.start = start
    self.end = end
  
  def __len__(self):
    return int((self.end.timestamp - self.start.timestamp).total_seconds() / 60)

  def contains(self, minute):
    startMinute = self.start.timestamp.minute
    endMinute = self.end.timestamp.minute
    return startMinute <= minute and minute < endMinute

class Shift(object):
  def __init__(self, events):
    startShift = events[0]
    self.guard = int(re.match(guardIdRegex, startShift.event).group(1))
    self.sleeps = [Period(events[i], events[i+1]) for i in range(1, len(events), 2)]

  def __str__(self):
    return '#{}: {}'.format(self.guard, ', '.join([str(p) for p in self.sleeps]))

  def getSleepArray(self):
    return [len([p for p in self.sleeps if p.contains(m)]) for m in range(0,60)]

  def wasAsleepAt(self, minute):
    return self.getSleepArray()[minute] > 0

  def minsAsleep(self):
    return sum([len(p) for p in self.sleeps])


def parseLine(line):
  match = re.match(eventRegex, line)
  groups = match.groups()
  timestamp = datetime.strptime(groups[0], '%Y-%m-%d %H:%M')
  event = groups[1]
  return Event(timestamp, event)

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  sortedEvents = sorted([parseLine(l) for l in lines], key=lambda event: event.timestamp)

  shifts = []
  current = []
  for event in sortedEvents:
    if len(current) > 0 and re.match(guardIdRegex, event.event):
      shifts.append(current)
      current = []
    current.append(event)
  shifts.append(current)

  return [Shift(shift) for shift in shifts]

def groupBy(arr, func):
  result = {}
  for item in arr:
    key = func(item)
    if key not in result:
      result[key] = []
    result[key].append(item)
  return result

def getTotalShiftsAsleepAt(shifts, minute):
  return sum([1 if shift.wasAsleepAt(minute) else 0 for shift in shifts])

def getMaxMinute(shifts):
  return max(range(0,60), key=lambda m: getTotalShiftsAsleepAt(shifts, m))

def run1():
  shifts = groupBy(parseInput(), lambda shift: shift.guard)
  guard = max(shifts.keys(), key=lambda guard: sum([shift.minsAsleep() for shift in shifts[guard]]))
  minute = getMaxMinute(shifts[guard])
  return guard * minute

def run2():
  shifts = groupBy(parseInput(), lambda shift: shift.guard)
  guard = max(shifts.keys(), key = lambda g: getTotalShiftsAsleepAt(shifts[g], getMaxMinute(shifts[g])))
  minute = getMaxMinute(shifts[guard])
  return guard * minute

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
  