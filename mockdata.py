from database import client
import csv


with open('/Users/niravadunuthula/Downloads/fake_data2.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == "User ID": 
            continue
        data = {
            u'uuid': row[0],
            u'name': row[1] + " " + row[2],
            u'improvement': row[3],
            u'averageTime': row[4],
            u'age': row[5],
            u'height': row[6],
            u'weight': row[7],
            u'distpweek': row[8],
        }

        client.collection('users').document(row[0]).set(data)

