import imaplib
import email
from sounds import sound_mixer
from utils import *

IMAP_SERVER = "imap.gmail.com"

class cabon_sound:
    def __init__(self, args):
        self.args = args
        self.mail = self._get_email()  # initialize the current mail instance.
        self.cur_ids = self._get_Mid(self.mail)
        self.new_mail, self.new_ids = None, None
        self.sound_mixer = sound_mixer(args)

    def _get_email(self):
        '''
        Get mail instance
        :return: IMAP mail instance
        '''
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(self.args.account, self.args.password)
        mail.select(self.args.label_name)

        return mail

    def _get_Mid(self, mail):
        '''
        Get Message IDs
        :param mail: mail instance
        :return: Mids in list
        '''
        mail_ids = mail.search(None, 'ALL')[1][0]
        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        Mids = []
        for i in range(first_email_id, latest_email_id):
            typ, data = mail.fetch(str(i), '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
            msg_str = email.message_from_string(str(data[0][1], 'utf-8'))
            Mids.append(msg_str.get('Message-ID'))

        return Mids

    def run(self):
        while True:
            self.mail.noop()  # send noop to the server
            new_ids = self._get_Mid(self.mail)
            is_diff, idx = check_diff(self.cur_ids, new_ids)
            if is_diff:
                try:
                    print(f'  Found changes in the mailbox! ({get_curtime()})')
                    data = self.mail.fetch(str(idx), '(RFC822)')
                    for response_part in data:
                        arr = response_part[0]
                        if isinstance(arr, tuple):
                            msg = email.message_from_string(str(arr[1], 'utf-8'))
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload()
                                    body = filter(body)
                                    self.sound_mixer.run(body)
                except:
                    pass
                self.cur_ids = new_ids

            else:
                print(f'  No changes in the mailbox! ({get_curtime()})')
