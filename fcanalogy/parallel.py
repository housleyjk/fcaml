'''
Created on Aug 25, 2011

@author: Jason
'''
import sys
from multiprocessing import Process
from krajc import find_children
from numpy import array, append
from context import Context

class Worker(Process):
    """
    Concurrent implementation of the Krajca algorithm.
    """
    def __init__(self, input, output, printer):
        self.input = input
        self.output = output
        self.printer = printer
        super(Worker, self).__init__()

    def run(self):
        while True:
            data= self.input.get()
            contexts = find_children(array([]), data.context, data.index, data.lattice, self.printer)
            contexts = append(contexts, Context(*data.context))
            self.printer.acquire()
            sys.stdout.write("Input length: %d   \r" % self.input.qsize())
            self.printer.release()
            self.output.put(contexts)
