from nwpc_workflow_model.ecflow.ecflow_node import EcflowNode
from nwpc_workflow_model.ecflow import NodeStatus, NodeType
from nwpc_workflow_model.node_variable import NodeVariableType, NodeVariable


class TestEcflowNode(object):
    @staticmethod
    def create_node():
        node = EcflowNode()
        node.variable_list.extend([
            NodeVariable(NodeVariableType.Variable, 'self_var_1', 'self_var_1_value'),
            NodeVariable(NodeVariableType.Variable, 'var', 'var1'),
            NodeVariable(NodeVariableType.Variable, 'father_var_2', 'father_var_2_in_node'),
        ])

        node.generated_variable_list.extend([
            NodeVariable(NodeVariableType.GeneratedVariable, 'self_gen_var_1', 'self_gen_var_1_value'),
            NodeVariable(NodeVariableType.GeneratedVariable, 'var', 'var2')
        ])

        # root_node -> father_node -> node
        node.inherited_variable_list.extend([
            {
                'path': '/root/father',
                'variable_list': [
                    NodeVariable(NodeVariableType.Variable, 'father_var', 'father_var_value'),
                    NodeVariable(NodeVariableType.Variable, 'father_var_2', 'father_var_2_value'),
                    NodeVariable(NodeVariableType.Variable, 'root_var_2', 'root_var_2_value_in_father')
                ],
                'generated_variable_list': [
                    NodeVariable(NodeVariableType.Variable, 'father_gen_var', 'father_gen_var_value')
                ]
            },
            {
                'path': '/root',
                'variable_list': [
                    NodeVariable(NodeVariableType.Variable, 'root_var', 'root_var_value'),
                    NodeVariable(NodeVariableType.Variable, 'root_var_2', 'root_var_2_value')
                ],
                'generated_variable_list': [
                    NodeVariable(NodeVariableType.Variable, 'root_gen_var', 'root_gen_var_value')
                ]
            }
        ])
        return node

    def test_node_variable(self):
        node = TestEcflowNode.create_node()

        # node's variables
        assert node.get_variable_value('self_var_1') == 'self_var_1_value'
        assert node.get_variable_value('self_gen_var_1') == 'self_gen_var_1_value'

        # Variable type overrides generated Variable type.
        assert node.get_variable_value('var') == 'var1'
        assert node.get_variable('var').variable_type == NodeVariableType.Variable

        # inherited variables
        assert node.get_variable_value('father_var') == 'father_var_value'
        assert node.get_variable_value('root_var') == 'root_var_value'

        assert node.get_variable_value('father_var_2') == 'father_var_2_in_node'
        assert node.get_variable_value('root_var_2') == 'root_var_2_value_in_father'

    def test_to_dict(self):
        node = TestEcflowNode.create_node()
        node_dict = node.to_dict()

        assert len(node_dict['variable_list']) == 3
        assert len(node_dict['generated_variable_list']) == 2
        assert len(node_dict['inherited_variable_list']) == 2

    def test_create_from_dict(self):
        node_dict = {
            'name': 'node name',
            'status': NodeStatus.unknown,
            'node_type': NodeType.Suite,
            'variable_list': [
                {
                    'name': 'var name',
                    'variable_type': NodeVariableType.Variable,
                    'value': 'var value'
                }
            ],
            'generated_variable_list': [
                {
                    'name': 'gen var name',
                    'variable_type': NodeVariableType.GeneratedVariable,
                    'value': 'gen var value'
                }
            ],
            'inherited_variable_list': [
                {
                    'path': '/root/father',
                    'variable_list': [
                        {
                            'name': 'father var name',
                            'variable_type': NodeVariableType.Variable,
                            'value': 'father var value'
                        }
                    ],
                    'generated_variable_list': [
                        {
                            'name': 'father gen var name',
                            'variable_type': NodeVariableType.GeneratedVariable,
                            'value': 'father gen var value'
                        }
                    ]
                },
                {
                    'path': '/root',
                    'variable_list': [
                        {
                            'name': 'root var name',
                            'variable_type': NodeVariableType.Variable,
                            'value': 'root var value'
                        }
                    ],
                    'generated_variable_list': [
                        {
                            'name': 'root gen var name',
                            'variable_type': NodeVariableType.GeneratedVariable,
                            'value': 'root gen var value'
                        }
                    ]
                }
            ]
        }

        node = EcflowNode.create_from_dict(node_dict)

        assert node.name == node_dict['name']
        assert node.status == node_dict['status']
        assert node.node_type == node_dict['node_type']
        assert len(node.variable_list) == 1
        assert len(node.generated_variable_list) == 1
        assert len(node.inherited_variable_list) == 2
