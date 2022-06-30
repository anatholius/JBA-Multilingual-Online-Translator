import re

# put your regex in the variable template
template = re.compile(r"\d{1,2}[./]\d{1,2}[./](\d{4})")
string = input()
# compare the string and the template
rematch = re.match(template, string)
print(rematch and rematch.groups()[0] or None)
