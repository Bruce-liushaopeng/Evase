import sqlite3

def newUserToDB(firstName, lastName):
    conn = sqlite3.connect('sample.db')
    query = f"INSERT INTO USER ( FirstName, LastName) VALUES ('{firstName}', '{lastName}')"
    print(firstName)
    print(query)
    conn.execute(f"INSERT INTO USER ( FirstName, LastName) VALUES ('{firstName}', '{lastName}')")
    conn.commit()

    curser = conn.execute("SELECT FirstName, LastName from USER")
    updatedDB = []
    for row in curser:
        data = [row[0], row[1]]
        updatedDB.append(data)
        print("ID = ", row[0])
        print("FirstName = ", row[1])

    conn.close()
    return updatedDB

def getUserFromDB(firstName):
    conn = sqlite3.connect('sample.db')
    curser = conn.execute(f"SELECT FirstName, LastName from USER where firstName = '{firstName}'")
    userInfo = []
    for row in curser:
        data = [row[0], row[1]]
        userInfo.append(data)
        print("ID = ", row[0])
        print("FirstName = ", row[1])

    conn.close()
    return userInfo


if __name__ == '__main__':
    conn = sqlite3.connect('sample.db')
    userInput = f"123' or 'hello' = 'hello"
    curser = conn.execute(f"SELECT FirstName, LastName from USER where firstName = '{userInput}'")
    updatedDB = []
    for row in curser:
        data = [row[0], row[1]]
        updatedDB.append(data)
        print("ID = ", row[0])
        print("FirstName = ", row[1])

    conn.close()