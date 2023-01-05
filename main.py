import os
from os.path import join

import argparse
import json
import time

from tree_parser.parser_driver import ParserDriver
from codeviews.AST.AST_driver import ASTDriver
from codeviews.CFG.CFG_driver import CFGDriver
from codeviews.CST.CST_driver import CSTDriver
from codeviews.DFG.DFG_driver import DFGDriver
from codeviews.combined_graph.combined_driver import CombinedDriver

start_time = time.time()
# ----------------------------------------------------------------
parser = argparse.ArgumentParser('Experiments')
input_file = open('config.json', 'r')
config = json.load(input_file)
input_file.close()
parser.set_defaults(**config)
parser.add_argument("-fn", "--file_name", type=str,
                        help="source file name input")
parser.add_argument("-lang", "--src_language", type=str,
                        help="langauge of source file")
parser.add_argument("-cv", "--code_view", type=str,
                        help="view type of code")
parser.add_argument("-cb", "--combined", action='store_true',
                        help="combined flag")
parser.add_argument("-sc", "--save_cleaned", type=str,
                        help="save cleaned source code")
args = parser.parse_args().__dict__

print(args)

# Set the Language you want to test here
src_language = args['src_language']
# Set the test file path here
file_name = args['file_name']
# file_path = join('./code_test_files', src_language, file_name)
# file_path = join('./code_test_files/special_cases', src_language, file_name)
file_path = file_name
file_handle = open(file_path, 'r')
src_code = file_handle.read()
file_handle.close()

is_combined = args['combined']
code_view = args['code_view']
graph_format = args['graph_format']

output_dir = f"./output_graphs/{src_language}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
root_name_file = file_name.split('/')[-1].split('.')[0]
output_file = join(output_dir, f'{code_view}_{root_name_file}.{graph_format}')
print(f'Dumping graph to {output_file}')

if args['save_cleaned']:
    parser = ParserDriver(src_language, src_code)
    with open(join(args['save_cleaned'], file_name), 'w') as f:
        f.write(parser.src_code)
    print(f'Save cleaned source code')

# ----------------------------------------------------------------
if is_combined == True:
    codeviews = args['combined_views']
    print("Combined view")
    output_file = f"./output_graphs/{src_language}/combined_{root_name_file}_output"
    CombinedDriver(src_language = src_language, src_code = src_code, output_file = output_file, graph_format = graph_format, codeviews = codeviews)

# Use the following cases if you want to generate simple AST, CST, CFG or DFG without using the combined driver
else:
    if code_view == 'DFG':
        DFGDriver(src_language, src_code, output_file)
    
    elif code_view == 'CFG':
        CFGDriver(src_language, src_code, output_file)
        
    elif code_view == 'AST':
        ASTDriver(src_language, src_code, output_file)
    
    elif code_view == 'CST':
        CSTDriver(src_language, src_code)
    
    elif code_view == 'combined_graph':
        pass

    else:
        print("code_view is not supported")

    
print("\n--- Time taken: %s seconds ---\n" % (time.time() - start_time))