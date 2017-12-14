grammar GrammaireSQL;

requete:
    ((SELECT|COUNT)? (type_ = TYPE)?) ((MOT? ps = params) | (WHEN te = time_expression))*
    ;

params:
    par1 = param (conj = CONJ par2 = param)*
    ;

param:
    a = VAR
    ;

time_expression:
    (year_ = year | month_year_ = month_year | date_interval_ = date_interval | date_ = date)
    ;

date_interval:
    a = date CONJ_ET b = date
    ;

date:
    (day_ = day DATE_SEPARATOR month_ = month DATE_SEPARATOR year_ = year) |
    (day_ = day MONTH year_ = year)
    ;

month_year:
    month_ = MONTH year_ = year
    ;

year:
    digit1 = DIGIT digit2 = DIGIT digit3 = DIGIT digit4 = DIGIT
    ;

month:
    digit1 = DIGIT digit2 = DIGIT
    ;

day:
    digit1 = DIGIT digit2 = DIGIT
    ;

// Lexer rules
SELECT: 'vouloir';
COUNT: 'combien';
TYPE: 'article' | 'rubrique' | 'contact';

CONJ: 'et' | 'ou';
CONJ_ET: 'et';
MOT: 'mot' | 'contenir' | 'parler' | 'parlent';

WHEN: 'parution' | 'en';
DIGIT: [0-9];
DATE_SEPARATOR: ('/' | '-');
MONTH: 'janvier' | 'fevrier' | 'mars' | 'avril' | 'mai' | 'juin' | 'juillet' | 'aout' | 'septembre' | 'octobre' | 'novembre' | 'decembre';

// Don't change order as it might overide previous lexer rules
WS : (' ' |'\t' | '\r' | 'je' | 'qui' | 'dont') -> skip;
VAR : ('A'..'Z' | 'a'..'z') ('a'..'z')+;