# my_simple_lang

My simple programming language written in Python

## Usage

```
python3 simple_lang.py {file_path}
```

or 

```
python3 simple_lang.py -c "{some codes}"
```

## Data types

There are 4 types of objects:
- Number: rational number implemented by Python `Fraction` class
- Pair: store the references to two objects
- Function: store executable codes and an optional argument identifier
- Null: same as python None type

## Operators

### Arithmetics

The `+`, `-`, `*`, `\`, `%`, `^` only accept number type and work just as you expect.

### Comparison

The comparison operators compare two objects by their values. The `>`, `<`, `>=`, `<=` can only compare numbers. The `==`, `!=` can compare on all data types.

For pair objects, it compare their reference objects recursively. They return number `1` if the comparison result is true, otherwise `0`.

### Logic

The logic operators `!` (NOT), `|` (OR) and `&` (AND) return `0` and `1` like comparison operators. All data type has their rule to evaluates to boolean. The boolean value of a number object is true if it is not 0, otherwise false. The null object is always false. Pair and function objects are always true. 

They do *not* short-circuit. If you want something like a if-statement, use `?`.

### Assignment

assignment operator `x = expr` requires the `x` at the left hand side to be a single variable. It assigns the evaluated value of right hand side expression to the left hand side variable and evalautes the same right hand side value.

### Pair maker, left getter and right getter

The pair maker `,` makes a pair is right-associative, so that it can be used to make linked list. See example codes `fizzbuzz.txt` and `hello_world.txt`. Theoretically, you can also use pair object to make a binary tree, and thus a set and a map.

Use `` `x `` and `~x` to get the left and right element of the pair.

### Function maker and argument setter

The function maker `{}` turns the wrapped codes into a function (no argument by default). You can use the argument setter `:` to bind *one* argument identifier to a function. Use currying or pair to pass more things.

### If operator

The "if" operator `?` is the logical-or operation that short-curcuits. If the left hand side is false in boolean, it stops and evaluates to the left hand side, otherwise, the right hand side will then be evaluated and the whole expression evaluates to the same as the right hand side.

For example, `(1 == 2) ? x = 3` evalautes to `0` and the assignment of `3` to variable `x` does not happen because the right hand side is ignored. The expression `(1 == 1) ? x = 3` evalautes to `3` and the variable `x` equals to `3` after evaluation.

### Function caller

The function caller are `()` and `$`. The syntax is `func_name(expr)` and `func_name $ expr`. It assigns the evaluated result of the expression to the argument varriable of the function (if any) and evaluates the function code. The syntax `func_name()` is valid and will be parsed as `func_name(null)`.

### Expression connector

The expression connector is `;`. It connects two expressions into one and evaluates to the later one.

### stdout writer

The `<<` operation output a number as a byte to the stdout (actually via Python `print(chr(x))`). This operator always evaluates to null.

## Variables

Variables identifier complies in regex `[_a-zA-z][_a-zA-z0-9]+`. Variables can be used without being assigned first and are default to be null. For example, code `b = 2; a == b` is valid and evaluates to `0` because `null` does not equal to number `2`.

## Expression

All the codes, including those wrapped in function maker `{}`, should a signle expression and evaluates to one object eventually.   
