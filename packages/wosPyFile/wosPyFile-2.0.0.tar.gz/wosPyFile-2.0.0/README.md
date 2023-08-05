# PyFile

PyFile is a simple library which provides you some funcionalities for file reading and writing.

# Install

    from wosPyFile import pyFile

# Files

PyFile is effective on simple text files, let's see some examples:

## Reading

###  Read all
This will return all lines

    pyFile.read("file.txt")


###  Read with conditions
 This will return only lines that begins with the list elements
  
    pyFile.read("file.txt", ["AAA", "BBB", "CCC"])

## Extracting data from lines
Let's assume that we have a variable called **line** with the value bellow
		

> **ABC1234567**

To extract data from this line, you can use pyFile.getLineData(), the second parameter is responsible to split the line in list elements

	   pyFile.getLineData(line, [3,10])
	  	  
Output:

> ["ABC", "1234567]


## Matrix

If you have a defined range you can use pyFile.generateMatrix()

    data = []
    collumns = 240
    size = 2
    matrix = pyFile.generateMatriz(collumns, len(lines), size)
    for index, line in  enumerate(lines):
	    pyFile.getLineData(line, matrix[index])
	

>A list element will be generated according with the interval defined in **size**


