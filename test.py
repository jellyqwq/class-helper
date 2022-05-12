import re

text = 'Joxxx'
x = bool(re.match(r'^[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{6,24}$', text, re.I))
print(x)