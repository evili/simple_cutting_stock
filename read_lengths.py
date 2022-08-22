import csv

def get_data(infile:str):
    lablen = []
    with open(infile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar="'")
        for row in reader:
            lablen.append([row[0], float(row[1])])
    return lablen
