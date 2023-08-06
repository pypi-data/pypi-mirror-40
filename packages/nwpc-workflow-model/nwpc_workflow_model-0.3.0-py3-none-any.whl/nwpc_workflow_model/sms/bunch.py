# coding=utf-8
from nwpc_workflow_model.bunch import Bunch as BaseBunch
from .node import Node, NodeStatus


class Bunch(BaseBunch):
    def __init__(self):
        BaseBunch.__init__(self)
        self.parent = None
        self.children = list()
        self.name = ''
        self.status = NodeStatus.Unknown
