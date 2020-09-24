# Constraint programming for synthetic biology

## A tool for biocompilation implemented with MiniZinc as part of a 3rd Year Computer Science project.

Aims to create valid devices using specified parts and avoiding specified restriction sites.

Objective function makes use of Chargraff's Second Parity Law by attempting to find device that minimises the differences in numbers of base nucleotides.



## Requires
 - Python3
 - MiniZinc (https://www.minizinc.org/) 

## How to use

- Download XML data for parts from iGEM registry (e.g. http://parts.igem.org/cgi/xml/part.cgi?part=BBa_E0040) and place in `backend/parts/`
- From project root run `python3 ./backend/process.py` in a terminal
