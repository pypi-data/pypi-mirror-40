# coding: utf-8
from nwpc_workflow_model.node_status import NodeStatus
from nwpc_workflow_model.node import Node as BaseNode


class Node(BaseNode):
    """
    Node:
        status:
            first three characters of the status word.
            unk: unknown
            sus: suspended
            com: complete
            que: queued
            sub: submitted
            act: active
            abo: aborted
            shu: shutdown
            hal: halted
    """

    def __init__(self, name='', status=NodeStatus.Unknown.value):
        BaseNode.__init__(self, name, status)
