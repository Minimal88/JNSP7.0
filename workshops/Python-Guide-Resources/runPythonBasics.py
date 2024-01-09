#!/usr/bin/env python

################################################################################
# runPythonBasics.py:
# This is the JSNP Python's guide
#
#  Project:        PYTHON-GUIDE
#  File:           runPythonBasics.py
#  Date(YY/MM/DD): 15/05/21
#
#   Author: GNSS Academy
#   Copyright 2021 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
################################################################################


#*******************************************************************************
#*******************************************************************************
#                           PYTHON GUIDE JSNP
#*******************************************************************************
#*******************************************************************************

from math import pi


# Script arguments
#-------------------------------------------------------------------------------
# First, import Python's sys module
import sys

print(sys.argv)

if(len(sys.argv) > 1):
    # Get the first argument
    first_arg = sys.argv[1]

print(first_arg)

# Data types
#-------------------------------------------------------------------------------

# Boolean 
#--------------------------------------

# The Boolean data type is either True or False. Boolean operators are
# ordered by priority: not -> and -> or

## Evaluates to True:
print(1<2 and 0<=1 and 3>2 and 2>=2 and 1==1 and 1!=0)
## Evaluates to False:
print(bool(None or 0 or 0.0 or '' or [] or {} or set()))

# Rule: None, 0, 0.0, empty strings, or empty container
# types evaluate to False

# Integer and Float
#--------------------------------------
# An integer is a positive or negative number without decimal point such as 3.
# A float is a positive or negative number with floating point precision
# such as 3.1415926.
# Integer division rounds toward the smaller integer (example: 3//2==1).

## Arithmetic Operations
x, y = 3, 2
print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x // y)
print(x % y)
print(-x)
print(abs(-x))
print(int(3.9))
print(float(3))
print(x ** y)


# String 
#--------------------------------------
# Python Strings are sequences of characters.

# String Creation Methods:
# 1. Single quotes
print('Yes')
# 2. Double quotes
print("Yes")
# 3. Triple quotes (multi-line)
print("""Yes
We Can""")
# 4. String method
print(str(5) == '5')

# 5. Concatenation
print("Ma" + "hatma")
'Mahatma'

# Whitespace chars:
# Newline \n,
# Space \s,
# Tab \t

## Indexing and Slicing
s = "The youngest pope was 11 years"
print(s[0])
print(s[1:3])
print(s[-3:-1])
print(s[-3:])

x = s.split()
print(x[-2] + " " + x[2] + "s")

## String Methods
y = " Hello world\t\n "
print(y.strip())
print("HI".lower())
print("hi".upper())
print("hello".startswith("he"))
print("hello".endswith("lo"))
print("hello".find("ll"))
print("cheat".replace("ch", "m"))
print(''.join(["F", "B", "I"]))
print(len("hello world"))
print("ear" in "earth")

# If you don’t want characters prefaced by \ to be interpreted as special 
# characters, you can use raw strings by adding an r before the first quote:
print('C:\some\name')
print(r'C:\some\name')

# String format
SubString = "Format examples"
print("%-20s: %d %02d %8d %lf %15.3lf %e" % (
    SubString,
    2,
    2,
    2,
    pi,
    pi,
    pi
))


# Complex numbers 
#--------------------------------------
# Python also has built-in support for complex numbers, and uses the j or J 
# suffix to indicate the imaginary part (e.g. 3+5j).
z = 3+5j
print(z, type(z))


# Lists 
#--------------------------------------
# They are ORDERED

squares = [1, 4, 9, 16, 25]
print(squares)

# Like strings (and all other built-in sequence types), lists can be indexed 
# and sliced:
print(squares[0])  # indexing returns the item
print(squares[-1])
print(squares[-3:])  # slicing returns a new list

# All slice following slice returns a new (shallow) copy of the list:
squares_copy = squares[:]

# Lists also support operations like concatenation:
squares = squares + [36, 49, 64, 81, 100]

print(squares)
print(squares_copy)

# Unlike strings, which are immutable, lists are a mutable type, i.e. it is 
# possible to change their content:
cubes = [1, 8, 27, 65, 125]  # something's wrong here
print(4 ** 3)  # the cube of 4 is 64, not 65!
cubes[3] = 64  # replace the wrong value
print(cubes)

