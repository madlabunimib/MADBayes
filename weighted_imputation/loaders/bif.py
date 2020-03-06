"""
The Interchange Format for Bayesian Networks (BIF)

Ref: http://www.cs.washington.edu/dm/vfml/appendixes/bif.htm

A more formal description of the proposed Interchange Format is given
here. The notation used by the Jack parser generator is used here. 
In the description below, the patterns used by the lexer to define
tokens are very similar to regular expressions used by the Unix regexp
facility. Non-terminals have a parenthesis pair "()" after their
names; terminals are usually capitalized. Some structures that may
appear in expansions are: 

   ( e )?      : An optional occurrence of e
   e1 | e2 | e3 | ... : A choice of e1, e2, e3, etc.
   ( e )+             : One or more occurrences of e
   ( e )*             : Zero or more occurrences of e
   ["a"-"z"] matches all lower case letters
   ~["\n","\r"] matches any character except the new line characters


--------------------------------------------------------------------------------

The following patterns are ignored when they appear between tokens: 

" "
"\t"
"\n"
"\r"
"//" (~["\n","\r"])* ("\n"|"\r\n")
"/*" (~["*"])* "*" (~["/"] (~["*"])* "*")* "/"
","
"|"


--------------------------------------------------------------------------------

The definition of a word is: 

WORD: LETTER (LETTER | DIGIT)*
LETTER: ["a"-"z","A"-"Z","_","-"]
DIGIT:  ["0"-"9"] 


--------------------------------------------------------------------------------

The definition of a non-negative integer number is: 

DECIMAL_LITERAL: ["1"-"9"] (["0"-"9"])* 



--------------------------------------------------------------------------------
The definition of a non-negative real number is: 
FLOATING_POINT_LITERAL: (["0"-"9"])+ "." (["0"-"9"])* (EXPONENT)? 
      | "." (["0"-"9"])+ (EXPONENT)? 
      | (["0"-"9"])+ (EXPONENT)? 
#EXPONENT: ["e","E"] (["+","-"])? (["0"-"9"])+


--------------------------------------------------------------------------------

The following words are keywords: 

NETWORK: "network" 
VARIABLE: "variable" 
PROBABILITY: "probability" 
PROPERTY: "property" 
VARIABLETYPE: "type" 
DISCRETE: "discrete" 
DEFAULTVALUE: "default" 
TABLEVALUES: "table" 


--------------------------------------------------------------------------------

A property is defined as: 

PROPERTYSTRING: PROPERTY (~[";"])* ";"


--------------------------------------------------------------------------------

The productions of the grammar are: 

CompilationUnit() :
  NetworkDeclaration() 
  ( VariableDeclaration()   |    ProbabilityDeclaration()  )*
  EOF

NetworkDeclaration() :
  NETWORK WORD NetworkContent()

NetworkContent() :
  "{" ( Property()  )* "}"

VariableDeclaration() :
  VARIABLE ProbabilityVariableName() VariableContent()

VariableContent(String name) :
  "{"  ( Property() | VariableDiscrete() )*   "}"

VariableDiscrete() :
  VARIABLETYPE DISCRETE 
    "[" DECIMAL_LITERAL "]" "{"    VariableValuesList()    "}" ";"

void VariableValuesList() :
    ProbabilityVariableValue() 
    ( ProbabilityVariableValue() )*

ProbabilityVariableValue() : WORD

ProbabilityDeclaration() :
  PROBABILITY ProbabilityVariablesList() ProbabilityContent()

ProbabilityVariablesList() :
   "("  ProbabilityVariableName() ( ProbabilityVariableName()   )* ")"

ProbabilityVariableName() : 

ProbabilityContent()
  "{" ( Property() | ProbabilityDefaultEntry()   | ProbabilityEntry()
  |
      ProbabilityTable()  )* "}"

ProbabilityEntry() :
   ProbabilityValuesList() FloatingPointList() ";"

ProbabilityValuesList() :
   "(" ProbabilityVariableValue() ( ProbabilityVariableValue()   )*
   ")"

ProbabilityDefaultEntry() :
   FloatingPointList() ";"

ProbabilityTable() :
   FloatingPointList() ";"

FloatingPointList() :
  FloatingPointToken()  ( FloatingPointToken()  )*

FloatingPointToken() :  

Property() :  



--------------------------------------------------------------------------------
"""