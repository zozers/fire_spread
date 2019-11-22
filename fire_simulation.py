import os
import shutil
from PIL import Image
import imageio  #to install see http://imageio.readthedocs.io/en/latest/installation.html ( should be able to write
#{conda install -c conda-forge imageio} in pycharm terminal to install)
import webbrowser
from percentage_not_burned_module import calculate_percentage_burned
from fire_logic_module import starting_map, start_fire, fire_alg,find_fire
destination = "fire/"


#Note this program deletes the dir fire and the gif from the current directory
# so there are not image conflicts. If you want to save them, move them to a different location
# before running again


#things I need to add and look at

#fire spread
#fire burn for how long
#density
#how many adjacent fires needed to spread

#fuel reduction strategys in california

#wind

#graph the number of patches as a function of the area




if os.path.exists(destination):
    shutil.rmtree(destination)
if os.path.exists(destination+"/fire_spread.gif"):
    shutil.rmtree(destination+"/fire_spread.gif")

try:
    os.mkdir(destination)
except FileExistsError:
    pass

# This is where the user inputs the grid size fire spread probability and lightning probability.
n = 400

spread_const = 50


# This function takes the array or [1] (tree), [0](burnt tree), [2](fire), and [4](lightning) and replaces
#  those values with their respective color codes.

def grid_to_color(data,n):
    color_grid = []
    for i in range(n):
        temp = []
        for j in range(n):
            if data[i][j][0] == 1:
                temp.append((0, 204, 0))
            elif data[i][j][0] == 2:
                temp.append((254, 73, 2))
            elif data[i][j][0] == 0:
                temp.append(( 0, 0, 0))
            elif data[i][j][0] == 4:
                temp.append((255,255,0))
            elif data[i][j][0]==["ranger"]:
                temp.append((115,198,250))
        color_grid.append(temp)
    return color_grid


# this function creates an png of the array. I found a stack overflow post that really helped with this becasue I am not
# entirely sure how PIL works.
def graph_array(grid_in_color, n, count):
    name = count
    im = Image.new(mode='RGB', size=(n, n))
    im.putdata([x for row in grid_in_color for x in row])
    im = im.resize((500,500))
    im.save(destination+name+".png", 'png',)


# this is just producing the first two images where there is no fire and one block of fire.
start_map = starting_map(n)
color_grid = grid_to_color(start_map, n)
graph_array(color_grid, n, "00")# makes png
map = start_fire(start_map)
color_grid1 = grid_to_color(map, n)
graph_array(color_grid1, n, "01") #makes png
iterations = 2
iteration_str = "02"

print("running simulation...")

while len(find_fire(map)) > 0:
    data = fire_alg(map,spread_const)
    color_grid = grid_to_color(data, n)
    graph_array(color_grid, n, iteration_str)
    iterations += 1
    if iterations < 10:
        iteration_str = "0"+str(iterations) # for file sorting
    elif iterations >99:
        iteration_str = "z"+str(iterations) # for file sorting
    else:
        iteration_str = str(iterations)


file_names = sorted((fn for fn in os.listdir(destination) if fn.endswith('.png'))) # sorting png's to be in order based on given name

# This is where the gif of the png's is made using the library imagio
images = []
for filename in file_names:
    images.append(imageio.imread(destination+filename))
imageio.mimsave("fire_spread.gif", images)

# Here is where it is automatically opened
dir_path = ('file://'+os.getcwd())
url=(dir_path)+"/fire_spread.gif"
webbrowser.open(url,new=0,autoraise=True)

# Here is where the percentage of the forest burned is calculated using the percentage_not_burned module.
print("\n"+"There is " +str(calculate_percentage_burned(map))+ " percent of the forest left.")







