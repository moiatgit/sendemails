##########
sendemails
##########

This project is aimed to develop a simple command line emailing utility
that uses a gmail account to send multiple emails.

It has been tested with Python 3.7+ under GNU/Linux.

Make sure you read the 

License
=======

So you think you could take any profit from this code and won't blame me
if anything (ANYTHING) goes wrong from it? Well, in that case, you can use
it as long as you acknowledge that:

1. The scripts included in this project are, by now, under construction.

2. They are not intended to be used directly without deep knowledge of its
   internals. Therefore if you plan to use it, you are aware that it is
   absolutely by your own risk. 

3. You can do whatever you want with the code of these scripts 
   under the terms of the GNU General Public License 
   as published by the Free Software Foundation,
   either version 3 of the License, or any later version (your choice)

Usage
=====

Please, install all the dependencies in `requirements.txt`.


To give you an idea of how to use these scripts, consider the following
cml interaction: ::

    $ cat ~/.config/sendemails/sendemails.yaml   # configuration file
    # Configuration for the sendemail app

    # Client secrets: this is the file downloaded from google that contains keys to get credentials
    client_secret_path: 'path/to/gmail/credentials.json'


    # The token file stores the user's access and refresh tokens, and is created
    # automatically when the authorization flow completes for the first time.
    token_path: 'path/to/gmail.token.json'


    # When changin the scopes, remember to remove the token file so it can be regenerated
    # Check scopes at: https://developers.google.com/gmail/api/auth/scopes
    scopes: 'https://www.googleapis.com/auth/gmail.send'


    # Folder containing the files with the email specs to be sent
    email_folder: './emails'


    # Sender of the messages
    sender: 'youremailaddress@example.org'


    # time in seconds to wait from one email to the next (so gmail does not
    # get too busy)
    time_sleep_seconds: 1

    $ ls emails     # folder with the email specs
    email1.txt
    email2.txt
    email3.txt,2021-12-11.sent
    $ cat email.txt
    to: destination.email@example.org
    subject: This is the email subject
    attach: path/to/attached/file.pdf
    <p>This is the text of the message</p>
    <p>It can be multiple lines length since it will be counted up to the end.</p>
    <p>And it can contain virtually any html</p>
    $ python3 checkemails.py    # allows cheking the pending emails
    Email container: /home/user/sendemails/emails
    Files already sent: 1
    Files to be sent: 2
    $ python3 sendemails.py
    email1.txt: email sent to someuser@gmail.com
    email2.txt: email sent to anotheruser@gmail.com
    $ ls emailfolder
    email1.txt,2021-12-12.sent
    email2.txt.2021-12-12.sent
    email3.txt,2021-12-11.sent

It includes an email generator `generate_email_specs.py` that is aimed to
compose email specs from a template and a csv file. This script is
currently not maintained (it probably won't even run!) but it is left here
as reference.

To set it up, configure the file config.py with the path to the gmail
credentials.

Current limitations and contribution opportunities
==================================================

Some of the current limitations are:

* it allows to attach just one file and it must be pdf

  Actually, sendemails.py is prepared to send files of different types but
  it has not been tested yet. checkemails.py should be reviewed to allow
  more types to go.

* it renames email specs before knowing they've actually been sent. When
  an error occurs, this makes difficult to know which emails have been
  sent and which not.

* it requires improvement on sendemails feedback about the actually sent
  emails. Sometimes it is possible that an email is not sent but it is
  difficult to tell from the current output

* it requires more than 0 items in the following output: ::

    $ pytest
    platform linux -- Python 3.7.3, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
    rootdir: /home/user/dev/sendemails
    collected 0 items

* `config.py` specifically, but also the rest of the scripts, require
  improvements in the error messages. Currently a direct `assert` is used.

* it requires important review to allow non-devs to use it safely

* it requires major rewriting of this "documentation" including
  clearer instructions on how to set it up. It is specially necessary to
  ease/clarify the gmail credentials and token obtention for non-devs.

* `generate_email_specs.py` could get back to maintenance and get
  improvements as those listed in its header.

Feel free to contribute with these or any other feature/limitation. Just
fork this project, do your improvements and pull-request me. You can't
imagine how happy I'll be with that ;)
