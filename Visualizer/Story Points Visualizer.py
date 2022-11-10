########################################################################################################
########################################################################################################

## Make sure to select "Columns", then tick off Story Points. Then export to Excel CSV (my defaults)
## Go to command line and enter "pip install matplotlib"

## Change test.csv into the file you are using
file_name = "test.csv"
## Set x to "1" to see story points or set x to "2" to see number of tasks completed
## or set x to "3" to see the burndown rate
x = 1

########################################################################################################
########################################################################################################


import csv
import numpy as np
import matplotlib.pyplot as plt

people = []

with open(file_name) as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        assignee = row[4]
        people = people + [assignee]


new_people = list(set(people))
new_people2 = []

for people2 in new_people:
    if (people2 != "") and (people2 != "Assignee"):
        new_people2 = new_people2 + [[people2 ,0,0,0,0,0]]
        

## print(new_people2)

def update_info(name, pri, sp):
    ## print(f"Done by {name} with priority {pri} and {sp} story points!")
    for each_person in new_people2:
        if each_person[0] == name:
            each_person[1] = each_person[1] + sp
            each_person[5] = each_person[5] + sp
            if (pri == "Low"):
                each_person[2] = each_person[2] + 1
            if (pri == "Medium"):
                each_person[3] = each_person[3] + 1
            if (pri == "High"):
                each_person[4] = each_person[4] + 1
    return None

def update_total(nm, pr, st):
    for each_person in new_people2:
        if each_person[0] == nm:
            each_person[5] = each_person[5] + st

with open(file_name) as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        assignee = row[4]
        priority = row[8]
        resolution = row[10]
        story = row[15]
        i_type = row[0]
        if (resolution == "Done") and (assignee != "") and (i_type != "Issue Type"):
            if story == "":
                update_info(assignee,priority,0) 
            else:
                update_info(assignee,priority,float(story)) 
        if (resolution == "") and (assignee != "") and (i_type != "Issue Type"):
            if story == "":
                update_total(assignee,priority,0) 
            else:
                update_total(assignee,priority,float(story)) 

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


## Datset
names = []
for name in new_people2:
    names = names + [name[0]]

story_points = []
for story in new_people2:
    story_points = story_points + [int(story[1])]

low_priority = []
for lp in new_people2:
    low_priority = low_priority + [int(lp[2])]

med_priority = []
for mp in new_people2:
    med_priority = med_priority + [int(mp[3])]

hi_priority = []
for hp in new_people2:
    hi_priority = hi_priority + [int(hp[4])]

total_sp = []
for tsp in new_people2:
    total_sp = total_sp + [int(tsp[5])]

#print(total_sp)

new_list = new_people2.copy()
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
    N = len(new_people2)
    ind = np.arange(N)
    width = 0.25
    
    bar1 = plt.bar(ind, low_priority, width, color = 'g')
    bar2 = plt.bar(ind+width, med_priority, width, color='y')
    bar3 = plt.bar(ind+width*2, hi_priority, width, color = 'r')

    plt.xlabel("Assignees")
    plt.ylabel('Tasks Completed')
    plt.title("Task Priorities")

    plt.xticks(ind+width, names)
    plt.xticks(rotation=20)
    plt.legend( (bar1, bar2, bar3), ('Low Priority', 'Medium Priority', 'High Priority') )
    plt.show()

if x == 3:
    plt.figure(figsize=(12,8))
    colors_list = ["Red"]
    graph = plt.bar(yourname, tester, color = colors_list)
    plt.title('Burndown Rate')
    plt.xlabel("Assignees")
    plt.ylabel('Percentage')
    plt.xticks(rotation=20)
    for x,y in zip(yourname, tester):

        label = "{:.2f}".format(y)

        plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha="center")
    plt.show()
