#!/usr/bin/python
#
# Copyright (c) 2015 Franklin Scott
# http://www.franklinscott.com/
# Licensed under the BSD-2 license (See file LICENSE).
#
# This project takes user input and creates a nice table that can be rendered 
# in Github Flavored Markdown (https://help.github.com/articles/github-flavored-markdown/#tables).
# Useful if you don't want to expose your content to online tools or if you want your
# tables to look nice in the raw.

import subprocess
import os
import sys
import re
import optparse
import platform

def add_spaces(word, column_size):
    if len(word) > column_size:
        print "WARNING: The word %s is bigger than the buffer size. A rendered table might still look okay. Use with a higher -b option to increase buffer." %(word)
    to_add = column_size - len(word)
    halfBuff = to_add / 2
    while halfBuff >= 0:
        word = " " + word + " "
        halfBuff = halfBuff - 1
    if to_add % 2 == 1:
        word = " " + word
    word = "|" + word
    return word

def load_table(mdtable):
    for x in mdtable:
        rowtemp = 0
        for y in x:
            x[rowtemp] = add_spaces(y, buff)
            rowtemp += 1
    return mdtable

def send_table_out(mdtable, out):
    with open(out, 'w') as f: 
        rowtemp = 0
        for x in mdtable:
            row = ""
            for y in x:
                row += y
            f.write(row + '|\n')
        print ('See %s for groups information.' % (out))

def get_user_prefs():
    print "The number of rows and columns must be greater than zero."
    num_rows = raw_input('Enter the number of rows: ')
    num_columns = raw_input('Enter the number of columns: ')
    try:
        num_rows = int(num_rows)
        num_columns = int(num_columns)
    except ValueError:
        print "Use positive integers to specify the number of rows and columns. Exiting ..."
        sys.exit(0)
    if num_rows < 1 or num_columns < 1:
        print " Seriously, the number of rows and columns must be greater than zero. Exiting..."
        sys.exit(0)
    mdtable = get_user_input(num_rows, num_columns)
    return mdtable

def get_user_input(num_rows, num_columns):
    rtemp = 0
    ctemp = 0

    while rtemp < num_rows:
        row = []
        ctemp = 0
        while ctemp < num_columns:
            if rtemp == 1 and ctemp == 0:
                while ctemp < num_columns:
                    row.append('---')
                    ctemp +=1
                mdtable.append(row)
                row = []
                ctemp = 0  
            row.append(raw_input('Row %i, Column %i: ' % (rtemp + 1, ctemp + 1)))
            ctemp += 1
        mdtable.append(row)
        rtemp = rtemp + 1
    return mdtable
    
usage = "usage: /.%prog [options] Makes a nice table capable of being rendered in Github Flavored Markdown from user input."
parser = optparse.OptionParser(usage=usage)

parser.add_option("-r", type="int", action="store", default=0, help="number of rows")
parser.add_option("-c", type="int", action="store", default=0, help="number of columns")
parser.add_option("-o", action="store", default="mdtable.md", help="name of output file(default: mdtable.md)")
parser.add_option("-b", type="int", action="store", default=15, help="size of buffer (default: 15)")

options, args = parser.parse_args()

num_rows = options.r
num_columns = options.c
buff = options.b

mdtable = []
if num_rows == 0 or num_columns == 0: 
    mdtable = get_user_prefs()
elif num_rows > 0 and num_columns > 0:
    mdtable = get_user_input(num_rows, num_columns)
mdtable = load_table(mdtable)
        
out = options.o
send_table_out(mdtable, out)

if 'CYGWIN' in platform.system():
    print 'use cygstart'
if 'Darwin' in platform.system():
   data = subprocess.check_output(["mate",out])
    
