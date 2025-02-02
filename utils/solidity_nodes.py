from codeviews.CFG.CFG_utils import return_method_parent, return_method_signatures


def return_switch_child(node):
    """ Searches for a switch descendent in the tree and returns it"""
    if node.type == 'switch_expression':
        return node

    for child in node.children:
        t = return_switch_child(child)
        if t is not None: return t

    return None

def return_switch_parent(node, non_control_statement):
    """ Searches for a switch expression while going up the tree and returns it"""
    while node.parent is not None:
        if node.parent.type in non_control_statement:
            return node.parent
        node = node.parent
    return None


# def return_method_parent(node, method_tags):
#     if node.type in method_tags:
#         return node
#     while node.parent is not None:
#         if node.parent.type in method_tags:
#             return node.parent
#         node = node.parent
#     return None


# def return_method_signatures(method_node):
#     method_name = list(filter(lambda child : child.type == 'identifier', method_node.children))
#     parameter_list = list(filter(lambda child : child.type == '_parameter_list' or child.type == 'parameter', method_node.children))
#     method_sig = method_name[0].text.decode('UTF-8') + '(' + (parameter_list[0].text.decode('UTF-8') + ')' if len(parameter_list) > 0 else '')
#     return method_name, parameter_list, method_sig


def return_code_boundary(node):
    node_list = [node] + node.children
    start_points = [n.start_point for n in node_list]
    end_points = [n.end_point for n in node_list]
    return min(start_points, key=lambda x: x[0]), max(end_points, key=lambda x: x[0])


def return_if_root(node):
    current_node = node
    while current_node.parent.type == 'if_statement':
        current_node = current_node.parent
    return current_node


