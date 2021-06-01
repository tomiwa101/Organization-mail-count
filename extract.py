import sqlite3

conn = sqlite3.connect("mboxdb.sqlite")
cur = conn.cursor()

# Delete existing table and Create fresh one
cur.execute("DROP TABLE IF EXISTS Counts")
cur.execute("""CREATE TABLE "Counts" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    "org" TEXT UNIQUE,
    "count" INTEGER)""")

fileName = "mbox.txt"
count = 0 
fhand = open(fileName)
for line in fhand :
    # Extract organization and store in variable
    if not line.startswith("From: ") : continue
    line = line.rstrip()
    atPosition = line.find("@")
    dotPosition = line.find(".", atPosition)
    org = line[atPosition+1:dotPosition]
    
    # Add or Update Info to Database 
    cur.execute("SELECT count FROM Counts WHERE org = ? ", (org, ))
    row = cur.fetchone()
    if row is None :
        cur.execute(" INSERT INTO Counts (org, count) VALUES ( ?, 1) ", (org, ))
    else :
        cur.execute(" UPDATE Counts SET count = count + 1 WHERE org = ? ", (org, ))

    # run commit after every 50 loops
    count = count + 1
    check = count%50
    if check == 0 :
        conn.commit()
    
conn.commit()

# Get the organization with highest count from database
strquery = "SELECT org, count FROM Counts ORDER BY count DESC LIMIT 1"
cur.execute(strquery)
highest = cur.fetchone()
print(*highest, sep = " ")


