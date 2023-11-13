# Genetic Algorithms by Max DeJesus

from random import choice, seed, choices, random
from scipy.special import softmax
from numpy import average

# All data associated with our problem case
# Tuple of all faculty
faculty = ('Lock', 'Glen', 'Banks', 'Richards', 'Shaw', 'Singer', 'Uther', 'Tyler', 'Numen', 'Zeldin')

# Room and capacity, one-to-one (index i will return respective room number and capacity)
# Rooms dict: key of room name, value of capacity
rooms_no = ('Slater 003', 'Roman 216', 'Loft 206', 'Roman 201', 'Loft 310', 'Beach 201', 'Beach 301', 'Logos 325', 'Frank 119')
rooms_cap = (45, 30, 75, 50, 108, 60, 75, 450, 60)
rooms = {rooms_no[i]: rooms_cap[i] for i in range(len(rooms_no))}

# Possible time slots
timeslots = ('10a', '11a', '12p', '1p', '2p', '3p')

# Activites in a dict struct, with name as key and value of list 
# with values [Expected enrollment, Preferred faculty, other faculty]
acts = ['SLA100A','SLA100B','SLA191A','SLA191B','SLA201','SLA291','SLA303','SLA304','SLA394','SLA449','SLA451']

activities = {
    'SLA100A' : [50, ('Glen', 'Lock', 'Banks', 'Zeldin'), ('Numen', 'Richards')],
    'SLA100B' : [50, ('Glen', 'Lock', 'Banks', 'Zeldin'), ('Numen', 'Richards')],
    'SLA191A' : [50, ('Glen', 'Lock', 'Banks', 'Zeldin'), ('Numen', 'Richards')],
    'SLA191B' : [50, ('Glen', 'Lock', 'Banks', 'Zeldin'), ('Numen', 'Richards')],
    'SLA201': [50, ('Glen', 'Banks', 'Zeldin', 'Shaw'), ('Numen', 'Richards', 'Singer')],
    'SLA291' : [50, ('Lock', 'Banks', 'Zeldin', 'Singer'), ('Numen', 'Richards', 'Shaw', 'Tyler')],
    'SLA303' : [60, ('Glen', 'Zeldin', 'Banks'), ('Numen', 'Singer', 'Shaw')],
    'SLA304' : [25, ('Glen', 'Banks', 'Tyler'), ('Numen', 'Singer', 'Shaw', 'Richards', 'Uther', 'Zeldin')],
    'SLA394' : [20, ('Tyler', 'Singer'), ('Richards', 'Zeldin')],
    'SLA449' : [60, ('Tyler', 'Singer', 'Shaw'), ('Zeldin', 'Uther')],
    'SLA451' : [100, ('Tyler', 'Singer', 'Shaw'), ('Zeldin', 'Uther', 'Richards', 'Banks')]
}

# Gen count
gen_count = 0

# Want to set up schedule to be a dict, keyed with an activity, 
# and has values of list: [Room, Time, Faculty]

# Functions

# Finds next key for activities dict
# Input: key: str
# Output: next_key: str or False
def next_key(key):
    if key in acts:
        key_index = acts.index(key)
        if key_index < len(acts) - 1:
            return acts[key_index + 1]
    return False

