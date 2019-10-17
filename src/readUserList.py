import exceptions
import re

def readUserList(file):
    userList = getList(file)
    sanitized = list( map(sanitizeUsername, userList) )
    return filterInvalidUsernames(sanitized)

def getList(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        raise exceptions.FileOpenErrorException( str(e) )

def sanitizeUsername(username):
    sanitized = username.strip()
    if sanitized.startswith('@'):
        sanitized = sanitized[1:]

    return sanitized

def filterInvalidUsernames(usernames):
    return [username for username in usernames if re.match(r'^[A-Za-z0-9_]+$', username)]