def get_nodes(root_node=None, node_list={}, graph_node_list=[], index={}, records = {}, statement_types = {}):
    """
    Returns statement level nodes recursively from the concrete syntax tree passed to it. Uses records to maintain required supplementary information. 
    noe_list maintains an intermediate representation and graph_node_list returns the final list. 
    """
    # print('Getting node list: ', root_node.type)
    # if index[(root_node.start_point,root_node.end_point,root_node.type)] in [35, 99, 174, 201, 245, 265, 307, 658, 707, 744, 771]:
    #     print(root_node)
    label = 'non label'
    code = ''
    method_node = return_method_parent(root_node, statement_types['method_type'])
    if method_node:
        method_name, para_list, method_sig = return_method_signatures(method_node, statement_types['parameter_type'])
    else:
        method_name, para_list, method_sig = '', '', ''

    if root_node.type in statement_types['node_list_type']:
        root_index = index[(root_node.start_point,root_node.end_point, root_node.type)]
    if root_node.type == 'parenthesized_expression' and root_node.parent is not None and root_node.parent.type == 'do_statement':
        label = 'while' + root_node.text.decode('UTF-8')
        type_label = 'while'
        node_list[(root_node.start_point,root_node.end_point, root_node.type)] = root_node
        # print(root_node.start_point, root_node.start_point[0], label)
        graph_node_list.append((index[(root_node.start_point,root_node.end_point,root_node.type)], root_node.start_point[0], label, type_label, '', root_node.text.decode('UTF-8')))

    elif root_node.type == 'catch_clause':
        node_list[(root_node.start_point,root_node.end_point, root_node.type)] = root_node
        catch_parameter = list(filter(lambda child : child.type == 'catch_formal_parameter', root_node.children))
        label = 'catch ('+catch_parameter[0].text.decode('UTF-8')+')'
        type_label = 'catch'
        # print(root_node.start_point, root_node.start_point[0], label)
        graph_node_list.append((index[(root_node.start_point,root_node.end_point,root_node.type)], root_node.start_point[0], label, type_label, '', root_node.text.decode('UTF-8')))

    elif root_node.type == 'finally_clause':
        node_list[(root_node.start_point,root_node.end_point, root_node.type)] = root_node
        label = 'finally'
        type_label = 'finally'
        # print(root_node.start_point, root_node.start_point[0], label)
        graph_node_list.append((index[(root_node.start_point,root_node.end_point,root_node.type)], root_node.start_point[0], label, type_label, '', root_node.text.decode('UTF-8')))

    # elif root_node.type == 'marker_annotation':
    #             print("MARKER", root_node.start_point)


    elif root_node.type in statement_types['node_list_type']:

        if root_node.type in statement_types['inner_node_type'] and root_node.parent is not None and root_node.parent.type in statement_types['outer_node_type'] and root_node.parent.child_by_field_name('body') != root_node:
            pass
            # If it has a parent and the parent is a for loop type and it is an initialization or update statement, omit it
        elif root_node.type in statement_types['inner_node_type'] and return_switch_child(root_node) is not None:
            switch_child = return_switch_child(root_node)
            child_index = index[(switch_child.start_point,switch_child.end_point,switch_child.type)]
            current_index = index[(root_node.start_point,root_node.end_point, root_node.type)]
            records['switch_child_map'][current_index] = child_index

        else:
            node_list[(root_node.start_point,root_node.end_point, root_node.type)] = root_node
            # Set default label values for the node and then modify based on node type if required in the following if-else ladder
            label = root_node.text.decode('UTF-8')
            type_label = 'expression_statement'
            

            if root_node.type == 'method_declaration' or root_node.type == 'constructor_declaration' or root_node.type == 'function_definition':
                # method_name = list(filter(lambda child : child.type == 'identifier', root_node.children))
                # parameter_list = list(filter(lambda child : child.type == 'formal_parameters' or child.type == 'formal_parameter', root_node.children))
                # label = method_name[0].text.decode('UTF-8') + (parameter_list[0].text.decode('UTF-8') if len(parameter_list) > 0 else '')
                # method_name, para_list, method_sig = return_method_signatures(root_node)

                # type_label = root_node.type
                type_label = 'function_definition'

                # print(label, root_node.start_point)
                records['method_list'][method_name[0].text.decode('UTF-8')] = index[root_node.start_point,root_node.end_point,root_node.type]
                records['method_locations'][method_name[0].text.decode('UTF-8')] = [root_node.start_point, root_node.end_point]
                graph_node_list.append((index[(root_node.start_point,root_node.end_point,root_node.type)], method_name[0].start_point[0], label, type_label, method_sig, root_node.text.decode('UTF-8')))
                # print(index[(root_node.start_point,root_node.end_point,root_node.type)], label, type_label)
            
            elif root_node.type == 'if_statement':
                root_if_node = return_if_root(root_node)
                root_if_index = index[(root_if_node.start_point,root_if_node.end_point,root_if_node.type)]
                # end_if_node = root_node.child_by_field_name('body')
                root_if_start_point, root_if_end_point = return_code_boundary(root_if_node)
                records['end_if_node'][root_if_index] = (root_if_index + len(index), root_if_start_point, root_if_end_point)
                # node_list[(root_if_start_point, root_if_end_point, 'end_if')] = end_if_node

                # print('if root node:' ,root_node)
                condition = list(filter(lambda child : child.type == 'binary_expression', root_node.children))
                # print('if statement condition: ', condition)
                if len(condition) > 0:
                    label = 'if_' + condition[0].text.decode('UTF-8')
                else:
                    label = 'if'
                type_label = 'if'
            
            elif root_node.type == 'else':
                # print('if root node:' ,root_node)
                condition = list(filter(lambda child : child.type == 'binary_expression', root_node.children))
                # print('if statement condition: ', condition)
                if len(condition) > 0:
                    label = 'if_' + condition[0].text.decode('UTF-8')
                else:
                    label = 'if'
                type_label = 'if'


            elif root_node.type == 'for_statement':
                try: 
                    init = root_node.child_by_field_name('init').text.decode('UTF-8')
                except:
                    init = ""
                try:
                    condition = root_node.child_by_field_name('condition').text.decode('UTF-8')
                except:
                    condition = ""
                try:
                    update = root_node.child_by_field_name('update').text.decode('UTF-8')
                except:
                    update = ""
                label = 'for(' + init + condition + ';' + update + ')'
                type_label = 'for'

                # Add end for node
                root_for_node = root_node
                root_for_index = index[(root_for_node.start_point,root_for_node.end_point,root_for_node.type)]
                root_for_start_point, root_for_end_point = return_code_boundary(root_for_node)
                records['end_loop_node'][root_for_index] = (root_for_index + len(index), root_for_start_point, root_for_end_point)


            elif root_node.type == 'enhanced_for_statement':
                try:
                    modifiers = str(list(filter(lambda child : child.type == 'modifiers', root_node.children)))
                    modifier = modifiers[0].text.decode('UTF-8')
                except: 
                    modifier = ""
                try: 
                    types = root_node.child_by_field_name('type').text.decode('UTF-8')
                except:
                    types = ""
                
                try:
                    variables = list(filter(lambda child : child.type == 'identifier', root_node.children))
                    variable = variables[0].text.decode('UTF-8')
                except: 
                    variable = ""
                try:
                    value = root_node.child_by_field_name('value').text.decode('UTF-8')
                except:
                    value = ""
                label = 'for(' + modifier + " "+ types + " "+ variable+ ':' + value + ')'
                type_label = 'for'

            elif root_node.type == 'while_statement':
                condition = list(filter(lambda child : child.type == 'parenthesized_expression', root_node.children))
                if len(condition) > 0:
                    label = 'while' + condition[0].text.decode('UTF-8')
                else: label = 'while'
                type_label = 'while'

                # Add end for node
                root_while_node = root_node
                root_while_index = index[(root_while_node.start_point,root_while_node.end_point,root_while_node.type)]
                root_while_start_point, root_while_end_point = return_code_boundary(root_while_node)
                records['end_loop_node'][root_while_index] = (root_while_index + len(index), root_while_start_point, root_while_end_point)

            elif root_node.type == 'do_statement':
                label = 'do'
                type_label = 'do'

            elif root_node.type == 'switch_expression':
                parent_statement  = return_switch_parent(root_node, statement_types['non_control_statement'])
                if parent_statement is not None:
                    label = parent_statement.text.decode('UTF-8').split('{')[0]
                else:
                    condition = list(filter(lambda child : child.type == 'parenthesized_expression', root_node.children))
                    label = 'switch' + condition[0].text.decode('UTF-8')
                type_label = 'switch'

            elif root_node.type == 'switch_block_statement_group' or root_node.type == 'switch_rule':
                case_label = list(filter(lambda child : child.type == 'switch_label', root_node.children))
                label = case_label[0].text.decode('UTF-8') + ':'
                type_label = 'case'

            elif root_node.type == 'try_statement' or root_node.type == 'try_with_resources_statement':
                label = 'try'
                type_label = 'try'

            elif root_node.type == 'synchronized_statement':
                condition = list(filter(lambda child : child.type == 'parenthesized_expression', root_node.children))
                label = 'synchronized ' + condition[0].text.decode('UTF-8')
                type_label = 'synchronized'
            elif root_node.type == 'labeled_statement':
                name = list(filter(lambda child : child.type == 'identifier', root_node.children))
                label = name[0].text.decode('UTF-8') + ":"
                records['label_statement_map'][label] = index[(root_node.start_point,root_node.end_point,root_node.type)]
                type_label = 'label'
            elif root_node.type == 'variable_declaration_statement' or \
                 root_node.type == 'local_variable_declaration' or \
                 root_node.type == 'state_variable_declaration' or \
                 root_node.type == 'variable_declaration':
                # label = 'new_variable'
                type_label = 'new_variable'
            elif root_node.type == 'return_statement':
                type_label = 'return'
            elif root_node.type == 'continue_statement':
                type_label = 'continue_statement'

            # show more information on graph
            label += f'\n{index[(root_node.start_point,root_node.end_point,root_node.type)]}-{type_label}-{root_node.start_point[0]+1}-{root_node.end_point[0]+1}'
            # print(root_node.start_point, root_node.start_point[0], label)
            if root_node.type != 'method_declaration' and root_node.type != 'constructor_declaration':
                graph_node_list.append((index[(root_node.start_point,root_node.end_point,root_node.type)], root_node.start_point[0], label, type_label, method_sig, root_node.text.decode('UTF-8')))
                if root_node.type == 'if_statement':
                    # graph_node_list.append((index[(end_if_node.start_point,end_if_node.end_point,end_if_node.type)], end_if_node.start_point[0], 'end_if', 'end_if', root_node.text.decode('UTF-8')))
                    graph_node_list.append((records['end_if_node'][root_if_index][0], records['end_if_node'][root_if_index][1][0], 'end_if', 'end_if', method_sig, root_node.text.decode('UTF-8')))
                elif root_node.type == 'for_statement':
                    graph_node_list.append((records['end_loop_node'][root_for_index][0], records['end_loop_node'][root_for_index][1][0], 'end_loop', 'end_loop', method_sig, root_node.text.decode('UTF-8')))
                elif root_node.type == 'while_statement':
                    graph_node_list.append((records['end_loop_node'][root_while_index][0], records['end_loop_node'][root_while_index][1][0], 'end_loop', 'end_loop', method_sig, root_node.text.decode('UTF-8')))


    for child in root_node.children:
        root_node, node_list, graph_node_list, records = get_nodes(root_node = child, node_list = node_list, graph_node_list = graph_node_list, index = index, records = records, statement_types = statement_types)

    return root_node, node_list, graph_node_list, records