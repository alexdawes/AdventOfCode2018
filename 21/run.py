def run1():
  b, c, e, f = 0, 0, 0, 0
  e = f | 65536
  f = 8858047
  while True:
    f = (((f + (e & 255)) & 16777215) * 65899) & 16777215
    if 256 > e:
      break
    e = e // 256

  return f
  
def run2():
  b, c, e, f = 0, 0, 0, 0
  fValues = []
  while True:
    e = f | 65536
    f = 8858047
    while True:
      f = (((f + (e & 255)) & 16777215) * 65899) & 16777215
      if 256 > e:
        break
      e = e // 256

    if f in fValues:
      return fValues[-1]
    else:
      fValues.append(f)
  
if __name__ == '__main__':
  print(f'Part 1: {run1()}')
  print(f'Part 2: {run2()}')
    

