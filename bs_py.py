import sqlite3

import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('test.sqlite3', check_same_thread=False)
cur = conn.cursor()


res = requests.get(
    'https://comicvine.gamespot.com/profile/theoptimist/lists/top-100-dc-characters/32198/')

html_doc = res.text

soup = BeautifulSoup(html_doc, 'html.parser')


name_list = (soup.select('div#default-content div ul li h3'))

cur.execute('DROP TABLE iam_user ')
cur.execute('CREATE TABLE IF NOT EXISTS iam_user '
            '(name TEXT NOT NULL, family TEXT)')

family = 'DC'
for s_no, name in enumerate(name_list, start=1):
    if s_no == 51:
        family = 'Marvel'
    act_name = ' '.join(name.text.split()[1:]).replace("'", "-")
    print(
        s_no, f"INSERT INTO iam_user (name,family) VALUES ('{act_name}', '{family}')")
    cur.execute(
        f"INSERT INTO iam_user (name,family) VALUES ('{act_name}', '{family}')")
conn.commit()
cur.close()
conn.close()
# l = ['Guy Gardner',
#      'Alfred Pennyworth',
#      'Wally West',
#      'Aquaman',
#      'Wally West',
#      ]

# for i in range(len(l)):
#     print(i+1, l[i])

# family = 'DC'
# for s_no, name in enumerate(l, start=1):
#     if s_no == 51:
#         family = 'Marvel'
#     print(s_no, name, family)
