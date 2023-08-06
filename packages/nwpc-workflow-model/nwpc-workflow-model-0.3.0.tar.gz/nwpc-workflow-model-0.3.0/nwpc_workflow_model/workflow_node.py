# coding: utf-8
from nwpc_workflow_model.node_status import NodeStatus
from nwpc_workflow_model.node_type import NodeType
from nwpc_workflow_model.node_variable import NodeVariable


class WorkflowNode(object):
    def __init__(self):
        self.variable_list = []
        self.generated_variable_list = []

        """
        inherited_variable_list, an array of objects as follows:
            {
                'path': node_path,
                'variable_list': Variable list,
                'generated_variable_list': generated Variable list
            }
        """
        self.inherited_variable_list = []

        self.name = ''
        self.path = None
        self.status = NodeStatus.unknown
        self.node_type = NodeType.Unknown

    def to_dict(self):
        inherited_variable_list = []
        for node in self.inherited_variable_list:
            inherited_variable_list.append({
                'path': node['path'],
                'variable_list': [var.to_dict() for var in node['variable_list']],
                'generated_variable_list': [var.to_dict() for var in node['generated_variable_list']]
            })
        return {
            'name': self.name,
            'status': self.status.name,
            'node_type': self.node_type.name,
            'variable_list': [var.to_dict() for var in self.variable_list],
            'generated_variable_list': [var.to_dict() for var in self.generated_variable_list],
            'inherited_variable_list': inherited_variable_list
        }

    @classmethod
    def create_from_dict(cls, node_dict):
        node = cls()
        node.name = node_dict['name']
        node.status = node_dict['status']
        node.node_type = node_dict['node_type']
        for a_var_dict in node_dict['variable_list']:
            a_var = NodeVariable.create_from_dict(a_var_dict)
            node.variable_list.append(a_var)
        for a_var_dict in node_dict['generated_variable_list']:
            a_var = NodeVariable.create_from_dict(a_var_dict)
            node.generated_variable_list.append(a_var)

        for a_parent in node_dict['inherited_variable_list']:
            node.inherited_variable_list.append({
                'path': a_parent['path'],
                'variable_list': [NodeVariable.create_from_dict(a_var_dict)
                                  for a_var_dict in a_parent['variable_list']],
                'generated_variable_list': [NodeVariable.create_from_dict(a_var_dict)
                                            for a_var_dict in a_parent['generated_variable_list']]
            })

        return node

    def get_variable(self, variable_name):
        for var in self.variable_list:
            if var.name == variable_name:
                return var
        for var in self.generated_variable_list:
            if var.name == variable_name:
                return var

        for node in self.inherited_variable_list:
            for var in node['variable_list']:
                if var.name == variable_name:
                    return var
            for var in node['generated_variable_list']:
                if var.name == variable_name:
                    return var
        return None

    def get_variable_value(self, variable_name):
        var = self.get_variable(variable_name)
        if var is None:
            return None
        else:
            return var.value
