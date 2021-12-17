#! /usr/bin/env python3
"""
  email specs generator. From the template in sys.argv[1] and the csv in
  sys.argv[2], it generates the files to be processed by sendmails.py

  TODO:

  - stop depending on pandas to read a simple csv
  - use ezodf to access odt directly
  - use jinja2 for templates instead of this custom replacement
"""

import sys
import re
import pathlib
import datetime
import csv
import config
import pandas as pd


def compose_email_spec(template, student_entry):
    """ Given a template and a Pandas Series containing the student results,
        this method replaces all the variables in the template by the corresponding values
        of the student """
    for key in set(re.findall('\{\{(.*?)\}\}', template)):
        template = template.replace('{{%s}}' % key, str(student_entry[key]))
    return template


def generate_email_specs(template, df):
    """ Given a template and a DataFrame containing the results of the students,
        this method composes and returns the text contents of the emails to be sent to the students.
        The returning values are listed as tuples (email, text) """
    results = []
    for index in df[df['email'].notna() & df['email'].str.contains('@')].index:
        entry = df.loc[index]
        results.append((entry['email'], compose_email_spec(template, entry)))
    return results


def save_email_specs(contents):
    """ given a list of tuples (email, text), it creates a file in the config.email_folder for each tuple,
        named as the email prefixed by current date and postfixed by .txt with the contents in text

        Expected contents format is the one returned by generate_email_specs()

        In case there's another email spec with this name, it breaks execution
    """
    root = pathlib.Path(config.email_folder)
    for email, text in contents:
        path = root / pathlib.Path('%s.%s.txt' % (datetime.date.today(), email))
        if path.is_file():
            print("Error: file already exists! %s" % path)
            sys.exit(1)
        path.write_text(text)
        print("Wrote file %s" % path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: %s path_to_template path_to_csv' % sys.argv[0])
        sys.exit(1)
    if not sys.argv[1].endswith('.template'):
        print('Template file extension must be .template')
        sys.exit(1)

    template_path = pathlib.Path(sys.argv[1])
    if not template_path.is_file():
        print('File not found %s' % sys.argv[1])
        sys.exit(1)

    if not sys.argv[2].endswith('.csv'):
        print('CSV file extension must be .csv')
        sys.exit(1)

    csv_path = pathlib.Path(sys.argv[2])
    if not csv_path.is_file():
        print('File not found %s' % sys.argv[2])
        sys.exit(1)

    csv_contents = pd.read_csv(str(csv_path))
    template = template_path.read_text()

    save_email_specs(generate_email_specs(template, csv_contents))

