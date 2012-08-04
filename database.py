from pymongo import Connection

def db_method(target):
    def wrapper(*args, **kwargs):
        connection = Connection()
        db = connection.rsvp
        try:
            return target(*args, db = db, **kwargs)
        finally:
            del connection
    return wrapper
