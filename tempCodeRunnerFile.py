import pandas as pd
import pymongo
from pymongo import MongoClient
import json
import urllib.parse # if the username/password contain special characters , then password has to be URL encoded
import getpass  # Making use of getpass() prompts the user for a password without echoing for security purpose
import numpy as np 
username = getpass.getuser()
password=getpass.getpass(prompt="Enter password for Mongo Database")
print(pymongo.__version__)
def mongoimport( db_name, coll_name, db_url,df):
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    with MongoClient(db_url) as client:
        print(client)
        db = client[db_name]
        coll = db[coll_name]
        
        payload = json.loads(df.to_json(orient='records'))
        coll.delete_many({})  # Delete anything if exists in a collection
        coll.insert_many(payload)  # Insert the csv file 
        return coll.count_documents({})  # return the count of inserted items



csv_path="/Users/surbhi/Downloads/herokuapp/BikePedCrash.csv"   # path where csv file is saved
db_name="Bike_Crash_Datbase"                                    # name of the database
coll_name="Bike_Crash_Collection"                               # name of the collection
username = urllib.parse.quote_plus(username)                    # url encoding the username
password = urllib.parse.quote_plus(password)                    # url encoding the password

# loading of dataset
def loading_dataset(csv_path):
    df = pd.read_csv(csv_path)
    df=df.T.drop_duplicates() # we first transpose the data and then drop the dupliacte rows .Again transpose the data
    df=df.T
    # """Columns "BikeAgeGrp" had inconsistent values, so we are dropping that coulmn, and creating a new columns again "BikeAgeGrp" based on BikeAge columns using conditions"""
    df.drop(columns=["BikeAgeGrp"],inplace=True)
    print(df.columns)

    # Dividing the dataframe into two parts , based on age values

    filer_condition=df.loc[(df['BikeAge']=="Unknown")|(df['BikeAge']=="70+")].index
    df_filter=df.drop(filer_condition)
    df_filter['BikeAge']=df_filter['BikeAge'].astype('int')

    # create a list of our conditions
    conditions = [
        (df_filter['BikeAge']>= 0) & (df_filter['BikeAge'] <= 20),
        (df_filter['BikeAge']>= 21)& (df_filter['BikeAge'] <= 30),
        (df_filter['BikeAge'] >= 31) & (df_filter['BikeAge'] <= 40),
        (df_filter['BikeAge'] >= 41) & (df_filter['BikeAge'] <= 50),
        (df_filter['BikeAge'] >= 51) & (df_filter['BikeAge'] <= 60),
        (df_filter['BikeAge'] >= 61) & (df_filter['BikeAge'] <= 70),
        (df_filter['BikeAge'] > 70) & (df_filter['BikeAge'] !=999 ),
        (df_filter['BikeAge'] == 999)]

    # create a list of the values we want to assign for each condition
    values = ['0-20', '21-30', '31-40', '41-50','51-60','61-70','70+',"Unknown"]

    # create a new column and use np.select to assign values to it using our lists as arguments
    df_filter['BikeAgeGrp'] = np.select(conditions, values)
    filer_condition=df.loc[(df['BikeAge']=="Unknown")|(df['BikeAge']=="70+")].index
    df_another_filter=df.loc[filer_condition,:]

    print(df_another_filter.shape)
    # create a list of our conditions
    conditions = [
        (df_another_filter['BikeAge']=="Unknown") ,
        (df_another_filter['BikeAge']=="70+")]

    # create a list of the values we want to assign for each condition
    values = ["Unknown","70+"]

    # create a new column and use np.select to assign values to it using our lists as arguments
    df_another_filter['BikeAgeGrp'] = np.select(conditions, values)

    # display updated DataFrame
    # df_another_filter.tail()

    # concatenating the two dataframes to get a single dataframe
    df=pd.concat([df_another_filter,df_filter],axis=0)

    return df

# display updated DataFrame
# df_filter.head()


data=loading_dataset(csv_path)
# defining the connection string
db_url=f"mongodb+srv://{username}:{password}@sandbox.iq6qn.mongodb.net/{db_name}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
print(db_url)

# calling the function
inseretd_items=mongoimport(db_name, coll_name, db_url,data)
print(inseretd_items)