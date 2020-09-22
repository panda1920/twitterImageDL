import re
import logging

import twitter_image_dl.exceptions as exceptions

logger = logging.getLogger(__name__)

def readUserList(filepath):
    logger.info('Loading userlist from file %s', str(filepath))

    usernames = [
        sanitizeUsername(username)
        for username in getList(filepath)
    ]
    return removeInvalidUsernames( removeDuplicates(usernames) )

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
    logger.info('Removing duplicate usernames')

    uniques = []
    for username in usernames:
        if username not in uniques:
            uniques.append(username)

    return uniques

def removeInvalidUsernames(usernames):
    logger.info('Removing invalid usernames')

    valid_pattern = r'^[A-Za-z0-9_]+$'
    return [
        username for username in usernames
        if re.match(valid_pattern, username)
    ]
