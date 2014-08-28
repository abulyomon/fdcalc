fdcalc
======

fdcalc is concerned with relations' functional dependancies.

The first tool is mincover.py that calculcates minimal cover for a relation's given functional dependancies.

Run
===

mincover's first argument takes a plain text file name containing the functional dependancies in the following format:
```
A->B
B->C
C->D
```

You can try with the supplied example:
```
python mincover.py example.txt
```