# Fitness function, holds all conditionals for evaluating well-performing schedules
# Input: schedule: dict
# Returns: fitness: flaot
def calculate_fitness(schedule):
    fitness = 0.0
    
    # Base loop: evaluates a basic score based on simple factors
    for act, info in schedule.items():
        room = info[0]
        fac = info[2]
        tmp_fit = 0.0

        # begin base conditionals
        # Check if preferred or other faculty
        if fac in activities[act][1]:
            tmp_fit += 0.5
        elif fac in activities[act][2]:
            tmp_fit += 0.2
        else:
            tmp_fit -= 0.1
            
        # Check room size
        if rooms[room] < activities[act][0]:
            tmp_fit -= 0.5
        elif rooms[room] > 3 * activities[act][0]:
            tmp_fit -= 0.2
        elif rooms[room] > 6 * activities[act][0]:
            tmp_fit -= 0.4
        else:
            tmp_fit += 0.3
        
        # Add base score to total score
        fitness += tmp_fit
    
    # Overlap loop: checks item i against j, with j traversing list backwards until reaching i
    for act1, info1 in schedule.items():
        tmp_fit = 0.00
        act2 = act1
        while True:
            act2 = next_key(act2)
            # Break case
            if not act2:
                break    
            info2 = schedule[act2]
            
            # Same room, same time
            if info2[0] == info1[0] and info2[1] == info1[1]:
                tmp_fit -= 0.50
            
            # Same facilitator, same time, different room
            if info2[2] == info1[2] and info2[1] == info1[1] and info2[0] != info1[0]:
                tmp_fit -= 0.20
            else: 
                tmp_fit += 0.20
            
            # Section-related overlaps
            if act1 == 'SLA100A':
                # Same time as another section
                if schedule['SLA100B'][1] == info1[1]:
                    tmp_fit -= 0.50
                    
                # Four hours apart from other section
                elif (schedule['SLA100B'][1] == '10a' and info1[1] == '2p') or (schedule['SLA100B'][1] == '10a' and info1[1] == '3p'):
                    tmp_fit += 0.50
                elif schedule['SLA100B'][1] == '11a' and info1[1] == '3p':
                    tmp_fit += 0.50
            if act1 == 'SLA191A':
                # Same time as another section
                if schedule['SLA191B'][1] == info1[1]:
                    tmp_fit -= 0.50
                    
                # Four hours apart from other section
                elif (schedule['SLA191B'][1] == '10a' and info1[1] == '2p') or (schedule['SLA191B'][1] == '10a' and info1[1] == '3p'):
                    tmp_fit += 0.50
                elif schedule['SLA191B'][1] == '11a' and info1[1] == '3p':
                    tmp_fit += 0.50
                    
            # Activity 100 and 191 overlap/concurrency
            if act1 == 'SLA100A' or act1 == 'SLA100B':
                # Activity 191 overlaps with 100 (only need to check here)
                if (timeslots.index(info1[1]) ==  timeslots.index(schedule['SLA191A'][1])) or (timeslots.index(info1[1]) ==  timeslots.index(schedule['SLA191B'][1])):
                    tmp_fit -= 0.25
                    
                # Activitty 191 directly follows a 100 section
                elif (abs(timeslots.index(info1[1]) - timeslots.index(schedule['SLA191A'][1])) == 1):
                    if info1[0].split()[0] == 'Roman' or info1[0].split()[0] == 'Beach':
                        if schedule['SLA191A'][0].split()[0] != 'Roman' or schedule['SLA191A'][0].split()[0] != 'Beach':
                            # If same professor, deduct more points
                            if schedule['SLA191A'][2] == info1[2]:
                                tmp_fit -= 0.9
                            tmp_fit -= 0.9
                    else:
                        if schedule['SLA191A'][2] == info1[2]:
                            tmp_fit += 0.5
                        tmp_fit += 0.5
                elif (abs(timeslots.index(info1[1]) -  timeslots.index(schedule['SLA191B'][1])) == 1):
                    if info1[0].split()[0] == 'Roman' or info1[0].split()[0] == 'Beach':
                        if schedule['SLA191B'][0].split()[0] != 'Roman' or schedule['SLA191B'][0].split()[0] != 'Beach':
                            # If same professor, deduct more points
                            if schedule['SLA191B'][2] == info1[2]:
                                tmp_fit -= 0.9
                            tmp_fit -= 0.9
                    else:
                        if schedule['SLA191B'][2] == info1[2]:
                            tmp_fit += 0.5
                        tmp_fit += 0.5
                        
                # Activity 191 is one hour after a 100 section
                elif(abs(timeslots.index(info1[1]) - timeslots.index(schedule['SLA191A'][1])) == 2) or (abs(timeslots.index(info1[1]) -  timeslots.index(schedule['SLA191B'][1])) == 2):
                    tmp_fit += 0.25
            if act1 == 'SLA191A' or act1 == 'SLA191B':
                    # Activitty 100 directly follows a 191 section
                    if (abs(timeslots.index(info1[1]) - timeslots.index(schedule['SLA100A'][1])) == 1):
                        if info1[0].split()[0] == 'Roman' or info1[0].split()[0] == 'Beach':
                            if schedule['SLA100A'][0].split()[0] != 'Roman' or schedule['SLA100A'][0].split()[0] != 'Beach':
                                # If same professor, deduct more points
                                if schedule['SLA100A'][2] == info1[2]:
                                    tmp_fit -= 0.9
                                tmp_fit -= 0.9
                        else:
                            if schedule['SLA100A'][2] == info1[2]:
                                tmp_fit += 0.5
                            tmp_fit += 0.5
                    elif (abs(timeslots.index(info1[1]) -  timeslots.index(schedule['SLA100B'][1])) == 1):
                        if info1[0].split()[0] == 'Roman' or info1[0].split()[0] == 'Beach':
                            if schedule['SLA100B'][0].split()[0] != 'Roman' or schedule['SLA100B'][0].split()[0] != 'Beach':
                                # If same professor, deduct more points
                                if schedule['SLA100B'][2] == info1[2]:
                                    tmp_fit -= 0.9
                                tmp_fit -= 0.9
                        else:
                            if schedule['SLA100B'][2] == info1[2]:
                                tmp_fit += 0.5
                            tmp_fit += 0.5
                            
                    # Activity 100 is one hour after a 191 section
                    elif (abs(timeslots.index(info1[1]) - timeslots.index(schedule['SLA100A'][1])) == 2) or (abs(timeslots.index(info1[1]) -  timeslots.index(schedule['SLA100B'][1])) == 2):
                        tmp_fit += 0.25

        # Add overlap score to total score
        fitness += tmp_fit
            
    # Facilitator loop: evaluates score based on faculty-specifif criteria
    for fac in faculty:
        tmp_fit = 0.0
        count = 0
        for info in schedule.values():
            if info[2] == fac:
                count += 1
        # Special case: Tyler has < 2 activities
        if fac == 'Tyler':
            if count >= 2:
                tmp_fit -= 0.4
            else:
                pass
        else:
            if count < 3:
                tmp_fit -= 0.4
            elif count > 4:
                tmp_fit -= 0.5
            else:
                pass
        
        # Add facilitator score to total score
        fitness += tmp_fit       
            
    # Return fitness to closest hundreth
    return round(fitness, 2)

