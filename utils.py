__all__ = ["check_diff", 'get_curtime', 'filter', 'conver2ascii']

from datetime import datetime
from argparse import ArgumentParser
import re

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

    filtered = ''.join(new_body)
    filtered = conver2ascii(filtered)
    filtered = ''.join([chr(i) for i in filtered if i==32 or 65<=i<=90 or 97<=i<=122])
    filtered = re.sub(" +", " ", filtered)

    return filtered.lower()


def conver2ascii(body):
    return [ord(c) for c in body]


def build_args(config):
    parser = ArgumentParser()

    parser.add_argument(
        '--account',
        type=str,
        default=config["account"]+"@gmail.com",
        help='Gmail account')

    parser.add_argument(
        '--password',
        type=str,
        default=config["password"],
        help='password')

    parser.add_argument(
        '--sound_interval',
        type=float,
        default=config["sound_interval"],
        help='sound_interval')

    parser.add_argument(
        '--total_duration',
        type=float,
        default=config["total_duration"],
        help='total_duration')


    parser.add_argument(
        '--label_name',
        type=str,
        default=config["label_name"],
        help='label_name')

    parser.add_argument(
        '--source_path',
        type=str,
        default=config["source_path"],
        help='source_path')

    parser.add_argument(
        '--save_path',
        type=str,
        default=config["save_path"],
        help='save_path')

    return parser.parse_args()