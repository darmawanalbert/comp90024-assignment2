import csv
file2 = open('sinceID.csv', 'w')
writer = csv.writer(file2)
writer.writerow('abc')
file2.close()