def is_authenticated(self):
    return True

def is_active(self):
    return True

def is_anonymous(self):
    return False

def get_id(self):
    return self.username

def __repr__(self):
    return '<User {}>'.format(self.username)
