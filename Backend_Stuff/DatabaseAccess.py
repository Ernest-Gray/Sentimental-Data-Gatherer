import mysql.connector
import json
import datetime as dt

#Get json values
with open("./Backend Stuff/config.json", "r") as json_file:
    json_data = json.load(json_file)
    DBName = json_data["DBName"]
    DBPass = json_data["DBPass"]
    DBHost = json_data["DBHost"]
    DBUser = json_data["DBUser"]
    
# Connect to the database
cnx = mysql.connector.connect(user=DBUser,
                              password=DBPass,
                              host=DBHost,
                              database=DBName)


def InsertData(tableName:str, data:dict):
    
    if "DROP" in tableName or "DELETE" in tableName:
        print("Error: Drop or Delete detected in Insert Statement")
        return None
    
    try:
        # Create a cursor object
        cursor = cnx.cursor()
        
        #Get the columns
        cursor.execute("SHOW COLUMNS FROM " + str(tableName))
        columns = cursor.fetchall()
        
        cols = []
        for item in columns:
            if 'auto_increment' not in item:
                cols.append(item)
        columns = cols
        print(columns)

        query = "INSERT INTO " + str(tableName) + " ("
        for x in range(len(columns)-1):
            query += columns[x][0] + ", "
        query += columns[-1][0] + ")"
        
        query += " VALUES ("
        for x in range(len(columns)-1):
            query += "%(" + str(columns[x][0]) + ")s, "
        query += "%(" + str(str(columns[-1][0])) + ")s)"
        
        print("Query: " + str(query))
        # Execute a SQL query
        # cursor.execute(query, tuple(data.values()))
        cursor.execute(query, data)
        
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()
    except Exception as e:
        print("Error Occurured: the table columns are" + str(columns))
        print(e)
        return None

def GetData(tablename:str, where=""):
    
    if "DROP" in tablename or "DELETE" in tablename:
        print("Error: Drop or Delete detected in Insert Statement")
        return None
    
    cursor = cnx.cursor()
    
    query = "SELECT * FROM " + str(tablename) + " "
    
    if where != "":
        if "DROP" in where or "DELETE" in where:
            print("Error: Drop or Delete detected in Insert Statement")
            return None
        query += where
    
    print(query)
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    cursor.close()
    cnx.close()
    return results
        
#TESTING
# print(tuple({"Symbol" : "AAPL", "Company_Name" : "Apple"}.values()))
InsertData("Tickers", {"Company_Name" : "Microsoft", "Symbol" : "MSFT" })
# InsertData("Sentiment_Data", {"Value": 1, "Time": dt.datetime.now(), "Symbol": "AAPL"})

print(GetData("Sentiment_Data", where="WHERE Symbol='AAPL'"))