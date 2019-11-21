

def calculate_percentage_burned(data):
    num_trees = 0
    for row in data:
        for entry in row:
            if entry[0] == 1:
                num_trees += 1
    percentage = ((num_trees / ((len(data)**2)))*100)
    return percentage