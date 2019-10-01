#!/usr/bin/python3
import sys
import parsing_libs
#main parser caller
#AUTHOR: Abhi Singh
#email: abhijit.singh@mail.mcgill.ca 
#PLEASE READ README.md to CONSULT THE BNF (Backus Naur Form) Specification

assert len(sys.argv) == 2
data=""

extension = sys.argv[1].split('.')[-1]
assert extension=="py" or extension=="ts"

with open(sys.argv[1], 'r') as file: #open and read file
    data = file.read()

parsing_libs.run(extension,data)

print(
" Total # of lines:",parsing_libs.total_lines_ct,"\n",
"Total # of comment lines:",parsing_libs.comment_lines_ct,"\n",
"Total # of single line comments:",parsing_libs.single_line_ct,"\n",
"Total # of comment lines within block comments:",parsing_libs.comment_lines_block_ct,"\n",
"Total # of block line comments:",parsing_libs.blocks_ct,"\n",
"Total # of TODO's:",parsing_libs.todo_ct
)



