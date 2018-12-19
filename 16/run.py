import re

p1Regex = [
  r'Before: \[(\d+), (\d+), (\d+), (\d+)\]',
  r'(\d+) (\d+) (\d+) (\d+)',
  r'After:  \[(\d+), (\d+), (\d+), (\d+)\]'
]

p2Regex = r'(\d+) (\d+) (\d+) (\d+)'

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


def parseInput1():
  results = []
  with open('input1', 'r') as f:
    lines = f.readlines()
  for i in range(0, len(lines), 4):
    subLines = [l.strip() for l in lines[i:i+3]]
    results.append(tuple([[int(d) for d in re.match(p1Regex[j], subLines[j]).groups()] for j in range(3)]))
  return results

def parseInput2():
  with open('input2', 'r') as f:
    lines = f.readlines()
  return [[int(g) for g in re.match(p2Regex, line).groups()] for line in lines]

def clone(reg):
  return [r for r in reg]

def run1():
  tests = parseInput1()
  results = []
  for i in range(len(tests)):
    (before, instr, after) = tests[i]
    args = instr[1:]
    result = []
    for instrKey, instrFn in instructions.items():
      bef = clone(before)
      instrFn(bef, *args)
      if bef == after:
        result.append(instrKey)
    results.append(result)
  return len([r for r in results if len(r) >= 3])

def run2():
  tests = parseInput1()
  instrs = { i: list(instructions.keys()) for i in range(len(instructions)) }
  for i in range(len(tests)):
    (before, instr, after) = tests[i]
    instr, args = instr[0], instr[1:]
    for instrKey in instrs[instr]:
      bef = clone(before)
      instructions[instrKey](bef, *args)
      if bef != after:
        instrs[instr].remove(instrKey)
  
  countDetermined = 0
  while True:
    if len([k for k,v in instrs.items() if len(v) > 1]) == 0:
      break

    determined = [k for k,v in instrs.items() if len(v) == 1]
    determinedInstrs = [instrs[k][0] for k in determined]

    if len(determined) == countDetermined:
      break
    countDetermined = len(determined)

    for k, v in instrs.items():
      if k in determined:
        continue
      for instr in determinedInstrs:
        if instr in v:
          v.remove(instr)

  if len([k for k,v in instrs.items() if len(v) > 1]) > 0:
    return 'Failed'

  instrs = { k: v[0] for k,v in instrs.items() }
  
  program = parseInput2()
  reg = [0,0,0,0]
  for instr in program:
    instr, args = instr[0], instr[1:]
    instrKey = instrs[instr]
    instrFn = instructions[instrKey]
    instrFn(reg, *args)

  return reg[0]


if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
  