from google.cloud import firestore


def auth(username: str, password: str) -> bool:
    """Helper function to authenticate with database.

    :type username: str
    :param username: The requester's username.

    :type password: str
    :param password: The reqeuster's password.

    :ret type: User
    """
    db = firestore.Client()
    user_ref = db.collection(u"users").where("username", "==", username).stream()

    users = [user.to_dict() for user in user_ref]

    if len(users) > 1:
        return False

    if users[0]["password"] == password:
        return True
    else:
        return False
