

def get_first_function_body_statement(body_node, statement_types):
        function_children = list(filter(lambda child: child.type in statement_types['node_list_type'], body_node.children))
        return function_children[0] if len(function_children) > 0 else None


def get_next_node(node_value, statement_types):
    next_node = node_value.next_named_sibling
    if next_node == None:
        # Sibling not found

        current_node = node_value
        while current_node.parent is not None:
            if current_node.parent.type in statement_types['loop_control_statement']:
                next_node = current_node.parent
                if next_node.type == 'for_statement':
                    next_node = next_node.child_by_field_name('update')
                break
            next_node = current_node.next_named_sibling
            if next_node is not None:
                break
            current_node = current_node.parent

    if next_node == None:
        return 2

    if next_node.type == 'block_statement':
        for child in next_node.children:
            if child.is_named:
                next_node = child
                break
    return next_node


def get_next_index(node_indexes, node_value, statement_types):
    next_node = get_next_node(node_value, statement_types)
    if isinstance(next_node, int):
        return next_node
    return node_indexes[(next_node.start_point, next_node.end_point, next_node.type)]