import re

import twitter_image_dl.exceptions as exceptions

def readUserList(filepath):
    usernames = [
        sanitizeUsername(username)
        for username in getList(filepath)
    ]
    usernames = removeDuplicates(usernames)
    return filterInvalidUsernames(usernames)

def getList(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        filepath.touch()
        return []

def sanitizeUsername(username):
    sanitized = username.strip()
    if sanitized.startswith('@'):
        sanitized = sanitized[1:]

    return sanitized

def removeDuplicates(usernames):
    uniques = []
    for username in usernames:
        if username not in uniques:
            uniques.append(username)

    return uniques

def filterInvalidUsernames(usernames):
    return [username for username in usernames if re.match(r'^[A-Za-z0-9_]+$', username)]
