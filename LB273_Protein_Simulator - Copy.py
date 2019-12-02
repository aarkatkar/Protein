import matplotlib.pyplot as plt
from matplotlib import style
import time

##style.use('fivethirtyeight')

def isEquivalent(first_route, second_route):
    s = reversed(second_route)
    flip = True
    negflip = True
    length = len(first_route)
        
    for i in range(length):
        if flip and first_route[i] != second_route[length-i-1]:
            flip = False
        if negflip and first_route[i] != -second_route[length-i-1]:
            negflip = False
        if flip or negflip:
            continue
        else:
            return False
    return True

def isValid(c):
    posset = set([(0,0), (0,1)])
    direction = (0,1)
    pos = (0,1)
    for d in c:
        direction = turn(direction, d)
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        if pos in posset:
            return False
        posset.add(pos)
    return True

def simulate(nodes):
    start_time = time.time()
    shape_size = nodes - 2
    candidates = []
    for n in range(3**shape_size):
        number = []
        remainder = n
        left = False
        for i in range(shape_size)[::-1]:
            digit = 3**i
            if remainder >= digit:
                floor = remainder//digit
                if floor == 1:
                    number.append(1)
                    left = True
                elif left:
                    number.append(-1)
                else:
                    break
                remainder = remainder % digit
            else:
                number.append(0)
        else:
            candidates.append(tuple(number))
    
    found = set()
    for route in candidates:
        if not isValid(route):
            continue
        for f in found:
            if isEquivalent(route, f):
                break
        else:
            found.add(route)
    print(time.time()-start_time)
    plot_all(found, shape_size)

unit_circle = [(0,1), (1,0), (0,-1), (-1,0)]
index_map = dict(zip(unit_circle, [unit_circle.index(t) for t in unit_circle]))
def turn(previous, enter):
    previous_index = index_map[previous]
    i = (previous_index + enter) % 4
    return unit_circle[i]

def show_all(nodes):
    shape_size = nodes - 2
    candidates = []
    for n in range(3**shape_size):
        number = []
        remainder = n
        for i in range(shape_size)[::-1]:
            digit = 3**i
            if remainder >= digit:
                floor = remainder//digit
                if floor == 1:
                    number.append(1)
                else:
                    number.append(-1)
                remainder = remainder % digit
            else:
                number.append(0)
        candidates.append(tuple(number))
    plot_all(candidates, shape_size)

def plot(c, offset=(0,0)):
    posset = [(0,0), (0,1)]
    direction = (0,1)
    pos = (0,1)
    for d in c:
        direction = turn(direction, d)
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        posset.append(pos)
    ax.plot([x[0]+offset[0] for x in posset], [y[1]+offset[1] for y in posset])

def plot_all(routes, shape_size):
    fig = plt.figure()
    global ax
    ax = fig.add_subplot(111, aspect='equal')
    row_number = int(len(routes)**0.5)
    x0 = 0
    y0 = 0
    for i, r in enumerate(routes):
        if i % row_number == 0 and i != 0:
            x0 = 0
            y0 += shape_size+3
        plot(r, offset=(x0,y0))
        x0 += shape_size+3
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.title('N = {}'.format(shape_size+2))
    plt.show()
        
