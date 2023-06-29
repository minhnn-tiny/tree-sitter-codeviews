import os
from os.path import join

import json


if __name__ == '__main__':

    bug_list = [
                'access_control',
                # 'arithmetic',
                # 'denial_of_service',
                # 'front_running',
                # 'reentrancy',
                # 'time_manipulation',
                # 'unchecked_low_level_calls'
                ]
    for bug in bug_list:
    # Loading original annotations ========================================================

        org_annotation_buggy = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/data/solidifi_buggy_contracts/{bug}/vulnerabilities.json'
        org_annotation_curated = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/data/smartbug-dataset/vulnerabilities.json'
        with open(org_annotation_buggy, 'r') as f:
            buggy_anno = json.load(f)
        with open(org_annotation_curated, 'r') as f:
            curated_anno = json.load(f)
        total_anno = buggy_anno + curated_anno
        anno_dict = {}
        for anno in total_anno:
            anno_dict[anno['name']] = anno

        # org_annotation = 'code_test_files/vul4j/vulnerabilities.json'
        # with open(org_annotation, 'r') as f:
        #     total_anno = json.load(f)
        # anno_dict = {}
        # for anno in total_anno:
        #     anno_dict[anno['name']] = anno
    #==========================================================================


    # Get source codes ========================================================

        source_dir = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/buggy_curated'
        cleaned_source_dir = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated'
        sol_files = [f for f in os.listdir(source_dir) if f.endswith('.sol')]
        # sol_files = ['buggy_39.sol']
        # source_dir = 'code_test_files/vul4j/'
        # cleaned_source_dir = 'code_test_files/vul4j/cleaned_sources'
        # sol_files = [f for f in os.listdir(source_dir) if f.endswith('.java')]
    #==========================================================================

        org_src_locations = {}
        cleaned_src_locations = {}
        cleaned_annotions = []
        for sm in sol_files:
            print(sm)
            with open(join(source_dir, sm), 'r') as file_handle:
                org_src_code = file_handle.read()
            for id, line in enumerate(org_src_code.split('\n')):
                org_src_locations[id + 1] = line
            with open(join(cleaned_source_dir, sm), 'r') as file_handle:
                cleaned_src_code = file_handle.read()
            for id, line in enumerate(cleaned_src_code.split('\n')):
                cleaned_src_locations[id + 1] = line


            anno = {}
            anno['name'] = sm
            anno['path'] = join('code_test_files/vul4j/cleaned_sources', sm)
            anno['source'] = anno_dict[sm]['source']
            anno['vulnerabilities'] = []
            vuls = anno_dict[sm]['vulnerabilities']
            for vul in vuls:
                new_location = {'lines': [], 'category': vul['category']}
                lines = sorted(vul['lines'])
                current_line = 0
                # print(vul)
                for l in lines:
                    org_code = org_src_locations[l]
                    for ln, code in cleaned_src_locations.items():
                        if code.rstrip() == org_code.split('//')[0].rstrip() and ln > current_line and org_code.rstrip() != "":
                            # print(l, ln)
                            # print(code.rstrip())
                            # print(org_code.rstrip())
                            new_location['lines'].append(ln)
                            current_line = ln
                            break
                new_location['lines'] = sorted(new_location['lines'])
                anno['vulnerabilities'].append(new_location)
            cleaned_annotions.append(anno)
        
        cleaned_annotation_output = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/{bug}/cleaned_buggy_curated/vulnerabilities.json'

        # cleaned_annotation_output = 'code_test_files/vul4j/cleaned_sources/vulnerabilities.json'
        with open(cleaned_annotation_output, 'w') as f:
            json.dump(cleaned_annotions, f, indent=4)
