#!/usr/bin/env python3

from EventEmitterPy.emitter import EventEmitter
from zenui.dom import DOM
from zenui.compiler import ZenuiCompiler

globalEmitter = EventEmitter()

htmlCompiler = ZenuiCompiler()

class ZenUIComponent:
    def __init__(self):
        self.globalEmitter = globalEmitter
        self.localEmitter = EventEmitter()
        self.dom =  DOM()
        self.render = htmlCompiler
    

