Introduction
=============

Abstract
----------
Extension of pyparsing. You can easily build your own languages. :v:

Keywords
----------
* PEG
* Regular Expressions
* Parser
* Formal Grammar


## Awesome Feature:

    1. mixedExpression
    2. build languages (see example)
    3. many parse expressions

Requirements
-----------
pyparsing



## Download

`pip install pyparsing_ext`



## Structure

core: basic token classes

actions: classes for parsing actions

utils: some useful tools

Content
=========

Tokens:

    Wordx: powerful Word
    CharsNot: powerful CharsNotIn
    MeanWhile:
    LinenStart:


Functions:

```python
keyRange # more powerful then srange, employing Wordx
ordRange # special keyRange, but is more commonly used
chrRange
CJK # for matching Chinese Japanese Korean
enumeratedItems
delimitedMatrix # delimitedList with two seps
mixedExpression # more powerful than infixedExpression
```



Actions:

```
BaseAction: Base Class of Actions
BifixAction: action for bifix operators such as <x,y>
...
```



Example
=========

```python
w = Wordx(lambda x: x in {'a', 'b', 'c', 'd'}) # == Word('abcd')

M = delimitedMatrix(w, ch1=' ', ch2=pp.Regex('\n+').leaveWhitespace())
p = M.parseString('a b\n c d')
print(p.asList())

s = '''
[1]hello, world
[2]hello, kitty
'''
print(enumeratedItems().parseString(s))

cjk = ordRange(0x4E00, 0x9FD5)
cjk.parseString('我爱你, I love you') # => ['我爱你']

cjk = ordRanges((0x4E00, 0x9FD5, 0, 256))
cjk.parseString('我爱你 I love you') # => ['我爱你 I love you']
```



## build your own languages

```python
import pyparsing_ext.pylang.example

pyparsing_ext.pylang.example.smallPy.cmdline()  # in mode of command line
```
output:
```C
Example 1:
|-1| -> ('|', '|')(-(1))
Example 2:
parse source code:
 
x=|-1|;  # absolute value
y=x*2+1;
if x == 1
{z=[3.3 _]; # the floor value
}
print "z =", z;
 
result:
z = 3 
see the dictionary of variables:
{'x': Decimal('1'), 'y': Decimal('3'), 'z': 3}
```