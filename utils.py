__all__ = ["check_diff", 'get_curtime', 'filter', 'conver2ascii']

from datetime import datetime


def check_diff(cur_ids, new_ids):
    '''
    Check if there is changes in the mailbox.
    This only check for removing mails. So, when the length of cur_ids and new_ids are equal to each other, return False.
    :param cur_ids: Current Mids
    :param new_ids: Updated Mids
    :return: False or index of removed id.
    '''
    if len(cur_ids) == len(new_ids):
        return False, -1

    for i in range(len(new_ids)):
        if cur_ids[i] != new_ids[i]:
            return True, i


def get_curtime():
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    return current_time


def filter(body):
    body = body.split("\r\n")
    new_body = list()
    filters = ['https://', 'mailto:']
    for content in body:
        for f in filters:
            if f in content:
                break
        else:
            new_body.append(content)

    return ''.join(new_body)


def conver2ascii(body):
    return [ord(c) for c in body]
