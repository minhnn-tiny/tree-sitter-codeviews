import os
from os.path import join

import networkx as nx
import pandas as pd
import json
from datasets import load_dataset

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
    # source_dir = './code_test_files/vul4j/cleaned_sources'
    # source_dir = './code_test_files/java'

    # files = [f for f in os.listdir(source_dir) if f.endswith(lang_extension)]
    # files = ['ParametersInterceptor.java']

    # AST_output = 'code_test_files/vul4j/ast'
    # CFG_output = 'code_test_files/vul4j/cfg'
    # DFG_output = 'code_test_files/vul4j/dfg'
    # AST_CFG_output = 'code_test_files/vul4j/ast_cfg'
    # AST_CFG_DFG_output = 'code_test_files/vul4j/ast_cfg_dfg'
    # cleaned_code_output = 'code_test_files/vul4j/cleaned_sources'

    bug_type = {
                'access_control': 57, 
                # 'arithmetic': 60,
                # 'denial_of_service': 46,
                # 'front_running': 44, 
                # 'reentrancy': 71,
                # 'time_manipulation': 50, 
                # 'unchecked_low_level_calls': 95
               }
    for bug, count in bug_type.items():
        # source_dir = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/buggy_curated'
        source_dir = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated'
        vul_annotation_file = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated/vulnerabilities.json'
        # output = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/ast_cfg'
        output = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/ast'
        with open(vul_annotation_file, 'r') as f:
            annoataions = json.load(f)
        new_annotations = {}
        for anno in annoataions:
            new_annotations[anno['name']] = anno
        # source_dir = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/clean_{count}_buggy_curated_0'
        CFG_output = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cfg'
        AST_CFG_output = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/ast_cfg'
        os.makedirs(AST_CFG_output, exist_ok=True)
        # CFG_output = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated'

        files = [f for f in os.listdir(source_dir) if f.endswith(lang_extension)]
        # files = ['arbitrary_location_write_simple.sol']
        cleaned_code_output = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated'
        new_line_location = {}
        methods_locations = {}
        function_data = {
            'func': [],
            'target': [],
            'project': [],
        }
        for sm in files:
            print('Processing ', join(source_dir, sm))
            with open(join(source_dir, sm), 'r') as file_handle:
                src_code = file_handle.read()
            # parser = ParserDriver(src_language, src_code)
            # cleaned_src_code = parser.src_code
            # src_code_lines = cleaned_src_code.split('\n')
            # with open(join(cleaned_code_output, sm), 'w') as f:
            #     f.write(cleaned_src_code)
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
            # print('Processing CFG')
            # cfg_driver = CFGDriver(src_language, src_code, join(CFG_output, sm.replace(lang_extension, '.dot')))

            # methods_locations[sm] = cfg_driver.CFG.records['method_locations']
            # bug_lines = new_annotations[sm]['vulnerabilities'][0]['lines'] if sm in new_annotations else []
            # for method, loc in methods_locations[sm].items():
            #     code_lines = list(range(loc[0][0]+1, loc[1][0]+2))
            #     is_vul = len(set(bug_lines) & set(code_lines)) > 0
            #     func_code = src_code_lines[loc[0][0]: loc[1][0]+1]
            #     function_data['func'].append('\n'.join(func_code))
            #     function_data['target'].append(is_vul)
            #     function_data['project'].append(sm)

        ## Push dataset to huggingface
        # output_func_dataset = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated/func_sol_dataset.csv'
        # df = pd.DataFrame.from_dict(function_data)
        # df.to_csv(output_func_dataset)
        # dataset = load_dataset('csv', data_files=output_func_dataset, split='train')
        # dataset.push_to_hub('nguyenminh871/reentrancy_solidity_function')
        # output_method_locations = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated/method_locations.json'
        # with open(output_method_locations, 'w') as f:
        #         json.dump(methods_locations, f)

            # except:
            #     continue
            # print(cfg_driver.CFG.CFG_node_list)

            # print('Processing DFG')
            # dfg_driver = DFGDriver(src_language, src_code, join(DFG_output, sm.replace('.java', '.dot')))

            print("Combined view")
            CombinedDriver(src_language = src_language, src_code = src_code, output_file = join(AST_CFG_output, sm.replace(lang_extension, '.dot')), codeviews = config['combined_views'])
            # ASTDriver(src_language, src_code, join(output, sm.replace(lang_extension, '.dot')))