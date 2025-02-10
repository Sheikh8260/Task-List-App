from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.tasklist

class User:
    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

class TaskList:
    def __init__(self, name, description, user_email):
        self.name = name
        self.description = description
        self.user_email = user_email
        self.tasks = []

class Task:
    def __init__(self, title, description, due_date, priority, status, tags, subtasks):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.tags = tags
        self.subtasks = subtasks