# You can also add new items at the end of the list, by using the append() 
# method (we will see more about methods later):
cubes.append(216)  # add the cube of 6
cubes.append(7 ** 3)  # and the cube of 7
print(cubes)

# Assignment to slices is also possible, and this can even change the size of 
# the list or clear it entirely:
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print(letters)

# replace some values
letters[2:5] = ['C', 'D', 'E']
print(letters)

# now remove them
letters[2:5] = []
print(letters)

# clear the list by replacing all the elements with an empty list
letters[:] = []
print(letters)

# The built-in function len() also applies to lists:
letters = ['a', 'b', 'c', 'd']
print(len(letters))

# It is possible to nest lists (create lists containing other lists), for 
# example:
a = ['a', 'b', 'c']
n = [1, 2, 3]
x = [a, n]

print(x)
print(x[0])
print(x[0][1])


# Dictionaries 
#--------------------------------------
# They are NOT ORDERED

# Unlike lists, which are indexed by a range of numbers, dictionaries are 
# indexed by keys, which can be any immutable type; strings and numbers can 
# always be keys.

# It is best to think of a dictionary as a set of key: value pairs, with the 
# requirement that the keys are unique (within one dictionary). 

# A pair of braces creates an empty dictionary: {}.

calories = {'apple' : 52, 'banana' : 89, 'choco' : 546}

print(calories.keys())
for key in calories.keys():
    print(key)

print(calories.values())
for value in calories.values():
    print(value)

print(calories['apple'] < calories['choco'])
calories['cappu'] = 74
print(calories['banana'] < calories['cappu'])
print('apple' in calories.keys())
print(52 in calories.values())

# Loop over a dictionary
for key, value in calories.items():
    print(key) if value > 500 else None



# Control Flow Statements
#-------------------------------------------------------------------------------

# if 
#--------------------------------------
# Perhaps the most well-known statement type is the if statement. For example:

x = 2

if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
elif x == 1:
    print('Single')
else:
    print('More')


# There can be zero or more elif parts, and the else part is optional. 
# The keyword ‘elif’ is short for ‘else if’, and is useful to avoid excessive 
# indentation. 
# An if … elif … elif … sequence is a substitute for the switch or case 
# statements found in other languages.


# for 
#--------------------------------------
# Measure some strings:
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

for i in range(5):
    print(i)

for i in range(1, 5):
    print(i)

for i in range(1, 10, 2):
    print(i)

# while
#--------------------------------------
a, b = 0, 1
while a < 2000:
        print(a, end=' ')
        a, b = b, a+b 

# break 
#--------------------------------------
for i in range(5):
    print(i)

    if i==2:
        break


# continue 
#--------------------------------------
for i in range(5):
    if i==2:
        continue

    print(i)

# pass 
#--------------------------------------
# The pass statement does nothing. It can be used when a statement is required 
# syntactically but the program requires no action

for i in range(5):
    if i==2:
        # Do nothing
        pass # Without it, IndentationError

    print(i)



