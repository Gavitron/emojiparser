# emojiparser

> tools to assist with bulk uploading emojis to your Slack!

## Notes

These tools are here to bridge the workflow gaps when trying to migrate slack emojis from one org to another.

## Requirements

[emojipacks](https://github.com/lambtron/emojipacks)
[Slack Emoji Porter](https://github.com/mootcycle/slackporter)

download / setup / install both these tools first, so that you can use this toolset.

Note that emojipacks has to have the extra changes from my fork to work right.

## Usage

### Phase 1: create pack
first phase, we use slackporter to get a list of all 'missing' emoji, then convert that into an emojipack yaml.

start slackporter and let it do its thing.  Let it load a page of emojis.  Scroll this page all the way to the bottom so that it finishes loading everything.  In Chrome, do a `SaveAs, Complete` of the whole page.  you only need the contents of the `<div class="main">` but you may not have to trim the page at all.  put the resulting file into `/src/foo.html`

if you get your emojis somewhere else, you may have to edit `parser.py` to add a mode for your input data.

Finally, run `parser.py foo` to create `out/foo.yaml`

### Phase 2: import pack
this just uses emojipacks to perform a standard bulk import of the new 'foo' pack, and log the output

run `emojipacks -s <slackID> -e <email> -p <pass> -y out/foo.yaml |tee out/foo.log`


### Phase 3: pack rerates
in a perfect world this would have been enough, but sadly, many of your uploads have now failed for myriad reasons.  You have a log of this in `out/foo.log`.

trim `out/foo.log` by hand until it is nothing but lines of the form `key:{json}` and save it as `src/foo.log`

run `reparser.py foo` which will create `out/re-foo.yaml`

finally run `emojipacks -s <slackID> -e <email> -p <pass> -y out/re-foo.yaml |tee src/foo.log`

repeat this until there are no failures reported by `reparser.py`

### Stomping Duplicates
so you've found a better pack, but some of the emoji names are already taken? 

First, run `reparser.py foo True` which will create `out/re-foo.yaml` as a list of only the emojis that didn't get uploaded due to duplicate names.

Next, run `emojipacks -s <slackID> -e <email> -p <pass> -y out/re-foo.yaml --remove |tee -a src/re-foo.log` to delete all those emoji from your slack channel.

Last, run `emojipacks -s <slackID> -e <email> -p <pass> -y out/re-foo.yaml |tee -a src/foo.log` to re-upload all the emoji you just made room for.


## crib notes

`./parser.py sa sa
emojipacks -s <slackID> -e <email> -p <pass> -y out/sa.yaml |tee src/sa.log`
`./reparser.py sa True
emojipacks -s <slackID> -e <email> -p <pass> -y out/re-sa.yaml |tee src/sa.log`
