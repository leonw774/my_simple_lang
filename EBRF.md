# The EBRF of Lreŋ

```
bin_digits = "0" | "1";
dec_digits = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
hex_digits = dec_digits | "A" | "B" | "C" | "D" | "E" | "F";
               | "a" | "b" | "c" | "d" | "e" | "f";
bin_number = "0b", bin_digits, {bin_digits};
dec_number = digits, {digits}, [ "." {digits} ];
hex_number = "0x", hex_digits, {hex_digits};
number     = bin_number | dec_number | hex_number;

infix_oper = "+" | "-" | "*" | "/" | "%"

escapables = "\a" | "\b" | "\n" | "\r" | "\t" | "\v" | "\\" | "\'";
printables = hex_digits | ghijklmnopqrstuvwxyzGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~ 
char  := "'" (printable_ascii_charactors | escapables) "'"


expr   := number "{" + expr + "}"
```
