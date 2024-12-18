from tinydb import TinyDB, Query

db = TinyDB('users.json')

User = Query()

# functions to use the database


def create_user(username, bot):
    if not user_exists(username):
        # initial data
        db.insert({
            'username': username,
            'bot': bot,
            'matches_played': 0,
            'matches_won': 0,
            'matches_lost': 0,
            'points_played': 0,
            'points_won': 0,
            'points_lost': 0,
            'hits': 0,
        })
        return True
    return False


def user_exists(username):
    if len(db.search(User.username == username)) == 0:
        return False
    else:
        return True


def update_user(username, data):
    db.update(data, User.username == username)


def get_user_data(username, data=None):
    user = db.search(User.username == username)[0]
    if data is None:
        return user
    if isinstance(data, str):
        return user[data]
    return {d: user[d] for d in data}


def all_users():
    return db.all()


def remove_user(username):
    db.remove(User.username == username)
