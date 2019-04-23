#!/usr/local/bin/python3
import pprint
import yaml
import sys
import io

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

if (len(sys.argv) == 3):
    val=sys.argv[1]
    mode=sys.argv[2].lower()
elif (len(sys.argv) == 2):
    val=sys.argv[1]
    mode='df'
else:
    print("usage:\n\t%s <foo> [mode]", sys.argv[0])
    exit(1)

emojilist = []

#import list from html
with open("./src/%s.html"%val) as x: html = x.read()
parsed_html = BeautifulSoup(html, 'html.parser')


full_list = parsed_html.findAll('li')
for each in full_list:
    emoji = {}
    emoji['name'] = each.text.strip().translate(str.maketrans('','',':'))
    if mode == 'sa':
        # for slackmoji lists
        emoji['url'] = each.find("img")['src']
    elif mode == 'sm':
        # for slackmoji lists
        emoji['url'] = each.find("img")['src']
    else:
        # for raw slackporter data
        emoji['url'] = each.get("data-url")
    emojilist.append(emoji)

pprint.pprint(emojilist)

# Define data
data =  {'title' : val,
         'emojis': []
        }
for each in sorted(emojilist,key=lambda e: e['name']):
    data['emojis'].append({"name": each['name'],"src":each['url']})

# Write YAML file
yaml.add_representer(dict, lambda self, data: yaml.representer.SafeRepresenter.represent_dict(self, data.items()))
with io.open("./out/%s.yaml"%val,"w+") as outfile:
    yaml.dump(data, outfile, default_style=None, indent=4, default_flow_style=False, allow_unicode=True)
