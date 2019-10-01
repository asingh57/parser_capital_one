# parser_capital_one
Solution of coding assessment by Capital One

Usage:
python3 parse_file filename.ts
OR
python3 parse_file filename.py


# NOTE THAT COMMENT PARSING IS EXTENSION DEPENDENT
Any other file will throw assertion error

I have prepared the following solution in:
Python using BNF grammar parsing

The Backus Naur Form (BNF) for TypeScript was obtained here
https://github.com/frenchy64/typescript-parser/blob/master/typescript.ebnf


Only the following snippet is however, necessary for our purposes. It has been edited to enable TODO recognition

```
<TODO> :: #"TODO:"
<TODOComment> :: TODO CommentContent
<CommentContent> :: TODOComment | #"." CommentContent |""
<LineBreak> :: #"(\n\r|\r\n)|[\n\r]"
<SingleLineComment> ::= '//' CommentContent (LineBreak|"")
<MultiLineComment> ::= '/*' InsideMultiLineComment* ('*/'|"")
<InsideMultiLineComment> ::= !( '*/' | '/*' ) (TODO |(#"." | LineBreak)) | MultiLineComment
<Whitespace> ::= <(#" +" | SingleLineComment | MultiLineComment | LineBreak)>

<ws-opt> ::= Whitespace*
```
Finally, we describe our custom EBNF line (since we don't need all other variable parsing):
```
<code> ::= <ws-opt> #(.*) <code> | ""
```
<code> is enough to parse the whole program

Note the following:
[^abc] (everything except a,b,c)
. anythin except newline
&#35; represents any text
\s+ represents whitespace


For python style code, the implementation needs to be changed a bit
<SingleLineCommentPython> ::= '#[ ]. " CommentContent (LineBreak|"")
<MultiLineCommentPython> ::= SingleLineCommentPython SingleLineCommentPython+
<WhitespacePython> ::= <(MultiLineCommentPython| SingleLineCommentPython| LineBreak)>




Please note the following edge cases and assumptions:

# Case 1
```
/*1
2
*/3
```

AND

```
/*1
*2
*/3
```
are both considered 3 comment lines

# Case 2
```
/* /* */ */
```
are considered TWO block line comments and TWO comment lines

# Case 3
```
// .. // ... 
```
(on the same line) are considered ONE single line comment and ONE comment line

# Case 4

\r\n is considered ONE line break. so is \r by itself, so is \n by itself

However \r\n\r\n would be two line breaks. So would be \r\n\r, \r\n\n and \n\n\r

Note that \r\r\r and \n\n\n are three line breaks each

#Case 5

TODO:TODO: are considered two TODOs.

#Case 6
```
/*

*/
```
AND 
```
/*
*
*/
```
are both 3 lines of block comments

#Case 7
```
a=10&#35;THIS IS AN INT
&#35; THIS IS B
```

The above is one code block (not two individual line comments)