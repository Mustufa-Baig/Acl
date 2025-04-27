import sys
from Scripts import error_checker
from Scripts import pre_loader
from Scripts import runner
from Scripts import parser

code=""

# Read the code into memory
try:
    # Load file from cli input
    with open(sys.argv[1],'r') as file:
        code=file.read()
    with open("last.txt",'w') as l:     
        l.write(sys.argv[1])
    print("<Running ",sys.argv[1],">")
    
except:
    try:
        # try to Load last read file
        with open("last.txt",'r') as l:
            fname=l.readlines()[0]
            with open(fname,'r') as file:
                code=file.read()
            print("< Running ",fname,">")
    except:
        # return an error
        print("Error: No input file given")
        print("\n<Program execution terminated>")
        sys.exit()


code,v_temp=parser.extract_code(code)
syn_err=error_checker.check_syntax_errors(code)
typ_err=error_checker.check_type_errors(code,v_temp)
if len(syn_err)>0:
    print("SYNTAX ERROR")
    print(syn_err)
    
if len(typ_err)>0:
    print("TYPE ERROR")
    print(typ_err)

if len(syn_err)==0 and len(typ_err)==0:
    conditionals=pre_loader.cache_conditional_jumps(code)
    gt_positions=pre_loader.cache_goto_jumps(code,conditionals)

    runner.run(code,gt_positions,conditionals)


    
end=input("\n<Program executed>\n<Press 'Enter' to exit>")
