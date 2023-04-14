### KAH SHIUH TANG 114529235

##### decaf_ast.py
    - AST class
    - Store the values needed for the AST construction
    - Does some basic type-checking
    - Does a top-down traversel to fill out missing values in tree
##### decaf_checker.py  
    - Main class, takes input from the user
    - Used to run the checking code
    - Will print YES if the syntax is valid
##### decaf_lexer.py 
    - Used to turn the code into a token stream
##### decaf_parser.py 
    - Turns the tokens generated and uses bottom up rules to check for errors
    - Tries to construct as much of AST as it can
* Not my parser, checker or lexer code, used Professor Kane's parser, AST add-ons are part of parser is the only part that is mine
