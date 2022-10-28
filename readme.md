This program contains a lexer and parser to tokenize and parse the syntax of a C-like language.
The lexer uses regular expressions to separate a source code file into tokens and categorize them.
The parser uses recursive-descent parsing to implement the Extended Backus-Naur Form definition of the programming language.

How to Execute:
    To execute the program, ensure you have lexer.py, parser.py, testMain.py, and token.py, in the same folder.
    Navigate to the folder where you have the .py files in your command line of choice, then type "python testMain.py" (without the quotes).
    The program will prompt for a file name, and you may enter the path to the test file of your choice. The provided test files are logic.txt, math.txt, and flow.txt. It works best if you have the test file in the same directory as the .py files.
        If the program cannot find the file you specified, it will throw an error. Ensure the file name you give it is exactly the same as the file's name, including the file extension (.txt in most cases).
    When the program finds the file to which you direct it, it will automatically tokenize and parse the source code, and print a table containing the tokens as well as a stack trace of any syntax error that may exist in the source code.
        Note that all three provided files have valid syntax for the language, so changes need to be made to demonstrate syntax errors.

Testing Files:
    math.txt demonstrates variables, data types, integer and float literals, array indexing, assignments, and mathematical operations.
    logic.txt demonstrates boolean values, logical operators, and unary operators.
    flow.txt demonstrates program flow, including if and while statements, as well as code blocks.

API
        Main Methods:
            main():                         Executes the flow of the program, including file and terminal I/O.
            lexerOutput(lexer):             Prints the tokenized source code from the lexer.
            parserOutput(parser):           Prints the syntax error stack to trace the earliest occurrence of a syntax error in the source code.

    Classes & their public methods
        Lexer
            Takes a text file containing code and splits it into tokens, then categorizes and returns the tokens.
            Public Methods:
                Lexer(file):                Constructor. Conducts the processing of the input file.
                getAll():                   Returns a list of all tokens in the input text.
                next():                     Returns the next token in the lexer's internal list, then iterates to the next token in the list.
                remaining():                Returns the number of tokens that have yet to be iterated through in the lexer's list.
                reset():                    Resets the position of the next() method to the first token in the lexer's list.
                peek():                     Returns the next token within the lexer's internal list without moving to the next item in the list.
            Private Methods:
                __findWords(data):          Splits a line of the input source code into its constituent words, then returns a list of the words.
                __getTokenCategory(word):   Compares a word against a table of reserved words and symbols to try and provide a token category. Will assign the category 'unknown' if the word does not match the table.
                __isIdentifier(word):       Evaluates a word to determine whether it is an identifier.
                __isInteger(word):          Evaluates a word to determine whether it is an integer.
                __isRealNumber(word):       Evaluates a word to determine whether it is a floating-point number.

        Token
            A data type that encapsulates a token's name, category (e.g. keyword, identifier, integer literal), and the line it occurs in a source code file.
            Public Methods:
                Token(category, lineNumber, word):     Constructor. Creates a new Token object.
                category():                 Returns the category under which the token is classified.
                lineNumber():               Returns the number of the line where the token appeared in the source code.
                word():                     Returns the word that has been tokenized from an input source code (e.g. int, while, ;)
            Private Methods:
                None.

        Parser
            Takes a list of tokens returned by a Lexer and analyzes them for syntactic errors.
            Public Methods:
                Parser(tokenList, debug = False):       Constructor. Creates a new Parser object with a list of Tokens and an optional argument for debugging purposes.
                errorStack():               Returns a double-ended queue of all syntac errors detected in the tokenized source code. Can be used as a call stack to determine exactly which token caused a syntax error and which type of language construct was being parsed at the time.

            Private Methods:
                __appendError(token, message):          Creates a new ParseError object using the provided Token and message, then pushes it onto the error stack.
                __removeComments(tokenQueue):           Removes all Tokens of category 'comment' from the Token queue to allow the parsing of a token list that has not yet had all comments removed.
            
            Private Parsing Methods:
                    Each parsing method checks for the presence of a given formula from the language's EBNF definition, and can record a syntax error if the correct sequence of tokens is not present.
                __addition():
                __addOp():                  
                __assignment():
                __block():
                __boolean():
                __char():
                __conjunction():
                __declaration():
                __declarations():
                __equality():
                __equOp():
                __expression():
                __factor():
                __float():
                __identifier():
                __ifStatement():
                __integer():
                __literal():
                __mulOp():
                __primary():
                __program():
                __relation():
                __relOp():
                __statement():
                __statements():
                __term():
                __type():
                __unaryOp():
                __whileStatement():

        ParseError
            Encapsulates information about a syntax error identified by a parser, including the token that causes the error and a message to help the programmer resolve the syntax error.
            Public Methods:
                ParseError(message, token): Constructor. Creates a new ParseError object with the given parameters.
                message():                  Returns the error message produced by the parser.
                token():                    Returns the Token that caused the parse error.
            Private Methods:
                None.
