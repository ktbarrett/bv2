# pyhdltypes

Models of VHDL datatypes in Python.

## Datatypes And Hierarchy

### StdLogic / StdULogic

9-value (`U`, `X`, `0`, `1`, `L`, `H`, `W`, `Z`, `-`) logic type as seen in VHDL.
Because these are value types and not signals, there is no resolving; so `StdLogic` is an alias for `StdULogic`.

### Logic

4-value (`X`, `Z`, `0`, `1`) logic type as seen in Verilog.
Proper subtype of `StdULogic`.

### Bit

2-value (`0`, `1`) bit type.
Proper subtype of `Logic` and `StdULogic`.

### Array

Heterogenous (and thus generic) array datatype.
Arrays have fixed size and arbitrary indexing schemes.
Arrays can be concatenated.

### Record

Record container type as seen in VHDL.
Basically a dataclass, but you inherit instead of decorate.

### StdLogicVector / StdULogicVector

`Array` of `StdULogic`.
Supports bitwise logic operations like `&`, `|`, `^`, and `~`.

### LogicArray

`Array` of `Logic`.
Proper subtype of `StdULogicVector`.

### BitArray

`Array` of `Bit`.
Proper subtype of `LogicArray` and `StdULogicVector`.

### Unsigned

Modeled after VHDL's `unsigned` type.
Proper subtype of `BitArray`.
Supports arithmetic including: `+`, `-`, `*`, `/`, `%`, `rem`, `>>`, `<<`;
and comparisons like: `<`, `<=`, `>`, and `>=`.

### Signed

Modeled after VHDL's `signed` type.
Proper subtype of `BitArray`.
Supports arithmetic including: `+`, `-`, `*`, `/`, `%`, `rem`, `>>`, `<<`;
and comparisons like: `<`, `<=`, `>`, and `>=`.

### Ufixed

Modeled after VHDL's `ufixed` type.
Proper subtype of `BitArray`.
Support arithmetic including: `+`, `-`, `*`, `/`, `%`, `rem`, `>>`, `<<`;
comparisons like: `<`, `<=`, `>`, and `>=`;
and fixed point operations like `resize`.

### Sfixed

Modeled after VHDL's `sfixed` type.
Proper subtype of `BitArray`.
Support arithmetic including: `+`, `-`, `*`, `/`, `%`, `rem`, `>>`, `<<`;
comparisons like: `<`, `<=`, `>`, and `>=`;
and fixed point operations like `resize`.
