from random import randint
test = [[[1,0],[1,0]],[[1,0],[1,0]]]

#creats a nxn array
def starting_map(n):
    map = []
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append([1,0])
        map.append(temp)
    return map

#nicly prints array out
def print_array(data):
    for row in data:
        print(row,"\n")
    print("\n")


# this takes an nxn array and puts [2] directly in the middle if n is odd.
# And randomly as close to the middle as possible if n is even
def start_fire(data):
    n = len(data)
    rand1 = randint(0,100)
    rand2 = randint(0,100)

    if n % 2 == 0:
        if rand1 > 50:
            i = int((n/2) -1)
        else:
            i = int(n/2)
        if rand2 > 50:
            j = int((n/2) -1)
        else:
            j = int(n/2)
    else:
        i = int(((n+1)/2)-1)
        j = i
    data[i][j][0] = 2
    return data



# This finds the fire before it spreads so that I can toggle it off in another fire
def find_fire(map):
    fire = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j][0] == 2:
                fire.append((i,j))
            elif map[i][j][0] == 4: # lightning is still considered a fire and so it can spread fire.
                fire.append((i,j))
    return fire


# This is where the fire is spread and the array is edited to add the new fire.
def fire_logic(map,fire_loc,spread_const):
    length = len(map)
    fire = fire_loc
    data = map
    for (i,j) in fire:
        if i-1 >=0:
            if randint(0,100) <= spread_const:
                if data[i-1][j][0] == 1:
                    data[i-1][j][0] = 2 # North
        if i+1 <length:
            if randint(0,100) <= spread_const:
                if data[i+1][j][0] == 1:
                    data[i+1][j][0] = 2 # South
        if j-1 >= 0:
            if randint(0,100) <= spread_const:
                if data[i][j-1][0] == 1:
                    data[i][j-1][0] = 2 # East
        if j+1 < length:
            if randint(0,100) <= spread_const:
                if data[i][j+1][0] == 1:
                    data[i][j+1][0] = 2 # West
    return data

# this is where the fire is toggled off and the lightning is changed to fire.
# the lightning iterations is managed here as well
def toggle_fire_and_lightning(data,fire_loc):
    for (i,j) in fire_loc:
        if data[i][j][1] == 0 and data[i][j][0] == 2:
            data[i][j][0] = 0
        if data[i][j] == [4,2]: # this will change the lightning color to fire's color
            data[i][j] = [2,2]
        if data[i][j][1] > 0: # this is for lighting which lasts 3 iterations
            data[i][j][1] -= 1



def fire_alg(map,spread_const): # this is just putting the 3 fire functions together
    fire_loc = find_fire(map)
    new_map = fire_logic(map,fire_loc,spread_const)
    toggle_fire_and_lightning(new_map,fire_loc)
    return new_map




