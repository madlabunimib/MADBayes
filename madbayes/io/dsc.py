DSC_GRAMMAR = r"""

  start: compilationunit
  %ignore " "
  %ignore "\t"
  %ignore "\n"
  %ignore "\r"
  %ignore "//"
  %ignore "/*"
  %ignore "\""
  %ignore ","
  %ignore "|"

  WORD: LETTER (LETTER | DIGIT)*
  LETTER: /[a-zA-Z_-]/
  DIGIT:  /[0-9]/

  DECIMAL_LITERAL: /[0-9][1-9]*/
  FLOATING_POINT_LITERAL: /[0-9]+\.[0-9]*/ (EXPONENT)?
        | /\.[0-9]/ (EXPONENT)?
        | /[0-9]+/ (EXPONENT)?
  EXPONENT: ("e"|"E") ("+"|"-")? /[0-9]+/

  NETWORK: "belief network"
  VARIABLE: "node"
  PROBABILITY: "probability"
  PROPERTY: "property"
  VARIABLETYPE: "type"
  DISCRETE: "discrete"

  PROPERTYSTRING: PROPERTY /[^;]*/ ";"

  compilationunit: networkdeclaration ( variabledeclaration | probabilitydeclaration )*

  networkdeclaration: NETWORK WORD (networkcontent)?

  networkcontent: "{" ( property  )* "}"

  variabledeclaration: VARIABLE probabilityvariablename variablecontent

  variablecontent: "{" ( property | variablediscrete )* "}"

  variablediscrete: VARIABLETYPE ":" DISCRETE "[" DECIMAL_LITERAL "]" "=" "{" variablevalueslist "}" ";"

  variablevalueslist: probabilityvariablevalue ( probabilityvariablevalue )*

  probabilityvariablevalue: (WORD | DECIMAL_LITERAL)

  probabilitydeclaration: PROBABILITY probabilityvariableslist probabilitycontent

  probabilityvariableslist: "(" probabilityvariablename ( probabilityvariablename )* ")"

  probabilityvariablename: (WORD | DECIMAL_LITERAL)

  probabilitycontent: "{" ( property | probabilityentry | probabilitytable )* "}"

  probabilityentry: probabilityvalueslist ":" floatingpointlist ";"

  probabilityvalueslist: "(" probabilityvariablevalue ( probabilityvariablevalue )* ")"

  probabilitytable: floatingpointlist ";"

  floatingpointlist: FLOATING_POINT_LITERAL ( FLOATING_POINT_LITERAL )*

  property: (WORD | DECIMAL_LITERAL)

"""
