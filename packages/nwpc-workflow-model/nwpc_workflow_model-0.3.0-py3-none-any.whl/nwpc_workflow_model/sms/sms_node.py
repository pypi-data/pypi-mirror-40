# coding: utf-8
from nwpc_workflow_model.workflow_node import WorkflowNode
from nwpc_workflow_model.node_variable import NodeVariable, NodeVariableType


class SmsNode(WorkflowNode):
    def __init__(self):
        WorkflowNode.__init__(self)

    @classmethod
    def create_from_cdp_show_output(cls, cdp_output):
        # find status
        cur_line_no = 0
        line_count = len(cdp_output)

        while cur_line_no < line_count:
            line = cdp_output[cur_line_no]
            if len(line) > 0 and line.startswith('/') and not line.startswith('/-CDP'):
                break
            cur_line_no += 1
        if cur_line_no == line_count:
            return None

        # find show
        while cur_line_no < line_count:
            line = cdp_output[cur_line_no]
            if line == '\n':
                break
            cur_line_no += 1

        cur_line_no += 1
        if cur_line_no >= line_count:
            return None

        line = cdp_output[cur_line_no]
        if line[0].startswith('#'):
            return None

        start_line_no = cur_line_no

        cur_line_no += 1
        end_line_no = -1
        while cur_line_no < line_count:
            line = cdp_output[cur_line_no]
            if not line.startswith('  '):
                end_line_no = cur_line_no
                break
            cur_line_no += 1

        if end_line_no == -1:
            return None

        # get variables
        node_line = cdp_output[start_line_no: end_line_no]
        node = SmsNode()
        tokens = node_line[0].strip().split(' ')
        if len(tokens) > 5:
            node.node_type = tokens[0]
            node.name = tokens[1]
            node.status = tokens[4]

        for line in node_line[1:]:
            line = line.strip()
            if line.startswith('# genvar '):
                index = line.find(' ', 9)
                if index == -1:
                    continue
                variable_name = line[9:index]
                variable_value = line[index + 1:]
                if variable_value[0] == '\'' and variable_value[-1] == '\'':
                    variable_value = variable_value[1:-1]
                variable = NodeVariable(
                    NodeVariableType.GeneratedVariable,
                    variable_name,
                    variable_value
                )
                node.generated_variable_list.append(variable)
            elif line.startswith('edit '):
                index = line.find(' ', 5)
                if index == -1:
                    continue
                variable_name = line[5:index]
                variable_value = line[index + 1:]
                if variable_value[0] == '\'' and variable_value[-1] == '\'':
                    variable_value = variable_value[1:-1]
                variable = NodeVariable(
                    NodeVariableType.Variable,
                    variable_name,
                    variable_value
                )
                node.variable_list.append(variable)
            else:
                pass

        return node

    @classmethod
    def create_from_cdp_info_output(cls, cdp_output):
        # find status
        cur_line_no = 0
        line_count = len(cdp_output)

        while cur_line_no < line_count:
            line = cdp_output[cur_line_no]
            if len(line) > 0 and line.startswith('//'):
                break
            cur_line_no += 1
        if cur_line_no == line_count:
            return None

        node = SmsNode()

        path_line = cdp_output[cur_line_no].strip()
        path_line_tokens = path_line.split(' ')
        node_path = path_line_tokens[0]
        node.path = node_path[node_path.index('/', 2):]
        node.name = node_path[node_path.rfind('/')+1:]
        node.node_type = path_line_tokens[1][1:-1]
        node.status = path_line_tokens[-1]

        cur_line_no += 1
        while cur_line_no < line_count:
            line = cdp_output[cur_line_no]
            if line.startswith('Variables'):
                break
            cur_line_no += 1

        if cur_line_no == line_count:
            return None

        variable_start_line_no = cur_line_no = cur_line_no + 1

        while cur_line_no < line_count:
            line = cdp_output[cur_line_no]
            if not line.startswith('  '):
                break
            cur_line_no += 1
        variable_end_line_no = cur_line_no

        def get_variable_from_variable_line(variable_line, path_start):
            name_start = 0
            value_end = path_start-2
            if variable_line[0] == '(':
                variable_type = NodeVariableType.GeneratedVariable
                name_start += 1
            else:
                variable_type = NodeVariableType.Variable

            equal_index = variable_line.index('=')
            var_name = variable_line[name_start:equal_index].strip()
            var_value = variable_line[equal_index+2:value_end].strip()

            variable = NodeVariable(name=var_name, value=var_value, variable_type=variable_type)
            return variable

        for a_variable_line in cdp_output[variable_start_line_no: variable_end_line_no]:
            a_variable_line = a_variable_line.strip()
            path_start = a_variable_line.rindex('[')
            node_path = a_variable_line[path_start+1:-1]
            if len(node_path) == 0:
                variable = get_variable_from_variable_line(a_variable_line, path_start)
                if variable.variable_type == NodeVariableType.Variable:
                    node.variable_list.append(variable)
                else:
                    node.generated_variable_list.append(variable)
            else:
                if not (len(node.inherited_variable_list) > 0 and
                        node.inherited_variable_list[-1]['path'] == node_path):
                    node.inherited_variable_list.append({
                        'path': node_path,
                        'variable_list': [],
                        'generated_variable_list': []
                    })

                variable = get_variable_from_variable_line(a_variable_line, path_start)
                if variable.variable_type == NodeVariableType.Variable:
                    node.inherited_variable_list[-1]['variable_list'].append(variable)
                else:
                    node.inherited_variable_list[-1]['generated_variable_list'].append(variable)

        return node
