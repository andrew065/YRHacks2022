from config import mongo_password

def get_database():
    from pymongo import MongoClient
    CONNECTION_STRING = f'mongodb+srv://yrhaccs:{mongo_password}@cluster0.4lzbj.mongodb.net/myFirstDatabase'
    client = MongoClient(CONNECTION_STRING)
    return client['discordcalendar']
