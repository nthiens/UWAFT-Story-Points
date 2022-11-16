########################################################################################################
########################################################################################################

## Make sure to select "Columns", then tick off Story Points. Then export to Excel CSV (my defaults)
## Go to command line and enter "pip install matplotlib" 

## Change test.csv into the file you are using
file_name = "test2.csv"

## Set x to "1" to see story points 
## Set x to "2" to see number of tasks completed. Only tasks with
##      priority "Lowest", "Low", "Medium", "High", and "Highest"
##      will be shown
## Set x to "3" to see the burndown rate
x = 3

## Add names to this list to exclude them from metrics
remove_people = ["Sachin Fernando", "Nathee Thiensirisak"]

## If the assignee on Jira is in the title, put the assignee(s) inside angle brackets <>
## If angle brackets exist in the title AND there is an assignee, the assignee will take precedence

## For one assignee
## ex: <Ben Clayton> Determine Distubances

## For more than one assignee
## ex2: <Ben C. & Alex J.> Tool Sim Selection
## ex3: <Alex/Sam> Install CARLA

########################################################################################################
########################################################################################################

import csv
import numpy as np
import matplotlib.pyplot as plt

def extract_name(title):
    ext_name = ""
    counter = 0
    while title[counter] != ">":
        ext_name = ext_name + title[counter]
        counter = counter + 1
    counter = 0
    return (ext_name[1:])

def remove_from_list(remove, lis):
    lis_new = lis.copy()

    for a in remove:
        for b in lis_new:
            if (b[0] == a):
                lis_new.remove(b)
            #print(lis_new)

    return lis_new

people = []

with open(file_name) as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        title = row[3]
        assignee = row[4]
        
        if (title[0] == "<") and (assignee == ""):
            row[4] = extract_name(row[3])
            people = people + [row[4]]
        else:
            people = people + [assignee]
        #print(people)



new_people = list(set(people))
new_people2 = []

for people2 in new_people:
    if (people2 != "") and (people2 != "Assignee"):
        new_people2 = new_people2 + [[people2 ,0,0,0,0,0]]
        

#print(new_people2)

def update_info(name, pri, sp):
    ## print(f"Done by {name} with priority {pri} and {sp} story points!")
    for each_person in new_people2:
        if each_person[0] == name:
            each_person[1] = each_person[1] + sp
            each_person[5] = each_person[5] + sp
            if (pri == "Low") or (pri == "Lowest"):
                each_person[2] = each_person[2] + 1
            if (pri == "Medium"):
                each_person[3] = each_person[3] + 1
            if (pri == "High") or (pri == "Highest"):
                each_person[4] = each_person[4] + 1
    return None

def update_total(nm, pr, st):
    for each_person in new_people2:
        if each_person[0] == nm:
            each_person[5] = each_person[5] + st

with open(file_name) as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        title = row[3]
        assignee = row[4]
        priority = row[8]
        resolution = row[10]
        story = row[15]
        i_type = row[0]

        #print(title[0])
        #print(assignee)

        if (title[0] == "<") and (assignee == ""):
            #print('hi')
            row[4] = extract_name(row[3])
            #print(row[4])

        #print(row)
        #print(resolution, row[4], i_type)

        i = row[4]
        #print(i)

        #print(new_people2)
        #print(resolution, assignee, i_type)

        if (resolution == "Done") and (i_type != "Issue Type"):
            update_info(i,priority,float(story)) 
            #print(i, "is awesome")
        elif (resolution == "Done") and (assignee != "") and (i_type != "Issue Type"):
            #print("did0")
            if story == "":
                #print("did 1")
                update_info(assignee,priority,0) 
            else:
                update_info(assignee,priority,float(story)) 
                #print("did2")
        if (resolution == "") and (assignee != "") and (i_type != "Issue Type"):
            if story == "":
                update_total(assignee,priority,0) 
                #print("did3")
            else:
                update_total(assignee,priority,float(story)) 
                #print("did4")

def sort_by_sp(lop):
    return lop[1]

new_people2.sort(key=sort_by_sp, reverse=True)


def burn_down(lop):
    for ppl in lop:
        if (ppl[5] == 0) or (ppl[5] == "0") or (ppl[5] == 0.0) or (ppl[5] == "0.0"):
            ppl[5] = 0
        else:
            ppl[5] = 100 * (ppl[1]/ppl[5])


burn_down(new_people2)
#print(new_people2)

new_people3 = remove_from_list(remove_people, new_people2)

## Datset
names = []
for name in new_people3:
    names = names + [name[0]]

story_points = []
for story in new_people3:
    story_points = story_points + [int(story[1])]

low_priority = []
for lp in new_people3:
    low_priority = low_priority + [int(lp[2])]

med_priority = []
for mp in new_people3:
    med_priority = med_priority + [int(mp[3])]

hi_priority = []
for hp in new_people3:
    hi_priority = hi_priority + [int(hp[4])]

total_sp = []
for tsp in new_people3:
    total_sp = total_sp + [int(tsp[5])]

#print(total_sp)

new_list = new_people3.copy()
#print(new_list)


def sorter(lop):
    return lop[5]

new_list.sort(key=sorter, reverse=True)

yourname = []
for yn in new_list:
    yourname = yourname + [yn[0]]

tester = []
for t in new_list:
    tester = tester + [t[5]]
#print(yourname)
#print(tester)

if x == 1:
    fig, ax = plt.subplots(figsize =(14, 8))
    ax.barh(names, story_points)
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    
    ax.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
            
    ax.invert_yaxis()
    
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
         str(round((i.get_width()), 2)),
         fontsize = 10, fontweight ='bold',
         color ='grey')
         
    plt.xlabel("Story Points")
    plt.ylabel("Story Points")
    plt.title("Sprint Statistics")
    plt.show()


if x == 2:
    x = names
    low_priority = np.array(low_priority)
    med_priority = np.array(med_priority)
    hi_priority = np.array(hi_priority)

    plt.xlabel("Tasks Completed")
    plt.ylabel("Assignee")
    plt.title("Task Priority Completion")

    plt.barh(x, low_priority, color="g")
    plt.barh(x, med_priority, left=low_priority, color="yellow")
    plt.barh(x, hi_priority, left=low_priority+med_priority, color="r")
    
    plt.legend(['Low Priority', 'Medium Priority', "High Priority"])
    

    plt.show()

if x == 3:
    fig, ax = plt.subplots(figsize =(14, 8))
    ax.barh(yourname, tester)
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    
    ax.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
            
    ax.invert_yaxis()
    
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
         str(round((i.get_width()), 2)),
         fontsize = 10, fontweight ='bold',
         color ='grey')
         
    plt.ylabel("Assignees")
    plt.xlabel("Percentage")
    plt.title('Burndown Rate')
    plt.show()

