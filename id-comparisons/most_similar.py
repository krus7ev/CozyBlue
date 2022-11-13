import csv

with open('id_similarities.csv', 'r') as file:
    items = []
    reader = csv.reader(file)
    for row in reader:
        items.append(row)
    items = [x for x in items if x[0] != x[1]]
    items.sort(key=lambda x: x[2])
    for item in items:
        if float(item[2]) > 0.7:
            print(item[0].rjust(30), item[1].rjust(30), f"{float(item[2])*100:.2f}%")
