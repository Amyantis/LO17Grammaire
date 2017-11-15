grammar GrammaireSQL;

requete
    : (SELECT|COUNT) (ARTICLE | BULLETIN) (MOT ps = params)* (WHEN te = time_expression)*
    ;

params
    : par1 = param (CONJ par2 = param)*
    ;

param
    : a = VAR
    ;

time_expression
    : (year | date | date_interval)
    ;

date_interval
    : date date
    ;

date
    :
    (day DATE_SEPARATOR month DATE_SEPARATOR year) |
    (day MONTH year)
    ;

year
    : DIGIT DIGIT DIGIT DIGIT
    ;

month
    : DIGIT DIGIT
    ;

day
    : DIGIT DIGIT
    ;

// Lexer rules
SELECT: 'vouloir' | 'voudrais' | 'voulais' | 'souhaite' | 'lister' | 'trouve';
COUNT: 'combien';
ARTICLE: 'article' | 'articles';
BULLETIN: 'bulletin';
CONJ: 'et' | 'ou';
POINT: '.';
MOT: 'mot' | 'contenir' | 'parler' | 'parlent';
WS : (' ' |'\t' | '\r' | 'je' | 'qui' | 'dont') -> skip;
VAR : ('A'..'Z' | 'a'..'z') ('a'..'z')+;

WHEN: 'parus' | 'paru' | 'écrites';
DIGIT: [0-9];
DATE_SEPARATOR: ('/' | '-');
MONTH: 'janvier' | 'fevrier' | 'mars' | 'avril' | 'mai' | 'juin' | 'juillet' | 'aout' | 'septembre' | 'octobre' | 'novembre' | 'decembre';