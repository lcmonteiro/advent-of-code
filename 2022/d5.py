#python 3.7.1
'''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
...
'''
from re     import compile 
from pprint import pprint
    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()

def parse_stacks(data):
  regex  = compile(r'.*\[.\].*')
  stacks = []
  for line in data:
    if not regex.match(line):
      if stacks: break
      else     : continue 
    stacks.append(line[1:len(line):4])
  stacks = zip(*stacks)
  stacks = map(reversed,stacks)
  stacks = map(''.join, stacks)
  stacks = map(str.strip, stacks)
  return list(stacks)
  
def parse_moves(data):
  regex = compile(r'move (\d+) from (\d+) to (\d+)')
  moves = []
  for line in data:
    result = regex.match(line)
    if not result:
      if moves: break
      else    : continue 
    moves.append((
      int(result[1]),
      int(result[2]) - 1,
      int(result[3]) - 1))
  moves = map(tuple, moves)
  return list(moves)

def process(stacks, moves):
  split = lambda x,i: (x[:i],x[i:])
  for size, src, dst in moves:
    left, right = split(stacks[src],-size)
    # stacks[dst] = stacks[dst] + right[::-1] # PART-1
    stacks[dst] = stacks[dst] + right[::1]
    stacks[src] = left
  return ''.join(map(lambda x:x[-1],stacks))


data   = list(input_data())
stacks = parse_stacks(data)
moves  = parse_moves(data)
result = process(stacks, moves)
pprint(result)
