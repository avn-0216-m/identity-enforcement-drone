import re


string = "beep boop beep boop beepboop"
word = "boop"
regex = "(?<!\w)boop(?!\w)"

for match in re.finditer(regex, string):
    print(match.start())
    print(match.group())