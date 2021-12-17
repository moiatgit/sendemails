#! /usr/bin/env python3

# This script checks the emails folder and sumarices what it finds

import sys
import pathlib
import datetime
from collections import namedtuple
import config

EmailSpecs = namedtuple('EmailSpecs', ['to', 'subject', 'attachment', 'text'])


def get_email_file_contents(path):
    """ given a path to a file it returns the tuple:

        (result_ok, contents)

        Where 

        result_ok is True when the file contained the expected format, False otherwise
        contents is a string describing the reason the format is wrong, when not result_ok
        contents is a EmailSpecs when result_ok
    """
    contents = path.read_text().split('\n')
    if len(contents) < 3:
        return (False, 'wrong format')

    line_to = contents[0].strip()
    if not line_to.startswith('to: '):
        return (False, 'First line should define the "to" argument')
    line_subject = contents[1].strip()
    if not line_subject.startswith('subject: '):
        return (False, 'Second line should define the "subject" argument')
    to = line_to[len('to: '):]
    subject = line_subject[len('subject: '):]
    if contents[2].strip().startswith('attach: '):
        attachment = pathlib.Path(contents[2].strip()[len('attach: '):])
        if not attachment.is_file():
            return (False, f'Attachment file not found {attachment}')
        if not attachment.suffix == '.pdf':
            return (False, f'Currently unsupported attachment type: {attachment}')
        text = '\n'.join(contents[3:])
    else:
        attachment = None
        text = '\n'.join(contents[2:])

    return (True, EmailSpecs(to, subject, attachment, text))


def unsent_emails():
    """ It returns a list of EmailSpecs for the emails found
        Renames all the files so they get the postfix «current_date».sent
    """
    # XXX It shouldn't rename these files until they're actually sent
    result = []
    path = pathlib.Path(config.email_folder)
    if not path.is_dir():
        return result
    for entry in list(path.glob('*.txt')):
        result_ok, specs = get_email_file_contents(entry)
        if result_ok:
            result.append(specs)
            entry.rename(entry.parent / pathlib.Path('%s.%s.sent' % (entry.name,
                                                                     datetime.date.today())))
    return result


if __name__ == '__main__':

    path = pathlib.Path(config.email_folder)

    if not path.is_dir():
        print("Email container not found: %s" % path)
        sys.exit(1)

    print("Email container: %s" % path)

    # already sent files
    already_sent = list(path.glob('*.sent'))
    print("Files already sent: %s" % len(already_sent))

    # to be sent files
    to_be_sent = list(path.glob('*.txt'))
    print("Files to be sent: %s" % len(to_be_sent))

    destinations = []
    for entry in to_be_sent:
        result_ok, specs = get_email_file_contents(entry)
        if result_ok:
            destinations.append(specs.to)

        if result_ok:
            print(f'File: {entry.name}: {specs.to} -> {specs.subject} {"" if specs.attachment is None else "(att)"}')
        else:
            print(f'File: {entry.name}: error {specs}')

    # summing up emails to be send
    if len(destinations) < 1:
        print("There are no emails to be sent")
    else:
        print("There are %s email/s to be sent" % len(destinations))

