import re

lineRegex = r'(\d+) units each with (\d+) hit points (\([A-z,;\s]+\))?\s?with an attack that does (\d+) (\w+) damage at initiative (\d+)'
weaknessRegex = r'.*weak to ([a-z\s,]+)'
immunityRegex = r'.*immune to ([a-z\s,]+)'

def getWeaknesses(line):
  match = re.match(weaknessRegex, line)
  if match is None:
    return []
  weaknesses = match.group(1).split(', ')
  return weaknesses

def getImmunities(line):
  match = re.match(immunityRegex, line)
  if match is None:
    return []
  immunities = match.group(1).split(', ')
  return immunities

def parseLine(line, team, _id):
  match = re.match(lineRegex, line)
  units = int(match.group(1))
  hp = int(match.group(2))
  weaknesses = getWeaknesses(line)
  immunities = getImmunities(line)
  dmg = int(match.group(4))
  dmgType = match.group(5)
  init = int(match.group(6))
  return Group(_id, units, hp, weaknesses, immunities, dmg, dmgType, init, team)

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()

  groups = []
  _id = 1
  for line in lines:
    line = line.strip()
    if line == 'Immune System:':
      currentTeam = TEAM_IMMUNE
      _id = 1
    elif line == 'Infection:':
      currentTeam = TEAM_INFECTION
      _id = 1
    elif line == '':
      continue
    else:
      group = parseLine(line, currentTeam, _id)
      groups.append(group)
      _id += 1
  
  return groups

TEAM_IMMUNE = 'Immune System'
TEAM_INFECTION = 'Infection'

class Group(object):
  def __init__(self, _id, units, hp, weaknesses, immunities, dmg, dmgType, init, team):
    self._id = _id
    self.units = units
    self.hp = hp
    self.weaknesses = weaknesses
    self.immunities = immunities
    self.dmg = dmg
    self.dmgType = dmgType
    self.init = init
    self.team = team

  def __str__(self):
    return f'Units: {self.units}, HP: {self.hp}, Weak: {self.weaknesses}, Immu: {self.immunities}, Dmg: {self.dmg}, DmgType: {self.dmgType}, Init: {self.init}'

  def getEffectivePower(self):
    return self.units * self.dmg

  def isAlive(self):
    return self.units > 0

  def isWeakTo(self, dmgType):
    return dmgType in self.weaknesses

  def isImmuneTo(self, dmgType):
    return dmgType in self.immunities

  def takeDamage(self, dmg):
    unitsKilled = min([dmg // self.hp, self.units])
    self.units -= unitsKilled
    return unitsKilled

def runTargetSelection(groups):
  orderedGroups = sorted(groups, key=lambda g: (-g.getEffectivePower(), -g.init))
  targets = {}
  for group in orderedGroups:
    enemies = [g for g in groups if g.team != group.team and g not in targets.values()]
    damages = {}
    for enemy in enemies:
      damageDealt = group.getEffectivePower()
      damageType = group.dmgType
      if enemy.isWeakTo(damageType):
        damageDealt *= 2
      if enemy.isImmuneTo(damageType):
        damageDealt = 0
      damages[enemy] = damageDealt

      # if damageDealt > 0:
      #   print(f'{group.team} group {group._id} would deal {enemy.team} group {enemy._id} {damageDealt} damage.')

    damagedEnemies = [e for e in enemies if damages[e] > 0]
    if len(damagedEnemies) == 0:
      continue
    chosenTarget = sorted(damagedEnemies, key=lambda e: (-damages[e], -e.getEffectivePower(), -e.init))[0]
    targets[group] = chosenTarget
 
  # print() 

  return targets
    
def runAttack(groups, targets):
  orderedGroups = sorted(groups, key=lambda g: (-g.init))
  for group in orderedGroups:
    if group not in targets or group.units <= 0:
      continue
    target = targets[group]
    damageDealt = group.getEffectivePower()
    damageType = group.dmgType
    if target.isWeakTo(damageType):
      damageDealt *= 2
    if target.isImmuneTo(damageType):
      damageDealt = 0

    unitsKilled = target.takeDamage(damageDealt)
    # print(f'{group.team} group {group._id} attacks {target.team} group {target._id}, killing {unitsKilled} units.')
  
  for group in [g for g in orderedGroups if g.units <= 0]:
    groups.remove(group)
  
  # print()

def runFight(groups):
  # immuneGroups = [g for g in groups if g.team == TEAM_IMMUNE]
  # infectionGroups = [g for g in groups if g.team == TEAM_INFECTION]
  # print(f'{TEAM_IMMUNE}:')
  # for g in immuneGroups:
  #   print(f'Group {g._id} contains {g.units} units')
  # print(f'{TEAM_INFECTION}:')
  # for g in infectionGroups:
  #   print(f'Group {g._id} contains {g.units} units')
  # print()

  targets = runTargetSelection(groups)
  runAttack(groups, targets)

  return len(targets) > 0 and len(set([g.team for g in groups])) > 1

  # print()

def runBattle(groups):
  count = 1
  numUnits = sum([g.units for g in groups])
  while len(set([g.team for g in groups])) > 1:
    # print(f'Fight {count}')
    runFight(groups)
    count += 1
    newNumUnits = sum([g.units for g in groups])
    if newNumUnits == numUnits:
      break
    else:
      numUnits = newNumUnits

def run1():
  groups = parseInput()

  # for g in groups:
  #   print(g)
  # print()

  runBattle(groups)
  winningTeam = list(set([g.team for g in groups]))[0]
  winningGroups = [g for g in groups if g.team == winningTeam]
  return sum([g.units for g in winningGroups])

def run2():
  boost = 1

  while True:
    # print(f'Running for boost {boost}')
    groups = parseInput()
    for g in groups:
      if g.team == TEAM_IMMUNE:
        g.dmg += boost
    runBattle(groups)
    if len(set([g.team for g in groups])) > 1:
      boost += 1
      continue
    winningTeam = list(set([g.team for g in groups]))[0]
    if winningTeam == TEAM_IMMUNE:
      winningGroups = [g for g in groups if g.team == winningTeam]
      return sum([g.units for g in winningGroups])
    else:
      boost += 1

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
  

  