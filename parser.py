from collections import deque
import re

class Parser:
    tokens = None
    errors = deque()
    debug = False

    # Parser class constructor
    def __init__(self, tokenList, debug = False):
        self.debug = debug                                        # Debug mode prints all called functions to the terminal
        self.tokens = deque(tokenList)                            # Python's double-ended queue is very useful for both queue and stack operations, and it is critical in this implementation
        self.tokens = self.removeComments(self.tokens)        # The parser ignores comments in the source code, so if they exist within the token list, they should be removed before parsing
        
        # Start the parsing by looking for a program
        self.program()

    # Push an error to the syntax error stack
    # This method is called by most of the parsing methods
    def appendError(self, token, message):
        newError = ParseError(message, token)
        self.errors.append(newError)

    # Return the error stack
    def errorStack(self):
        return self.errors

    # Remove all comment tokens from the token queue, as they should not affect the syntax of the program
    def removeComments(self, tokenQueue):
        count = len(tokenQueue)
        for i in range(count):
            if tokenQueue[0].category() == 'comment':
                tokenQueue.popleft()
            else:
                tokenQueue.append(tokenQueue.popleft())
        return tokenQueue


    ## ------ Methods for parsing blocks of tokens ------

    # Identify the addition of one or more terms
    def addition(self):
        if self.debug == True:
            print('addition')

        # Look for one or more terms with addition operations separating them
        # Record a syntax error is there is not at least one term or there is a hanging addition operator at the end of the addition
        while True:
            if not self.term():
                self.appendError(self.tokens[0], 'Addition')
                return False
            
            if not self.addOp():
                break

        return True

    # Identify an addition operator
    def addOp(self):
        if self.debug == True:
            print('addOp')

        # Look at the next token in the queue and see if it is an addition or subtraction sign
        nextToken = self.tokens[0]
        if not (nextToken.word() == '+' or nextToken.word() == '-'):
            return False
        self.tokens.popleft()                                     # Dequeue an operator once it has been identified

        return True
    
    # Identify an assignment statement
    def assignment(self):
        if self.debug == True:
            print('assignment')

        if not self.identifier():
            return False

        # Handle the assignment of an array element
        if (self.tokens[0].word() == '['):
            self.tokens.popleft().word()
            if not (self.integer() and self.tokens[0].word() == ']'):
                self.appendError(self.tokens[0], 'Assignment')
                return False
            self.tokens.popleft().word()

        # Look for the equals sign in the assignment
        if not self.tokens[0].word() == '=':
            self.appendError(self.tokens[0], 'Assignment')
            return False
        self.tokens.popleft()

        # Look for the right-hand expression in the assignment
        if not self.expression():
            self.appendError(self.tokens[0], 'Assignment')
            return False

        return True                                                 # Only return True if all components of an assignment are present

    # Parse a block of statements enclosed within braces
    def block(self):
        if self.debug == True:
            print('block')

        # Look for an opening brace, which indicates that a block exists
        if not self.tokens[0].word() == '{':
            return False
        self.tokens.popleft()

        # Parse through any statements in the block, but let the statements function worry about how to do so
        self.statements()

        # Look for the closing brace of the block and record an error if it doesn't exist
        if not self.tokens[0].word() == '}':
            self.appendError(self.tokens[0], 'Block')
            return False
        self.tokens.popleft()

        return True
        
    # Idenfity a Boolean value
    def boolean(self):
        if self.debug == True:
            print('boolean')

        # Look for the words 'true' and 'false'
        if not (self.tokens[0].word() == 'true' or self.tokens[0].word() == 'false'):
            return False
        self.tokens.popleft()
        return True

    # Identify a character literal
    def char(self):
        if self.debug == True:
            print('char')

        # The length of a character should always be 1
        if len(self.tokens[0].word()) != 1:
            return False

        # The order of an ASCII character (its corresponding integer value) is within the range [0, 127]
        if ord(self.tokens[0].word()) > 127:
            self.appendError(self.tokens[0], 'Char')
            return False
        self.tokens.popleft()

        # If both tests are passed, the word is a character
        return True

    # Parse a conjunction of one or more equalities
    def conjunction(self):
        if self.debug == True:
            print('conjunction')

        # Iterate through as many equalities as can be found in the statement
        while True:
            if not self.equality():
                self.appendError(self.tokens[0], 'Conjunction')
                return False

            # If there is no conjunction operator to join another equality to the end of the statement, assume the conjunction is over
            if not self.tokens[0].word() == '&&':
                break
            self.tokens.popleft().word()                          # Dequeue the conjunction operator if it exists

        return True

    # Parse through a variable declaration (or multiple declarations within the same statement)
    def declaration(self):
        if self.debug == True:
            print('declaration')

        # Consume the type of the declaration
        if not self.type():
            return False

        # Handle the individual variable identifier(s)
        while True:
            if not self.identifier():
                self.appendError(self.tokens[0], 'Declaration')

            # Deal with the declaration of an array
            if (self.tokens[0].word() == '['):
                self.tokens.popleft().word()
                if not (self.integer() and self.tokens[0].word() == ']'):
                    self.appendError(self.tokens[0], 'Declaration')
                    return False
                self.tokens.popleft().word()
            
            # Check if there is another variable being declared in the same statement
            if not self.tokens[0].word() == ',':
                break
            self.tokens.popleft().word()

        # Deal with the semicolon at the end of a declaration
        if not self.tokens[0].word() == ';':
            self.appendError(self.tokens[0], 'Declaration')
            return False
        self.tokens.popleft().word()

        return True

    # Parse through a sequence of one or more declarations
    def declarations(self):
        if self.debug == True:
            print('declarations')

        numDecl = 0

        while (True):
            if not self.declaration():
                break
            numDecl += 1

        # Ensure there is at least one declaration before confirming that there are declarations in the program
        if numDecl < 1:
            return False
        return True

    # Check whether there is an equality within a given expression. An equality is made up of one or two relations
    def equality(self):
        if self.debug == True:
            print('equality')

        # Check for the first relation
        if not self.relation():
            self.appendError(self.tokens[0], 'Equality')
            return False

        # Check for an equality operator, which indicates that there is another relation in this equality
        if self.equOp():
            if not self.relation():
                self.appendError(self.tokens[0], 'Equality')
                return False

        return True

    # Check for an equality operator, which is either == or !=
    def equOp(self):
        if self.debug == True:
            print('equOp')

        nextToken = self.tokens[0]
        if not (nextToken.word() == '==' or nextToken.word() == '!='):
            return False
        self.tokens.popleft().word()

        return True

    # Parse through an expression, which is made up of one or more conjunctions, connected by the || symbol
    def expression(self):
        if self.debug == True:
            print('expression')

        # Loop to consume one or more conjunctions that make up this expression
        while True:
            if not self.conjunction():
                self.appendError(self.tokens[0], 'Expression')
                return False

            # Check for a || symbol, which indicates there will be another conjunction in the expression
            if not self.tokens[0].word() == '||':
                break
            self.tokens.popleft().word()

        return True

    # Parse a factor, which is made up of an optional unary operator and a primary value or variable
    def factor(self):
        if self.debug == True:
            print('factor')

        self.unaryOp()                                            # Consume a unary operator if it exists, but don't generate any errors if it is not present

        # Consume the primary
        if not self.primary():
            self.appendError(self.tokens[0], 'Factor')
            return False

        return True

    # Check whether a token is a float. This is simple because the lexer categorizes float values with the category 'float' already
    def float(self):
        if self.debug == True:
            print('float')

        if not self.tokens[0].category() == 'float':
            return False

        return True
                
    # Check if there is an identifier. This is simple because the lexer assigns identifiers to the category 'identifier'
    def identifier(self):
        if self.debug == True:
            print('identifier')

        if not self.tokens[0].category() == 'identifier':
            return False
        self.tokens.popleft().word()
        return True

    # Parse through an if statement and ensure it contains the correct keyword, punctuation, expression, and statement
    def ifStatement(self):
        if self.debug == True:
            print('ifStatement')

        if not self.tokens[0].word() == 'if':
            return False
        self.tokens.popleft().word()

        if not self.tokens[0].word() == '(':
            self.appendError(self.tokens[0], 'If statement')
            return False
        self.tokens.popleft().word()

        if not self.expression():
            self.appendError(self.tokens[0], 'If statement')
            return False
        
        if not self.tokens[0].word() == ')':
            self.appendError(self.tokens[0], 'If statement')
            return False
        self.tokens.popleft().word()

        if not self.statement():
            self.appendError(self.tokens[0], 'If statement')
            return False

        # Deal with an else statement following the if statement
        if self.tokens[0].word() == 'else':
            self.tokens.popleft()
            if not self.statement():
                self.appendError(self.tokens[0], 'If statement')
                return False

        return True

    # Check if the next token is an integer
    def integer(self):
        if self.debug == True:
            print('integer')

        if not self.tokens[0].category() == 'integer':
            return False
        self.tokens.popleft().word()
        return True

    # Check if a token is a literal, which could be an integer, float, boolean, or char value
    def literal(self):
        if self.debug == True:
            print('literal')

        if not (self.float() or self.integer() or self.boolean() or self.char()):
            self.appendError(self.tokens[0], 'Literal')
            return False
        return True

    # Parse a multiplication operation
    def mulOp(self):
        if self.debug == True:
            print('mulOp')

        nextToken = self.tokens[0]
        if not (nextToken.word() == '*' or nextToken.word() == '/' or nextToken.word() == '%'):
            return False
        self.tokens.popleft().word()

        return True

    # Parse a primary, which can be a variable, literal, or expression wihin parentheses
    def primary(self):
        if self.debug == True:
            print('primary')

        if self.identifier():

            # Deal with the indexing of an array
            if (self.tokens[0].word() == '['):
                self.tokens.popleft().word()

                if not (self.integer() and self.tokens[0].word() == ']'):
                    self.appendError(self.tokens[0], 'Primary')
                    return False
                self.tokens.popleft().word()

            return True
        elif self.literal():
            return True
        elif self.tokens[0].word() == '(':
            self.tokens.popleft().word()

            if not (self.expression() and self.tokens[0].word() == ')'):
                self.appendError(self.tokens[0], 'Primary')
                return False
            self.tokens.popleft().word()

            return True
        elif self.type():                                         # Parse an expression that is being cast to another data type
            if not self.tokens[0].word() == '(':
                self.appendError(self.tokens[0], 'Primary')
                return False
            self.tokens.popleft().word()

            if not (self.expression() and self.tokens[0].word() == ')'):
                self.appendError(self.tokens[0], 'Primary')
                return False
            self.tokens.popleft().word()

            return True

        self.appendError(self.tokens[0], 'Primary')
        return False

    # Parse a program, which is the topmost component of the source code and contains a very specific header
    def program(self):
        if self.debug == True:
            print('program')

        # Consume the header, which must consist of the tokens 'int', 'main', '(', ')', '{'
        if not (self.tokens.popleft().word() == 'int' and self.tokens.popleft().word() == 'main' and self.tokens.popleft().word() == '(' and self.tokens.popleft().word() == ')' and self.tokens.popleft().word() == '{'):            
            print('Bad program header')
        self.declarations()
        self.statements()

    # Parse a relation, which is one or two additions, separated by a relation operator
    def relation(self):
        if self.debug == True:
            print('relation')

        # Consume the first addition
        if not self.addition():
            self.appendError(self.tokens[0], 'Relation')
            return False

        # Check if there is a relation operator, which indicates there is another addition
        if self.relOp():
            if not self.addition():
                self.appendError(self.tokens[0], 'Relation')
                return False

        return True

    # Check for the presence of a relativity operator
    def relOp(self):
        if self.debug == True:
            print('relOp')

        nextToken = self.tokens[0]
        if not (nextToken.word() == '>' or nextToken.word() == '>=' or nextToken.word() == '<' or nextToken.word() == '<='):
            return False
        self.tokens.popleft().word()

        return True

    # Parse a code statement, consisting of an assignment, if statement, while statement, or semicolon
    def statement(self):
        if self.debug == True:
            print('statement')

        if len(self.tokens) < 1:
            return False

        if self.tokens[0].word() == ';':
            self.tokens.popleft().word()
            return True
        elif (self.block() or self.assignment() or self.ifStatement() or self.whileStatement()):
            return True

        return False

    # Parse a sequence of one or more statements
    def statements(self):
        if self.debug == True:
            print('statements')

        numStat = 0

        while (True):
            if not self.statement():
                break
            numStat += 1

        if numStat < 1:
            return False
        return True
    
    # Parse a term in an expression, which consists of one or more factors
    def term(self):
        if self.debug == True:
            print('term')

        while True:
            if not self.factor():
                self.appendError(self.tokens[0], 'Term')
                return False

            if not self.mulOp():
                break

        return True

    # Check for the presence of a data type, of which int, bool, float, and char are recognized
    def type(self):
        if self.debug == True:
            print('type')

        nextToken = self.tokens[0]
        if (nextToken.category() == 'keyword' and (nextToken.word() == 'int' or nextToken.word() == 'bool' or nextToken.word() == 'float' or nextToken.word() == 'char')):
            self.tokens.popleft().word()
            return True
        return False

    # Check for a unary operator, which is either the unary negative for numeric values or unary negation for logical values
    def unaryOp(self):
        if self.debug == True:
            print('unaryOp')

        nextToken = self.tokens[0]
        if not (nextToken.word() == '-' or nextToken.word() == '!'):
            return False
        self.tokens.popleft().word()
        
        return True

    # Parse a while statement, which has a specific order of reserved words, punctuation, and an expression
    def whileStatement(self):
        if self.debug == True:
            print('whileStatement')

        if not self.tokens[0].word() == 'while':
            return False
        self.tokens.popleft().word()

        if not self.tokens[0].word() == '(':
            self.appendError(self.tokens[0], 'While statement')
            return False
        self.tokens.popleft().word()

        if not self.expression():
            self.appendError(self.tokens[0], 'While statement')
            return False
        
        if not self.tokens[0].word() == ')':
            self.appendError(self.tokens[0], 'While statement')
            return False
        self.tokens.popleft().word()

        if not self.statement():
            self.appendError(self.tokens[0], 'While statement')
            return False
        self.tokens.popleft().word()



# IMPORTANT
# ParseError has been included in this file because the Moodle submission box will only permit 8 files to be uploaded.
# ParseError.py is not needed, but is available upon request from Nathan Hagerdorn (n-hagerdorn@onu.edu).

# ParseError class
# Stores information about a syntax error found while parsing source code
class ParseError:
    message = None
    token = None

    def init(self, message, token):
        self.message = message
        self.token = token

    def message(self):
        return self.message

    def token(self):
        return self.token
        