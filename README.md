See `environment.yml` for dependencies.

Generate `antlr4` classes from our grammar:
```bash
antlr4 -o gen -listener -visitor -Dlanguage=Python3 GrammaireSQL.g4
```

TODOs:
- In Python, deal with the new grammar rules for handling request with time restriction
- Adapt table names to reality

Questions:
- Tables names? Que faire de article/bulletin ?
- How to handle words not existing in Lexicon during lemmatisation?
