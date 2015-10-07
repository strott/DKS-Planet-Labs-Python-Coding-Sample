# David K Strott
# Octber 7, 2015
# Planet Labs Python Sample
# An anagram is a word formed by rearranging the letters of another, like "topside" and "deposit". 
# In some cases, there might be as many (or more) anagrams than there are characters, like "post", 
# "spot", "stop" and "tops".
#
# Write a program to find all of the anagrams in a dictionary in which there are at least 4 letters 
# in the word and at least as many anagrams as there are letters.
# 
# The dictionary will be a file on disk with one line per word. Your operating system likely already has such a file in
# /usr/dict/words or /usr/share/dict/words.
#
# The output produced by your code should be in this format:
#
# emit, item, mite, time
# merit, miter, mitre, remit, timer
# reins, resin, rinse, risen, serin, siren
# inert, inter, niter, retin, trine
# inset, neist, snite, stein, stine, tsine

print("")
print("This is my first python script, it was written using Python 3.4 on Windows 10.")
print("This script uses a local copy of the dictionay that was stored at /etc/dictionaries-common/words "
      "(symlinked to /usr/share/dict from an Ubuntu 15.04 virtual machine.")
print("The dictionary file contains just under 100000 words will be handled by this script.")
print("\nAssumptions made by this program:")
print("1. Words from the dictionary that start with a capital letter (proper names and other junk at the start of the file) are ignored.")
print("2. Characters with accents are stripped of their accents (ex. Angstrom, eclair).")
print("3. Words that end with \"'s\" (any word that has a possessive form) are ignored.")
print("4. Words that contain less than 4 characters are ignored.")
print("5. The input file is alphabetized to maintain table insertion function simplicity and to keep the Big-O time from getting out of control.")
print("6. The input file has one word per line (i.e. is \\n delimited).")
print("")

# Some choices I'm making in this script (since I'm a python N00B):
# Use something like an insertion sort plunking elements into the Table data structure, which implies at least O(n^2).
# I made my own data structures because I wanted to see how classes work and behave (I probably could have used dict's
# but I wanted something a little more customizable).

# The general algorithm for this script is as follows:
# for each line of the file
#   Check the line (string) for the assumptions listed above.
#   Sort the characters of the string in ascending order (hashing function) and create a key
#   Make a tuple of the Key, word, word size and number of anagrams in the set (initally set to 1).
#   Insert the key/word tuple into the table, either as a new entry, or append the word to an existing key's wordlist.
# Sort the Table by word size to match the implicitely required output.
# Iterate through the table and print anagram sets that have more anagrams than the number of characters in the key.

import unicodedata
from time import gmtime, strftime

def stripAccents(string):
   return ''.join(char for char in unicodedata.normalize('NFD', string) if unicodedata.category(char) != 'Mn')

class KeyWordTuple(object):
    # Data structure for holding key, key length, anagram list, and number of anagram tuples.
    def __init__(self,key=None,length=None,num=None,words=None):
        if key is None:
            self.key = ""  # contains the hash key (ie. an alphabetic sort of a strings characters).
        else:
            self.key = key

        if length is None:
            self.length = 0  # the length of the word, used for checking against occurrences later.
        else:
            self.length = length

        if num is None:
            self.num = 0  # the number of times the hash key hits.
        else:
            self.num = num

        if words is None:
            self.words = []  # The list of anagrams found for a specific hash key.
        else:
            self.words = []
            self.words.append(str(words))

    def __str__(self):
        tempStr = "key: " + self.key + ", length: " + str(self.length) + ", num: " + str(self.num) + "; anagram list: "

        first = True
        for item in self.words:
            if first is True:
                tempStr += item
                first = False
            else:
                tempStr += ", " +str(item).strip('[\'\']')

        return tempStr

    def pushWord(self, word):
        # This function should only be called when the word list contains one or more words. A try/catch would be more
        # robust to have in here, but I'll learn more about exception handling later...
        self.words.append(str(word))
        self.num += 1

    def getKey(self):
        return self.key

    def getWords(self):
        return str(self.words)

    def getLength(self):
        return self.length

    def getNum(self):
        return self.num

    def printAnagramList(self):
        tempStr = ""

        first = True
        for item in self.words:
            if first is True:
                tempStr += item
                first = False
            else:
                tempStr += ", " +str(item).strip('[\'\']')

        return tempStr


