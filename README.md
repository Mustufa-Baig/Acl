# ACL - Asynchronous Computation Language
A Statically-Typed Functional Programming Language <br/>
(currently implemented in Python)
## Installation Prerequisite
* Python 3.12 or above
# Documentation
### Print Statements
ACL currently does not require any quotation for printing text  
use the `print` keyword to print any text or variable  
> print hello world  

use `printl` for inline printing
> printl Enter a number ->

Variables can be added in print statements, using ^expression^ synatax  
> print Pi is ^pi^  

### Comments
Comments are made using `~` symbol <br/>At least one space is required, otherwise it is considered a Jump Position
> ~ this is a comment

### Jump Statements
Comments without Spaces are considered as Jump Positions  
> ~this_is_a_jump_position

To perform a Jump, The `goto` keyword is used along with a jump position  
> goto this_is_a_jump_position

### Variables
There are currently 3 supported DataTypes in ACL <br/>
1. Integers 
> int num = 7
2. Double-Precision Floating point numbers
> float pi = 3.14
3. Strings
> string name = "Mustafa"

### Variable Operations
All numerical notations are PostFix
> int num = num 3+

Strings support concatenation and multiplication  
> string name = name " Baig" +  
> string greet = "he" "l" 2*+ "o "+

the ^expression^ synatax in print statements also applies to calculations  
> print ^greet 2*^  
> print calculated answer = ^3 7+ 5* 9 5+ +^ and ^8 2 2* *^

### Conditionals
ACL currently support + - * / % <br/>
As well as comparison operators < <= > >= = !=  
>if num 2%=0  
>	print ^num^ is even  
>else  
>	print ^num^ is odd  
>end  

All Indentation is ignored and is completely Optional

### User Input
The input keyword prompts the user for a keyboard input in the console
> int num = input

and works on all datatypes  
> string name = input
