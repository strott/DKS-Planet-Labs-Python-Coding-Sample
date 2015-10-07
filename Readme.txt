This is my first python script. It was written and tested using Python 3.4 on Windows 10.

The file 'test_input', it is based on the email instructions with a few extra words thrown in there for testing.
The File 'words' is the dictionary copied from Ubuntu.
An example output of the program can be seen in 'ExampleOutput.txt'

The script takes about 20 minutes to run on a Core i7-4712HQ with 16GB of RAM. This is mostly due to my insertion algorithm
having a run time of O(n^2), plus the extra time it takes to sort the output based on key size, as well as iterating through
the table and printing the formatted output to the terminal. I purposefully chose not to use a dict data structure so I 
could play around with classes.