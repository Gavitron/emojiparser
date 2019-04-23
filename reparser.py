#!/usr/local/bin/python3
import io
import sys
import json
import yaml
import pprint

done = []
takn = []
rate = []
fail = []

if (len(sys.argv) == 3):
    val=sys.argv[1]
    force_rename = True
elif (len(sys.argv) == 2):
    val=sys.argv[1]
    force_rename = False
else:
    print("usage:\n\t%s <foo> [force_rename]", sys.argv[0])
    exit(1)

#import html
with open("./src/%s.log"%val) as x: full_list = x.readlines()

linecount = 0
for each_line in full_list:
    try:
        linecount += 1
        (name,thejson)=each_line.split(':',1)
        thejson=thejson.strip('"\n').encode().decode('unicode_escape')
        data = json.loads(thejson)
        if data['ok']:
            done.append(name)
        elif data['error'] == 'error_name_taken':
            takn.append(name)
        elif data['error'] == 'error_name_taken_i18n':
            takn.append(name)
        elif data['error'] == 'ratelimited':
            rate.append(name)
        else:
            print("ERR: ",data['error'])
            fail.append(name)
    except json.decoder.JSONDecodeError as e:
        print("ERR: line %05d: %s"%(linecount,e))
        exit(1)
    except ValueError as e:
        print("ERR: line %05d: %s"%(linecount,e))
        exit(1)

print("done: %d" % len(done))
print("takn: %d" % len(takn))
print("rate: %d" % len(rate))
print("fail: %d" % len(fail))

if (len(rate)+len(fail)) <= 0:
    print("no emoji to re-rate, ending.")
    exit(0)

print("reading %s yaml"%val)
with open("out/%s.yaml"%val, 'r') as stream:
    try:
        theoldyaml = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

# Define data
print("creating re-%s yaml"%val)
data =  {'title' : val,
         'emojis': []
        }
if force_rename:
    print("forcing renames")
    if len(takn):
        for eachname in sorted(takn):
            src = list(filter(lambda emoji: emoji['name'] == eachname, theoldyaml['emojis']))
            if len(src):
                data['emojis'].append({"name": eachname,"src": src[0]['src']})
else:
    print("Rerating")
    if len(fail):
        for eachname in sorted(fail):
            src = list(filter(lambda emoji: emoji['name'] == eachname, theoldyaml['emojis']))
            if len(src):
                data['emojis'].append({"name": eachname,"src": src[0]['src']})
    if len(rate):
        for eachname in sorted(rate):
            src = list(filter(lambda emoji: emoji['name'] == eachname, theoldyaml['emojis']))
            if len(src):
                data['emojis'].append({"name": eachname,"src": src[0]['src']})

# Write YAML file
print("writing re-%s yaml"%val)
yaml.add_representer(dict, lambda self, data: yaml.representer.SafeRepresenter.represent_dict(self, data.items()))
with io.open("./out/re-%s.yaml"%val,"w+") as outfile:
    yaml.dump(data, outfile, default_style=None, indent=4, default_flow_style=False, allow_unicode=True)
