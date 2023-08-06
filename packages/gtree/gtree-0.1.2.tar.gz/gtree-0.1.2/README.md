# PTree

PTree provides a general tree implementation which is not really useful in itself.

## Requirements

The `gtree` package has no requirements other than Python 3.

## Usefulness

Ignoring the statement above, it provides a method for building a tree from dictionaries and convinient methods for iterating trees (bottom up as well as top to bottom).

This means that you can define a tree structure in JSON and YAML files, load it using e.g. using `json.load` and then build a tree.

See examples directory for more!

## Tests

The tests utilize the popular Python module `pytest`. From the project root directory run the following command to run all tests:

```
> pytest tests
```
