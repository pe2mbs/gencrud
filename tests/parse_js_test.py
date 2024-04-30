from sly import Lexer, Parser

class TypeScriptLexer( Lexer ):
    tokens      = { "EQ",
                    "NAME",
                    "NUMBER",
                    "CODEBLOCK",
                    "FUNC",
                    "IMPORT",
                    "FROM",
                    "CONST",
                    "EXPORT",
                    "CLASS",
                    "AS",
                    "TRUE",
                    "FALSE",
                    "NEW",
                    "EOL",
                    "CONST_STRING_DQ",
                    "CONST_STRING_SQ",
                    "DIVIDE_THIS",
                    "IF",
                    "STATIC",
                    "ELSE",
                    "WHILE",
                    "PUBLIC",
                    "PRIVATE",
                    "PROTECTED",
                    "CONSTRUCTOR",
                    "THIS",
                    "RETURN",
                    "GET",
                    "PUT",
                    "EXTENDS",
                    "IMPLEMENTS",
                    "SUPER" }
    ignore      = '\t '
    literals = {
        "=",
        "+",
        "-",
        "/",
        "*",
        "(",
        ")",
        ",",
        ";",
        "{",
        "}",
        "[",
        "]",
        ">",
        "<",
        "@",
        ":"
    }
    # Tokens
    NAME                = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER              = r'\d+'
    NAME['import']      = IMPORT
    NAME['from']        = FROM
    NAME['class']       = CLASS
    NAME['const']       = CONST
    NAME['export']      = EXPORT
    NAME['if']          = IF
    NAME['else']        = ELSE
    NAME['while']       = WHILE
    NAME['public']      = PUBLIC
    NAME['private']     = PRIVATE
    NAME['protected']   = PROTECTED
    NAME['static']      = STATIC
    NAME['constructor'] = CONSTRUCTOR
    NAME['this']        = THIS
    NAME['return']      = RETURN
    NAME['get']         = GET
    NAME['put']         = PUT
    NAME['extends']     = EXTENDS
    NAME['implements']  = IMPLEMENTS
    NAME['super']       = SUPER
    NAME['as']          = AS
    NAME['true']        = TRUE
    NAME['false']       = FALSE
    NAME['name']        = NEW
    # Special symbols

    # SINGLE_COMMENT  = r'\/\/[^\n\r]+(?:[\n\r]|\*\))$'
    # MULTI_COMMENT   = r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)'

    @_(r'\/\/[^\n\r]+(?:[\n\r]|\*\))$', r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)')
    def COMMENT( self, t ):
        return t

    EQ              = r'=='
    CODEBLOCK       = r'=>'
    DIVIDE_THIS     = r'/='
    FUNC            = r'\(\)'
    CONST_STRING_DQ = r'".*"'
    CONST_STRING_SQ = r"'.*'"
    IMPORT          = r'import'
    FROM            = r'from'
    CONST           = r'const'
    EXPORT          = r'export'
    CLASS           = r'class'
    IF              = r"if"
    ELSE            = r"else"
    WHILE           = r'while'
    PUBLIC          = r'public'
    PRIVATE         = r'private'
    PROTECTED       = r'protected'
    CONSTRUCTOR     = r'constructor'
    STATIC          = r'static'
    THIS            = r'this'
    GET             = r'get'
    PUT             = r'put'
    RETURN          = r'return'
    EOL             = '\n'
    EXTENDS         = r'extends'
    IMPLEMENTS      = r'implements'
    SUPER           = r'super'
    AS              = r'as'
    TRUE            = r'true'
    FALSE           = r'false'
    NEW             = r'new'
    # Ignored pattern
    ignore_newline  = r'\n'

    # Extra action for newlines
    def ignore_newline(self, t):    # noqa
        self.lineno += t.value.count('\n')

    def error( self, t ):
        print( "Illegal character '%s'" % t.value[ 0 ] )
        self.index += 1



if __name__  == '__main__':
    ts = TypeScriptLexer()
    with open( r'C:\src\python\testrun-web\frontend-v12\src\app\app-routing.module.ts', 'r' ) as stream:
        data = stream.read()

    tokens = ts.tokenize( data )
    for tok in tokens:
        print('type=%r, value=%r' % (tok.type, tok.value))