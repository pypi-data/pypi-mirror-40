#  Copyright (c) 2019 by Amirhossein Bagheri
import re
import string

def removeMultiple(line, char, Shouldhave=True):
    if char == 'all':
        return removeMultiple(removeMultiple(removeMultiple(line, '.'), '?'), '!')
    else:
        line += ' |'
        linex = []

        for l in line.split(char):
            if l != '':
                linex.append(l)
        if Shouldhave:
            line = char.join(linex)
        else:
            line = ''.join(linex)
        return line[:-2]
def RemoveSpaces(text, addDot=False):
    text = re.sub('  +', ' ', text)
    textfinal = []
    for line in text.split('\n'):
        if not line.isspace():
            if len(line) > 1:
                if line[-1] == ' ':
                    line = line[0:-1]
                if addDot:
                    line = removeMultiple(line, '.')
                    line = removeMultiple(line, '!')
                    line = removeMultiple(line, '?')
                    line = line[::-1].lstrip()[::-1]
                    last = line[-1]
                    for i, letter in enumerate(line[::-1]):
                        if letter in string.ascii_letters and letter != '':
                            break
                    line = line[::-1]
                    preline = line[i:][::-1]
                    afterline = line[:i][::-1]
                    afterline = removeMultiple(afterline, '.', False)
                    afterline = removeMultiple(afterline, '!', False)
                    afterline = removeMultiple(afterline, '?', False)
                    if afterline.isspace():
                        afterline = ''
                    if preline.isspace():
                        preline = ''
                    line = preline + afterline
                    line = line.lstrip()
                    if last not in ['?','!']:
                        line += '.'
                    else:
                        line += last
                else:
                    line = removeMultiple(line, '.')
                    line = removeMultiple(line, '!')
                    line = removeMultiple(line, '?')
                    line = line[::-1].lstrip()[::-1]
                    for i, letter in enumerate(line[::-1]):
                        if letter in string.ascii_letters and letter != '':
                            break
                    line = line[::-1]
                    preline = line[i:][::-1]
                    afterline = line[:i][::-1]
                    afterline = removeMultiple(afterline, '.', False)
                    afterline = removeMultiple(afterline, '!', False)
                    afterline = removeMultiple(afterline, '?', False)
                    if afterline.isspace():
                        afterline = ''
                    if preline.isspace():
                        preline = ''
                    line = preline + afterline
                    line = line.lstrip()

            if line != '':
                textfinal.append(line)
    return '\n'.join(textfinal)
