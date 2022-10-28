import re               # Regular Expression Library


from token import Token

# Lexer class
# Takes a text file and tokenizes its contents according to a list of common operators, reserved words, and data types in programming languages
class Lexer:
    counter = 0
    tokens = []

    # Lexer class constructor
    def __init__(self, file):    

        # Read individual lines of the file
        # Record the line on which each token appears     
        lineNumber = 0
        while True:
            # Read one line at a time
            lineNumber += 1
            data = file.readline()

            # Once all lines have been read, the last line will be empty, so break out of the loop
            if len(data) == 0:
                break

            # Split the line apart into individual words
            myWords = self.findWords(data)

            # Attempt to categorize each word
            for word in myWords:
                category = self.getTokenCategory(word)              # This method conducts a table matching to attempt to match reserved words and operators
                if category == 'comment':                           # Discard comments, as they are not true tokens
                    break
                if category == 'unknown':                           # Try to categorize the word using individual regex-based methods if the table matching failed
                    if self.isIdentifier(word):
                        category = 'identifier'
                    elif self.isInteger(word):
                        category = 'integer'
                    elif self.isRealNumber(word):
                        category = 'float'
                # Crease a new token and save it to the list of tokens
                newToken = Token(category, lineNumber, word)
                self.tokens.append(newToken)

    # Return all tokens as a list
    def getAll(self):
        return self.tokens

    # Iterate through the list of tokens, one token at a time
    def next(self):
        if self.counter < len(self.tokens):
            nextToken = self.tokens[self.counter]
            self.counter += 1
            return nextToken
        return None

    # Return the number of tokens that have yet to be iterated through
    def remaining(self):
        return len(self.tokens) - self.counter

    # Reset the iteration of the token list
    def reset(self):
        self.counter = 0

    # Peek at the next item in the token iteration without iterating past it
    def peek(self):
        if self.counter < len(self.tokens):
            nextToken = self.tokens[self.counter]
            return nextToken
        return None

    # Split a string of words into individual words using a regular expression
    # This method was provided by Dr. Al-Haj as an example of regular expressions
    def findWords(self, data):

        #How do we split the string?
        # 1. whitespaces
        # 2. punctuations
        # 3. operators

        # The regular expression splits on many different operators and punctuations, as well as all whitespace characters
        splitters = ( "\s+|"
                      "([ \;\,\}\{\(\)\[\]\: ])|"
                      "(\<\=)|(\>\=)|(\=\=)|(\/\/)|(\+\+)|([\+\-\*\/\!\%\<\>\=])|(\|\|)|(\&\&) "
                    )

        # combine all in one string and compile it into a pattern
        splittingPattern = re.compile(splitters)

        # use split() function to split the input data using the compiled pattern
        # filter out the None tokens from the list
        listOfWords = list(filter(None, splittingPattern.split(data)))

        return listOfWords

    # Get teh category of a given word by matching it against a table of reserved words and symbols
    def getTokenCategory(self, word):

        # Dictionary containing all reserved words, operators, and punctuation in the language to be tokenized
        lexDict = {
            'main': 'keyword',
            'int': 'keyword',
            'float': 'keyword',
            'char': 'keyword',
            'bool': 'keyword',
            'if': 'keyword',
            'while': 'keyword',
            'for': 'keyword',
            'else': 'keyword',
            'true': 'keyword',
            'false': 'keyword',
            '{': 'left_brace',
            '}': 'right_brace',
            '(': 'left_parenthesis',
            ')': 'right_parenthesis',
            '[': 'left_bracket',
            ']': 'right_bracket',
            ';': 'semicolon',
            ',': 'comma',
            "'": 'apostrophe',
            '+': 'addition_op',
            '-': 'subtraction_op',
            '*': 'multiplication_op',
            '/': 'division_op',
            '%': 'modulo_op',
            '!': 'negation_op',
            '>': 'greater_op',
            '>=': 'greater_or_equal_op',
            '<': 'less_op',
            '<=': 'less_or_equal_op',
            '||': 'blocking_or_op',
            '&&': 'blocking_and_op',
            '=': 'assignment_op',
            '//': 'comment'
        }

        # Attempt to match the word to a dictionary entry and return unknown if there is no match
        if word in lexDict:
            return lexDict[word]
        else:
            return 'unknown'

    # Determine if a word is an identifier using a regular expression
    def isIdentifier(self, word):

        # Match a letter or underscore, then any sequence of letters and numbers
        identifierPattern = re.compile("^[a-zA-Z_]\w*$")

        if identifierPattern.match(word) is not None:
            return True
        return False

    # Determine if a word is an integer using a regular expression
    # Provided by Dr.Al-Haj
    def isInteger(self, word):

        # Match one of more decimal digits
        integerNumbersPattern = re.compile("^\d+$")

        if integerNumbersPattern.match(word) is not None:
            return True

        return False

    # Determine if a word is a real (decimal/float) number using a regular expression
    def isRealNumber(self, word):

        # Match one or more digits and an optional period with trailing digits
        realNumbersPattern = re.compile("^\d+(.\d+)?$")
        
        if realNumbersPattern.match(word) is not None:
            return True

        return False
