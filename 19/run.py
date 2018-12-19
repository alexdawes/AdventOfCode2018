import re

ippRegex = r'#ip (\d+)'
instrRegex = r'(addr|addi|mulr|muli|banr|bani|borr|bori|setr|seti|gtir|gtri|gtrr|eqir|eqri|eqrr) (\d+) (\d+) (\d+)'

def parseInput():
  with open('input', 'r') as f:
    lines = f.readlines()
  ippLine, instrLines = lines[0], lines[1:]
  ipp = int(re.match(ippRegex, ippLine).group(1))
  instrMatches = [re.match(instrRegex, line) for line in instrLines]
  instrs = [(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))) for m in instrMatches]
  return ipp, instrs

def addr(reg, a, b, c):
  reg[c] = reg[a] + reg[b]

def addi(reg, a, b, c):
  reg[c] = reg[a] + b

def mulr(reg, a, b, c):
  reg[c] = reg[a] * reg[b]

def muli(reg, a, b, c):
  reg[c] = reg[a] * b

def banr(reg, a, b, c):
  reg[c] = reg[a] & reg[b]

def bani(reg, a, b, c):
  reg[c] = reg[a] & b

def borr(reg, a, b, c):
  reg[c] = reg[a] | reg[b]

def bori(reg, a, b, c):
  reg[c] = reg[a] | b

def setr(reg, a, b, c):
  reg[c] = reg[a]

def seti(reg, a, b, c):
  reg[c] = a

def gtir(reg, a, b, c):
  reg[c] = 1 if a > reg[b] else 0

def gtri(reg, a, b, c):
  reg[c] = 1 if reg[a] > b else 0

def gtrr(reg, a, b, c):
  reg[c] = 1 if reg[a] > reg[b] else 0

def eqir(reg, a, b, c):
  reg[c] = 1 if a == reg[b] else 0

def eqri(reg, a, b, c):
  reg[c] = 1 if reg[a] == b else 0

def eqrr(reg, a, b, c):
  reg[c] = 1 if reg[a] == reg[b] else 0


instructions = {
  'addr': addr,
  'addi': addi,
  'mulr': mulr,
  'muli': muli,
  'banr': banr,
  'bani': bani,
  'borr': borr,
  'bori': bori,
  'setr': setr,
  'seti': seti,
  'gtir': gtir,
  'gtri': gtri,
  'gtrr': gtrr,
  'eqir': eqir,
  'eqri': eqri,
  'eqrr': eqrr
}

def run(reg, ipp, instrs, numIterations=None):
  count = 0
  while numIterations is None or count < numIterations:
    count += 1

    if reg[ipp] not in range(len(instrs)):
      break

    ip = reg[ipp]
    instr = instrs[ip]
    instrFn = instructions[instr[0]]
    instrArgs = instr[1:]
    regCp = [r for r in reg]
    instrFn(reg, *instrArgs)

    instrStr = ' '.join([str(i) for i in instr])

    reg[ipp] += 1

def run1():
  ipp, instrs = parseInput()
  reg = [0,0,0,0,0,0]
  run(reg, ipp, instrs)
  return reg[0]
  
def run2():
  ipp, instrs = parseInput()
  reg = [1,0,0,0,0,0]
  run(reg, ipp, instrs, 20)
  num = reg[4]
  ttl = 0
  for i in range(1, num+1):
    if num % i == 0:
      ttl += i
  return ttl

if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
    

