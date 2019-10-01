#!/usr/bin/python3
import sys, re

#AUTHOR: Abhi Singh
#PLEASE READ README.md to CONSULT THE BNF (Backus Naur Form) Specification

assert len(sys.argv) == 2
total_lines_ct,comment_lines_ct,single_line_ct,comment_lines_block_ct,blocks_ct,todo_ct=1,0,0,0,0,0
data=""

with open(sys.argv[1], 'r') as file: #open and read file
    data = file.read()


def todo(in_str):#matches todo from the start and returns end of match index. -1 if no match
    
    pattern = re.compile("^(TODO:)")
    for m in pattern.finditer(in_str):
        global todo_ct
        todo_ct+=1
        return m.end()
    return -1

def todo_comment(in_str):#matches todo comment from the start and returns end of match index. -1 if no match
    todo_pos=todo(in_str)
    if (todo_pos==-1):
        return -1
    if todo_pos==len(in_str):
        return todo_pos
    cc= comment_content(in_str[todo_pos:])
    if cc==-1:
        return -1
    return cc + todo_pos
    
def comment_content(in_str):#matches comment content from the start and returns end of match index. -1 if no match
    if(len(in_str)==0):
        return 0
    tdc=todo_comment(in_str)
    if(tdc!=-1):
        return tdc
    
    end= -1
    pattern = re.compile("^.*")
    for m in pattern.finditer(in_str):
        end = m.end()


    if(end!=-1):
        if end==len(in_str) or end==0:
            return end
        end=comment_content(in_str[end:])

    return end

def line_break(in_str):#matches line break from the start and returns end of match index. -1 if no match
    pattern = re.compile("^((\n\r|\r\n)|[\n\r])")
    for m in pattern.finditer(in_str):
        global total_lines_ct
        total_lines_ct+=1
        return m.end()
    return -1

def single_line_comment(in_str):#matches single line comments from the start and returns end of match index. -1 if no match
    pattern = re.compile("^\/\/")
    end=-1
    global single_line_ct, comment_lines_ct
    for m in pattern.finditer(in_str):
        end= m.end()
    if (end==-1):
        return -1

    single_line_ct+=1
    comment_lines_ct+=1
    if end==len(in_str): 

        return end

    in_str=in_str[end:]
    cc= comment_content(in_str)
    if (cc==-1):
        lb=line_break(in_str)
        if(lb==-1):

            return end

        return end+lb
    lb=line_break(in_str[cc:])
    if(lb==-1):
        lb=0

    return end + lb + cc
    

def inside_multi_line_comment(in_str):

    pattern = re.compile("^\*\/")
    for m in pattern.finditer(in_str):
        return -1

    if(len(in_str)==0):
        return 0
    mlc=multi_line_comment(in_str)
    if(mlc>0):
        return mlc
    idx=0
    td=todo(in_str)

    if(td==len(in_str)):
        return td
    if (td!=-1):
        idx=td
        

    in_str=in_str[idx:]
    lb= line_break(in_str)
    if(lb!=-1):

        return lb+idx
    if(len(in_str)==0):
        return idx
    return idx+1
        

def handle_multiline_call(in_str):
    global blocks_ct, comment_lines_block_ct, total_lines_ct, comment_lines_ct
    recorded_comments_block_ct=comment_lines_block_ct
    recorded_total_lines=total_lines_ct
    ic= inside_multi_line_comment(in_str)
    if recorded_total_lines<total_lines_ct and comment_lines_block_ct==recorded_comments_block_ct:
            comment_lines_block_ct+=1
            comment_lines_ct+=1
    recorded_comments_block_ct=comment_lines_block_ct
    recorded_total_lines=total_lines_ct
    old_ic=0;
    while(ic!=-1 and ic!=0):
        
        old_ic+=ic
        if (ic == len(in_str)):
            return old_ic
        in_str=in_str[ic:]
        ic= inside_multi_line_comment(in_str)
        
        if recorded_total_lines<total_lines_ct and comment_lines_block_ct==recorded_comments_block_ct:
            comment_lines_block_ct+=1
            comment_lines_ct+=1
        recorded_comments_block_ct=comment_lines_block_ct
        recorded_total_lines=total_lines_ct
    return old_ic

def multi_line_comment(in_str):#matches block comment from the start and returns end of match index. -1 if no match
    pattern = re.compile("^\/\*")
    end=-1
    for m in pattern.finditer(in_str):
        end= m.end()
    if (end==-1):
        return -1
    global blocks_ct, comment_lines_block_ct, total_lines_ct, comment_lines_ct
    blocks_ct+=1
    comment_lines_block_ct+=1
    comment_lines_ct+=1
    if (end==len(in_str)):        
        return end
    in_str=in_str[end:]
    hmc= handle_multiline_call(in_str)  
    if (hmc==len(in_str)):
        return hmc  
    in_str=in_str[hmc:]

    end_pt=0
    pattern = re.compile("^\*\/")
    for m in pattern.finditer(in_str):
        end_pt= m.end()
    
    return end_pt+hmc+end

def whitespace(in_str):
    pattern = re.compile("^ +")
    for m in pattern.finditer(in_str):
        return m.end()

    end=single_line_comment(in_str)

    if(end!=-1):
        return end

    end=multi_line_comment(in_str)
    if(end!=-1):
        return end    

    end=line_break(in_str)
    return end
        
def ws_opt(in_str):

    ret=0
    old_ret=0
    while(ret!=-1):
        old_ret+=ret
        ret = whitespace(in_str)
        if (ret==len(in_str)):
            return old_ret+ret
        in_str=in_str[ret:]


    return old_ret
    

def code(in_str):
    if(len(in_str)==0):
        return 0
    
    wo= ws_opt(in_str)
    if wo==len(in_str):
        return wo

    in_str= in_str[wo:]
    first_occur=sys.maxsize
    last_occur=0
    pattern = re.compile("(\/\*|\/\/|\s)")
    for m in pattern.finditer(in_str):
        if(first_occur>m.start()):
            first_occur=m.start()
        

    if first_occur==sys.maxsize:
        return len(in_str)
    
    

    ret=code(in_str[first_occur:])

    return ret+wo
    


print(code(data))

print(
" Total # of lines:",total_lines_ct,"\n",
"Total # of comment lines:",comment_lines_ct,"\n",
"Total # of single line comments:",single_line_ct,"\n",
"Total # of comment lines within block comments:",comment_lines_block_ct,"\n",
"Total # of block line comments:",blocks_ct,"\n",
"Total # of TODO's:",todo_ct,"\n",
)