class Table(object):
    # Data structure for holding KeyWordTuple objects.
    def __init__(self):
        # Start with zero size and an empty list of keys.
        self.size = 0
        self.keyList = []

    def __str__(self):
        # Convert the entire contents of the Table to a string for output to the standard output.
        tempString = ""

        for item in self.keyList:
            tempString += str(item) + "\n"

        return tempString

    def insert(self, keyWordTuple):
        if self.size == 0:
            # if the Table's word list is empty, simply the KeyWordTuple to the Table append without insertion checks.
            self.keyList.append(keyWordTuple)
            self.size += 1
        else:
            # Variable to contain the insertion index point.
            tempIndex = 0

            # Iterate through the Table's key list, find the correct insertion point (assumes alphabetical order).
            for item in self.keyList:
                # Checks to see if the input key is less than the key in the Table, breaks if it is to halt the
                # index from incrementing any further. Also, by initializing the index to 0 for each pass through the
                # list, keys that belong at the head of the list can be inserted properly.
                if keyWordTuple.getKey() < item.getKey():
                    break

                # Check to see if the word should be appended to the word list of a key that already exists.
                if keyWordTuple.getKey() == item.getKey():
                    # If the key already exists, push word onto the KeyWordTuple's word list.
                    item.pushWord(keyWordTuple.getWords())
                    # If equality is found, set index to -1 so that the if/else after this for loop ignores this tuple
                    # and doesn't try to insert the tuple again.
                    tempIndex = -1
                    break

                # Increment the insertion index.
                tempIndex += 1

            # If the word wasn't already added to an existing key, then add the new key/word combo to the table in the
            # appropriate position, and increment the size member.
            if tempIndex != -1:
                if tempIndex == self.size:
                    self.keyList.append(keyWordTuple)
                    self.size += 1
                else:
                    self.keyList.insert(tempIndex, keyWordTuple)
                    self.size += 1

    def getSize(self):
        return self.size

    def sortResults(self):
        # Sort the key list based on the length of the key.
        self.keyList.sort(key=lambda keyWordTuple: keyWordTuple.getLength())

    def printResults(self):
        # print only the results where the
        for item in self.keyList:
            if item.getNum() >= item.getLength():
                print(item.printAnagramList())

# MAIN FUNCTION
# Instantiate a Table class object.
table = Table()

# Set verbose to true to get some extra content output to the terminal.
verbose = False

# Open the dictionary file in read mode, iterate through the contents of the file, and generate anagram lists.
print("Reading input file (start time: " +strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ")...")
#with open('test_input', 'r') as inputFile:
with open('words', 'r') as inputFile:
    for line in inputFile:

        # Strip accents from words that contain non-a-to-z characters.
        inString = stripAccents(line)

        # Create a character array from the line read from the input file.
        charArray = list(inString)

        # Remove the trailing \n from the string and then sort the characters of the string to produce the "hash" value.
        if charArray[-1] == '\n':
            charArray.pop()
            word = ''.join(charArray)
            charArray.sort()
        else:
            word = ''.join(charArray)
            charArray.sort()

        # Check to make sure the word from the dictionary is greater than 4 characters, if not, ignore it.
        if (len(charArray) >= 4) and (word.islower()) and ('\'' not in word):
            # Make a string from the sorted key character array hash function.
            key = ''.join(charArray)
            # Create the key word tuple.
            keyWordTuple = KeyWordTuple(key,len(charArray),1,word)
            # Insert the key word tuple into the table.
            table.insert(keyWordTuple)
        else:
            if verbose is True:
                if len(charArray) < 4:
                    print(word + " is being ignored because it contains less than 4 characters.")
                if not word.islower():
                    print(word + " is being ignored because it contains a capital letter.")
                if '\'' in line:
                    print(word + " is being ignored because it is pluralized.")
            else:
                pass

# Close the input file elegantly.
inputFile.close()

# Sort the contents of the table so that the keys with fewer characters precede keys with more characters.
print("\nSorting the results (start time: " +strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ")...")
table.sortResults()

# Print the entire contents of the table if verbose set to true.
if verbose is True:
    print("Table Contents:\n" + str(table))

# Print the resulting sorted table of anagrams
print("\nResults of running this script on the included dictionary file (start time: " +strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "):")
table.printResults()

print("\nEnd time: " +strftime("%Y-%m-%d %H:%M:%S", gmtime()))