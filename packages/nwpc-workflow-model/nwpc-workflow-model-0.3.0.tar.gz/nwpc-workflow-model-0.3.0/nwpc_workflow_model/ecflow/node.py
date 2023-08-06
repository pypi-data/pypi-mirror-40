# coding=utf-8
from nwpc_workflow_model.node_status import NodeStatus
from nwpc_workflow_model.node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, name='', status=NodeStatus.unknown.value):
        BaseNode.__init__(self, name, status)
