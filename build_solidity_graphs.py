import os
from os.path import join

import networkx as nx
import json

from tree_parser.parser_driver import ParserDriver
from codeviews.AST.AST_driver import ASTDriver
from codeviews.CFG.CFG_driver import CFGDriver
from codeviews.DFG.DFG_driver import DFGDriver
from codeviews.combined_graph.combined_driver import CombinedDriver


if __name__ == '__main__':
    input_file = open('config.json', 'r')
    config = json.load(input_file)
    input_file.close()

    src_language = 'solidity'
    lang_extension = '.sol'
    # source_dir = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/arithmetic/cleaned_buggy_curated'
    source_dir = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/arithmetic/clean_60_buggy_curated_0'
    CFG_output = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/arithmetic/clean_cfg'
    
    files = [f for f in os.listdir(source_dir) if f.endswith(lang_extension)]
    files = ['buggy_25.sol']

    # AST_output = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/ast'
    # CFG_output = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/cfg'
    # DFG_output = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/dfg'
    # AST_CFG_output = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/ast_cfg'


    code_property_output = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/ast_cfg_dfg'
    cleaned_code_output = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/arithmetic/cleaned_buggy_curated'
    
    # src_language = 'java'
    # lang_extension = '.java'
    # source_dir = './code_test_files/vul4j'
    # # source_dir = './code_test_files/java'

    # files = [f for f in os.listdir(source_dir) if f.endswith('.java')]
    # # files = ['FizzBuzz.java']

    # AST_output = 'code_test_files/vul4j/ast'
    # CFG_output = 'code_test_files/vul4j/cfg'
    # DFG_output = 'code_test_files/vul4j/dfg'
    # AST_CFG_output = 'code_test_files/vul4j/ast_cfg'
    # AST_CFG_DFG_output = 'code_test_files/vul4j/ast_cfg_dfg'
    # cleaned_code_output = 'code_test_files/vul4j/cleaned_sources'

    # parser_keys = []
    for sm in files:
        print('Processing ', join(source_dir, sm))
        with open(join(source_dir, sm), 'r') as file_handle:
            src_code = file_handle.read()
        parser = ParserDriver(src_language, src_code)
        cleaned_src_code = parser.src_code
        with open(join(cleaned_code_output, sm), 'w') as f:
            f.write(cleaned_src_code)
        # print(parser.all_tokens)
        # print(parser.label)
        # print(parser.method_map)
        # print(parser.start_line)
        # parser_keys += [key[-1] for key in parser.parser.index.keys()]

    # parser_keys = set(parser_keys)
    # print(sorted(parser_keys), len(parser_keys))

        # print(parser.CFG.CFG_node_list)

        # print('Processing AST')
        # ast_driver = ASTDriver(src_language, src_code, join(AST_output, sm.replace(lang_extension, '.dot')))
        # for n_id in 
        # print(ast_driver.graph)
        
        # try:
        print('Processing CFG')
        cfg_driver = CFGDriver(src_language, src_code, join(CFG_output, sm.replace(lang_extension, '.dot')))
        # except:
        #     continue
        # print(cfg_driver.CFG.CFG_node_list)

        # print('Processing DFG')
        # dfg_driver = DFGDriver(src_language, src_code, join(DFG_output, sm.replace('.java', '.dot')))

        # try:
        #     print("Combined view")
        #     CombinedDriver(src_language = src_language, src_code = src_code, output_file = join(AST_CFG_DFG_output, sm.replace(lang_extension, '')), codeviews = config['combined_views'])
        # except:
        #     continue