# Functions
#-------------------------------------------------------------------------------
def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()
def fib2(n):  # return Fibonacci series up to n
    """Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)    # see below
        a, b = b, a+b
    return result

# Now call the functions we just defined:
fib(2000)

f100 = fib2(100)    # call it
print(f100)         # write the result



# Modules
#-------------------------------------------------------------------------------
# If you quit from the Python interpreter and enter it again, the definitions 
# you have made (functions and variables) are lost. Therefore, if you want to 
# write a somewhat longer program, you are better off using a text editor to 
# prepare the input for the interpreter and running it with that file as input 
# instead. This is known as creating a script. As your program gets longer, you 
# may want to split it into several files for easier maintenance. You may also 
# want to use a handy function that you’ve written in several programs without 
# copying its definition into each program.

# Add MY_MODULES to the Python's search path variable sys.path
sys.path.append("MY_MODULES")

# Now we can import fibo module
import fibo

# Check all the names in fibo
print(dir(fibo))

# We could have also import the functions one by one:
# from fibo import fib, fib2

# Or import all names except those beginning with an underscore (_)
# from fibo import *

# Or using an alias:
# from fibo import fib as fibonacci


# Files
#-------------------------------------------------------------------------------
# open() returns a file object, and is most commonly used with two arguments: 
# open(filename, mode).
f = open('workfile.txt', 'w')

# The first argument is a string containing the filename. The second argument 
# is another string containing a few characters describing the way in which the 
# file will be used. mode can be:
#   'r' when the file will only be read, 
#   'w' for only writing (an existing file with the same name will be erased),
#   'a' opens the file for appending; any data written to the file is 
#   automatically added to the end. 'r+' opens the file for both reading and 
#   writing. 
# The mode argument is optional; 'r' will be assumed if it’s omitted.

# The file can be closed by calling the close() method
f.close()

# But...

# It is good practice to use the with keyword when dealing with file objects. 
# The advantage is that the file is properly closed after its suite finishes
with open('workfile.txt') as f:
    read_data = f.read()
    print(read_data)

    # If the end of the file has been reached, f.read() will return an empty 
    # string ('').
    read_data = f.read()
    print(read_data)
# End of with open('workfile.txt') as f

# Check that file has been closed
print(f.closed)

# Let's write some data in our file
with open('workfile.txt', "w") as f:
    f.write('This is the first line of the file.\n')
    f.write('This is the second line of the file.\n')
# End of with open('workfile.txt') as f

# readline() method reads one line of the file
with open('workfile.txt', "r") as f:
    read_data = f.readline()
    print(read_data)
    read_data = f.readline()
    print(read_data)
# End of with open('workfile.txt') as f

# A more efficient way to read the file line by line
with open('workfile.txt', "r") as f:
    for line in f:
        print(line)
# End of with open('workfile.txt') as f

# Use tell() and seek() to move the file pointer
with open('workfile.txt', "r") as f:
    # Save the reference
    p = f.tell()
    read_data = f.readline()
    print(read_data)
    # Move the pointer to the reference stored in p
    f.seek(p)
    read_data = f.readline()
    print(read_data)
# End of with open('workfile.txt') as f

# An alternative way to read delimiter-separated values (DSV) files
# ----> Check titanic.dat
TitanicDataColumnsList = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]

from collections import OrderedDict
TitanicDataIdx = OrderedDict({})
for i, Id in enumerate(TitanicDataColumnsList):
    TitanicDataIdx[Id] = i

print(TitanicDataIdx)

from pandas import read_csv
read_data = read_csv("titanic.dat", 
delim_whitespace=True, 
skiprows=1, 
header=None,
usecols=[TitanicDataIdx["Survived"],
         TitanicDataIdx["Name"]])

print(read_data)

# Filtering read data
filter_cond = read_data[TitanicDataIdx["Survived"]] == 1
filtered_read_data = read_data[filter_cond]

# The same can be done using loc function
filtered_read_data = read_data.loc[read_data[TitanicDataIdx["Survived"]] == 1]

print(filtered_read_data)

# Accessing data by label
print(filtered_read_data[TitanicDataIdx["Name"]][1])

# Accessing data by position index
print(filtered_read_data[TitanicDataIdx["Name"]].iloc[0])



# Syntax Errors
#-------------------------------------------------------------------------------
# Syntax errors, also known as parsing errors, are perhaps the most common kind 
# of complaint you get while you are still learning Python:
# a     =     ((5*4+(2*6+10))
## Syntax error here ^^^^^^^^
# print(a)

# File name and line number are printed so you know where to look in case the 
# input came from a script.



# numpy
#-------------------------------------------------------------------------------
import numpy as np      # Generally, all external modules are imported at the 
                        # beginning of the script

# NumPy's main object is the homogeneous multidimensional array. It is a table 
# of elements (usually numbers), all of the same type, indexed by a tuple of 
# non-negative integers. In NumPy dimensions are called axes.

# For example, the coordinates of a point in 3D space [1, 2, 1] has one axis. 
# That axis has 3 elements in it, so we say it has a length of 3. In the 
# example pictured below, the array has 2 axes. The first axis has a length of 
# 2, the second axis has a length of 3.

# The basic type: numpy.array
#--------------------------------------
a = np.array([6, 7, 8])
print(a, type(a))

# np.array is the equivalent of Python's range to generate np.arrays
b = np.arange(15).reshape(3, 5)
print(b)
print(b.shape)
print(b.size)
print(b.dtype.name)

# The type of the array can also be explicitly specified at creation time:
c = np.array( [ [1,2], [3,4] ], dtype=complex )
print(c)

# Other ways to create np.arrays
d = np.zeros( (3,4) )
print(d)

e = np.ones( (2,3,4), dtype=np.int16 )        # dtype can also be specified
print(e)

f = np.empty( (2,3) )                         # uninitialized, output may vary
print(f)

# Some methods implemented in np.arrays
a = np.random.random((2,3))                     # unidimensional array
print(a)
print(a.sum())
print(a.min())
print(a.max())

b = np.arange(12).reshape(3,4)                  # bidimensional array
print(b)
print(b.sum(axis=0))                            # sum of each column
print(b.min(axis=1))                            # min of each row
print(b.cumsum(axis=1))                         # cumulative sum along each row


# Arithmetic operations
#--------------------------------------
a = np.array( [20,30,40,50] )
b = np.arange( 4 )
print(b)

c = a-b
print(c)

print(b**2)

print(10*np.sin(a))

print(a<35)


# Matrix operations
#--------------------------------------
A = np.array( [[1,1],
               [0,1]] )
B = np.array( [[2,0],
               [3,4]] )

print(A * B)                       # elementwise product


print(A @ B)                       # matrix product


print(A.dot(B))                    # another matrix product


print(np.dot(A,B))                 # another one


# Indexing, Slicing and Iterating
#--------------------------------------
a = np.arange(10)**3

print(a)

print(a[2])

print(a[2:5])

a[:6:2] = -1000    # equivalent to a[0:6:2] = -1000; from start to position 6, 
                   # exclusive, set every 2nd element to -1000
print(a)

print(a[ : :-1])   # reversed a

# Indexing with Arrays of Indices
a = np.arange(12)**2                         # the first 12 square numbers
idx = np.array( [ 1,1,3,8,5 ] )              # an array of indices
print(a[idx])                                # the elements of a at the 
                                             # positions i

j = np.array( [ [ 3, 4], [ 9, 7 ] ] )        # a bidimensional array of indices
print(a[j])                                  # the same shape as j

# Indexing with Boolean Arrays
a = np.arange(12).reshape(3,4)
b = a > 4

print(b)                                     # b is a boolean with a's shape
print(a[b])                                  # 1d array with the selected 
                                             # elements

# Iterating over multidimensional arrays is done with respect to the first axis:
for row in b:
    print(row)


# Linear Algebra
#--------------------------------------
a = np.floor(10*np.random.random((3,4)))

print(a)
print(a.T)

print(np.ravel(a))

b = np.floor(10*np.random.random((4,4)))
print(b)

print(np.diag(b))

print(np.trace(b))

b_inv = np.linalg.inv(b)

print(b_inv @ b)

print(np.eye(b.shape[0]))


# Concatenating arrays
#--------------------------------------
a = np.floor(10*np.random.random((2,2)))
print(a)

b = np.floor(10*np.random.random((2,2)))
print(b)

print(np.vstack((a,b)))

print(np.hstack((a,b)))


# Copying arrays
#--------------------------------------
# Simple assignments make no copy of array objects or of their data.
a = np.arange(12)
b = a            # no new object is created
print(b is a)    # a and b are two names for the same ndarray object

b.shape = 3,4    # changes the shape of a
print(a.shape)

# Python passes mutable objects as references, so function calls make no copy.
def f(x):
    print(id(x))

print(a)
print(id(a))     # id is a unique identifier of an object
f(a)



# matplotlib
#-------------------------------------------------------------------------------
import matplotlib as mpl         # Generally, all external modules are imported 
import matplotlib.pyplot as plt  # at the beginning of the script


def showFigure():
    fig.savefig("my_plot.png", dpi=200., bbox_inches='tight')
    # plt.show()


# Creating a figure
#--------------------------------------
fig, ax = plt.subplots(1, 1, figsize = (8.4,7.6))
showFigure()

# Polar projection
fig = plt.figure(figsize = (8.4,7.6))
ax = fig.add_subplot(111, polar=True)
showFigure()


# Plotting data
#--------------------------------------
# Create figure
fig, ax = plt.subplots(1, 1, figsize = (8.4,7.6))

# Read the data from the file
read_data = read_csv("titanic.dat", 
delim_whitespace=True, 
skiprows=1, 
header=None,
usecols=[TitanicDataIdx["PassengerId"],
            TitanicDataIdx["Survived"],
            TitanicDataIdx["Name"],
            TitanicDataIdx["Age"],
            TitanicDataIdx["Sex"],
            TitanicDataIdx["Pclass"]])

print(read_data)

from numpy.lib.arraysetops import unique

xData = np.array(sorted(unique(read_data[TitanicDataIdx["Age"]])))
yData = np.array([])
for age in xData:
    filter_cond = read_data[TitanicDataIdx["Age"]] == age
    yData = \
        np.append(
            yData, 
            read_data[TitanicDataIdx["Survived"]][filter_cond].sum()
        )

print(xData)
print(yData)

ax.plot(xData, yData)
showFigure()

ax.clear()
ax.scatter(xData, yData)
showFigure()


# Adding a colormap and a colorbar
#--------------------------------------
zData = []
for age in xData:
    filter_cond = read_data[TitanicDataIdx["Age"]] == age
    filter_cond2 = read_data[TitanicDataIdx["Survived"]] == 1
    zData.append(
        read_data[TitanicDataIdx["Pclass"]][filter_cond][filter_cond2].median()
        )
zData = np.array(zData)

print(zData)

# Normalize data into the [0.0, 1.0] interval
vMin = min(zData) # get minimum z
vMax = max(zData) # get maximum z
normalize = mpl.cm.colors.Normalize(vmin=vMin, vmax=vMax)

# Set the position of the colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
color_ax = divider.append_axes("right", size="3%", pad="2%")

# Get a colormap from the list
# print(plt.colormaps())
cmap = mpl.cm.get_cmap('gnuplot')

# Set the colorbar
cbar = mpl.colorbar.ColorbarBase(color_ax, 
cmap=cmap,
norm=normalize,
label="median(Pclass)")

# Handle NaN in zData
filter_nan = np.logical_not(np.isnan(zData))

ax.clear()

# Plot filtering NaN out
ax.scatter(xData[filter_nan], yData[filter_nan], 
c = cmap(normalize(zData[filter_nan])), zorder=10)

showFigure()


# Setting the title, axes, grid...
#--------------------------------------
ax.set_title("Number of Titanic survivors vs age")
ax.set_xlabel("Age")
ax.set_ylabel("Number of survivors")
ax.grid(zorder=0)

showFigure()


# Setting marker
#--------------------------------------
ax.clear()

ax.scatter(xData[filter_nan], yData[filter_nan], 
c = cmap(normalize(zData[filter_nan])), zorder=10,
marker = '+')

showFigure()


# Plot more data
#--------------------------------------
fig, ax = plt.subplots(1, 1, figsize = (8.4,7.6))

y2Data = []
y3Data = []
for age in xData:
    filter_cond = read_data[TitanicDataIdx["Age"]] == age
    filter_cond2 = read_data[TitanicDataIdx["Survived"]] == 1
    y2Data.append(
        np.sum(
            read_data[TitanicDataIdx["Sex"]][filter_cond][filter_cond2] == 'female'
            )
        )
    y3Data.append(
        np.sum(
            read_data[TitanicDataIdx["Sex"]][filter_cond][filter_cond2] == 'male'
            )
        )

ax.scatter(xData, y2Data, zorder=10, marker="*", c='blue')
ax.scatter(xData, y3Data, zorder=10, marker=".", c='orange')

# Set legend
ax.legend(["female", "male"])

ax.set_title("Number of Titanic survivors vs age")
ax.set_xlabel("Age")
ax.grid(zorder=0)

showFigure()


# Second axis
#--------------------------------------
ax.clear()
ax.scatter(xData, yData, zorder=10, marker="+", c='blue')

ax2 = ax.twinx()
ax2.scatter(xData, zData, zorder=10, marker=".", c='orange')

ax.set_title("Number of Titanic survivors vs age")
ax.set_xlabel("Age")

ax2.set_ylabel("median(Pclass)")

ax.grid(zorder=0)

showFigure()