# Generate function: produces offspring with two parents using uniform crossover and mutation
# Input: parent1: dict, parent2: dict
# Returns: current_schedule: list[dict, float]
def generate(parent1, parent2):
    rng = None
    master = {}
    for activity in activities.keys():
            activity_sheet = {
                activity : []
            }
            
            # Loop for each trait in parents, randomly decide which parent passes trait/mutation
            for i in range(3):
                rng = random()
                c = 0
                flag = False
                
                # Mutation flag
                if rng < (0.01 / 2):
                    flag = True
                
                rng = random()
                # Parent trait flag
                if rng >= 0.5:
                    c = 1
                else:
                    c = 2

                # Case statement for which trait its on
                match i:
                    case 0:
                        if flag:
                            room = choice(rooms_no)
                        else:
                            if c == 1:
                                room = parent1[activity][i]
                            else:
                                room = parent2[activity][i]
                    case 1:
                        if flag:
                            time = choice(timeslots)
                        else:
                            if c == 1:
                                time = parent1[activity][i]
                            else:
                                time = parent2[activity][i]
                    case 2:
                        if flag:
                            fac = choice(faculty)
                        else:
                            if c == 1:
                                fac = parent1[activity][i]
                            else:
                                fac = parent2[activity][i]
                
            data = [room, time, fac]
            activity_sheet[activity] = data
            master.update(activity_sheet)
            
    score = calculate_fitness(master)
    return [master, score]


# Main

if __name__ == '__main__':
    # Instantiate vars
    gen_100_avg = None
    improvement = 100
    gens = []
    current_gen = []
    
    # Create the generation zero (pure randomization)
    for i in range(500):
        current_schedule = {}
        
        for activity in activities.keys():
            activity_sheet = {
                activity : []
            }
            
            room = choice(rooms_no)
            time = choice(timeslots)
            fac = choice(faculty)
            
            data = [room, time, fac]
            activity_sheet[activity] = data
            
            current_schedule.update(activity_sheet)
        
        score = calculate_fitness(current_schedule)
        current_gen.append([current_schedule, score])
    print('Gen 0 created.')
    gens.append(current_gen)
    
    # Main while loop: runs until criteria is met.
    # One full cycle indicates a complete generation.
    while True:
        if improvement >= 0.5:
            pass
        elif improvement < 0:
            pass
        else:
            break
        
        # Step one: split gen list into two for normalization
        current_fit = []
        current_acts = []
        for item in current_gen:
            current_acts.append(item[0])
            current_fit.append(item[1])
            
        # Step two: normalize and softmax fitness scores
        current_softmax = softmax(current_fit)
        
        # Step three: gather two parents and generate offspring
        current_gen = []
        for i in range(500):
            parent1, parent2 = choices(current_acts, weights=current_softmax, k=2)
            current_schedule = generate(parent1, parent2)
            current_gen.append(current_schedule)
        
        # Step four: closing arrangements
        gen_count += 1
        print(f'Gen {gen_count} created.')
        gens.append(current_gen)

        # Step five: calculate average improvement
        if gen_count == 100:
            gen_100_avg = average(current_fit)
        if gen_count > 100:
            avg = average(current_fit)
            improvement = ((avg - gen_100_avg) / gen_100_avg) * 100
            
    # Generative execution finished! Find a best schedule from latest generation
    print("Found! Locating a best schedule...")
    last_gen = gens[-1]
    elite = []
    max_fit = -1000
    for node in last_gen:
        if node[1] >= max_fit:
            if node[1] == max_fit:
                rng = random()
                if rng > 0.2:
                    elite = node
                    max_fit = node[1]
            else:
                elite = node
                max_fit = node[1]        
    elite_schedule = elite[0]
    elite_fitness = elite[1]
    
    # Output the elite schedule to a text file
    print('Creating schedule.txt with elite schedule...')
    out_file = open('schedule.txt', 'w+')
    with out_file:
        out_file.write('Optimized schedule found by genetic algorithm:\n')
        for activity, info1 in elite_schedule.items():
            out_file.write(f'{activity}: Room = {info1[0]}, Time = {info1[1]}, Facilitator = {info1[2]}\n')
        out_file.write(f'Total fitness: {elite_fitness}')    
    out_file.close()
    print('File created.')
        

    