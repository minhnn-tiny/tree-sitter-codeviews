import os
from os.path import join

import networkx as nx


def count_bug_node(graph):
    bug_nodes = 0
    for id, node in graph.nodes(data=True):
        if node['node_info_vulnerabilities'] is not None:
            bug_nodes += 1
    return bug_nodes, 100 * (bug_nodes/len(graph.nodes()))


def get_node_edge_types(graph):
    ntypes = []
    etypes = []
    for n_id, node in graph.nodes(data=True):
        if 'node_type' in node:
            ntypes.append(node['node_type'])
    for src, dst, edge in graph.edges(data=True):
        etypes.append(edge['edge_type'])
    return set(ntypes), set(etypes)


def get_number_of_nodes(nx_graph):
    nx_g = nx_graph
    number_of_nodes = {}
    for node, data in nx_g.nodes(data=True):
        if data['node_type'] not in number_of_nodes.keys():
            number_of_nodes[data['node_type']] = [0, 1]
            if data['node_info_vulnerabilities'] is not None:
                number_of_nodes[data['node_type']] = [1, 1]
            else:
                number_of_nodes[data['node_type']] = [0, 1]
        else:
            if data['node_info_vulnerabilities'] is not None:
                number_of_nodes[data['node_type']][0] += 1
            number_of_nodes[data['node_type']][1] += 1
    return number_of_nodes


if __name__ == '__main__':
    # ast_graph_dir = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/DFG'
    # ast_graph_dir = 'code_test_files/vul4j/CFG'
    # ast_graphs = [f for f in os.listdir(ast_graph_dir) if f.endswith('.dot')]
    # ntypes = []
    # etypes = []
    # for graph_file in ast_graphs:
    #     try:
    #         print(graph_file)
    #         graph = nx.nx_pydot.read_dot(join(ast_graph_dir, graph_file))
    #         for n_id, node in graph.nodes(data=True):
    #             if 'type_label' in node:
    #                 ntypes.append(node['type_label'])
    #             else:
    #                 print(n_id, node)

    #         for src, dst, edge in graph.edges(data=True):
    #             etypes.append(edge['edge_type'])
    #     except:
    #         continue
    
    # ntypes = list(set(ntypes))
    # etypes = list(set(etypes))

    # print(len(ntypes), ntypes)
    # print(len(etypes), etypes)

    # graph_file = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/buggy_curated/cleaned_cfg_compressed_graphs.gpickle'
    graph_file = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/ast_cfg/token_ast_cfg_compressed_graphs.gpickle'
    # graph_file = '/Users/minh/Documents/2022/programing_analysis/tree-sitter-codeviews/code_test_files/vul4j/cfg/cfg_compressed_graphs.gpickle'
    # graph_file = '/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/source_code/access_control/buggy_curated/cfg_compressed_graphs.gpickle'
    file_counter = {
                    'access_control': 57,
                    # 'arithmetic': 60, 'denial_of_service': 46,
                    # 'front_running': 44, 'reentrancy': 71, 'time_manipulation': 50, 
                    # 'unchecked_low_level_calls': 95
                    }
    edge = 0
    node = 0
    for bug, count in file_counter.items():
        # graph_file = f'/Users/minh/Documents/2022/smart_contract/mando/original-ge-sc/experiments/ge-sc-data/byte_code/smartbugs/runtime/gpickles/{bug}/clean_{count}_buggy_curated_0/compressed_graphs/cfg_compressed_graphs.gpickle'
        
        nx_graph = nx.read_gpickle(graph_file)
        # bug_nodes, bug_percent = count_bug_node(nx_graph)
        # print(bug_nodes, len(nx_graph), bug_percent)
        node += len(nx_graph.nodes)
        edge += len(nx_graph.edges)
        print(len(nx_graph.nodes))
        print(len(nx_graph.edges))
        # node_numbers = get_number_of_nodes(nx_graph)
        # node_types = sorted(node_numbers)
        # for node in node_types:
        #     print(node, f'{node_numbers[node][0]}/{node_numbers[node][1]}')
        ntypes, etypes = get_node_edge_types(nx_graph)
        print('ntypes: ', ntypes)
        print('etypes: ', etypes)
        # for node, data in nx_graph.nodes(data=True):
        #     print(node, data['function_fullname'])
    print(node, edge)
    print(nx_graph.nodes[10]['token'])
    print(type(nx_graph.nodes[10]['token']))
