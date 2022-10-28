from collections import deque
from lexer import Lexer
from parser import Parser

# Main method for testing the lexer and parser
def main():

    # Prompt the user for input
    print('Please enter the name of your source code file, including the file extension')
    filename = input()

    # Attempt to open a file using the provided file name, and catch the error that is raised when the file cannot be found
    try:
        # Open the file and pass it to the lexer to tokenize the contents
        file = open(filename, "r")
        lexer = Lexer(file)
        file.close()

        lexerOutput(lexer)                                          # Output the results of the lexing process

        # Use the parser to parse all of the tokens that the lexer has generated
        parser = Parser(lexer.getAll())
        parserOutput(parser)                                        # Output the results of parsing

    except FileNotFoundError:                                       # Handle the error that occurs when the user provides the name of a nonexistent file
        print('File not found. Please check that the file', filename, 'exists in the project directory')

# Output a formatted version of the lexer's processed tokens
def lexerOutput(lexer):
    
    # Format the output of tokens as a simple table
    print('{:<10} {:<10} {:<10}'.format('Line #', 'Value', 'Token Category'))
    print('--------------------------------------------------------')
    
    # Print each token using the lexer's next method
    while lexer.remaining() > 0:
        token = lexer.next()
        
        print('{:<10} {:<10} {:<10}'.format(token.lineNumber(), token.word(), token.category()))

# Output the results of parsing, including the locations and contexts of syntax errors in the provided code
def parserOutput(parser):
    errors = parser.errorStack()

    # Indicate if there are no syntax errors detected in the code
    if len(errors) == 0:
        print('No syntax errors detected')

    # Print the error stack, which can be used to trace a syntax error to its specific location in the code
    while len(errors) > 0:
            print('Syntax error in line', errors[-1].token().lineNumber(), ', encountered', errors[-1].token().word(), 'while parsing a(n)', errors.pop().message())

# Execute the main method of the program
if __name__ == "__main__":
    main()
