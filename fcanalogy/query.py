'''
Created on Aug 25, 2011

@author: Jason
'''
import yaml
from vectors import Vector
from lattice import Lattice
import copy
class Query(yaml.YAMLObject):
    '''
    Class for managing lattice queries and generation.
    dataset: can be an array or list of vectors, or a filename leading to an ordered, comma separated datafile

    minimal_lattice: generates a new lattice constrained by the test vector and queries that lattice for the result
    run_tests: takes a sequence of test vectors and runs the specified function for each vector
    '''

    yaml_tag ="!Query"

    def __init__(self, dataset):
        if isinstance(dataset, str):
            with open(dataset) as file:
                lines = [line.split(',') for line in file.readlines()]
                dataset = [Vector(big[0].rstrip(' '), big[1].split(), big[2]) for big in lines]
        self.dataset = dataset
        self.full_lattice = None

    def minimal_lattice(self, test, verbose=False, exclude=True):
        print test
        extent = copy.deepcopy(self.dataset)
        for v in extent:
            v.intent = v.intent & test.intent
            if exclude and v.intent == test.intent:
                v.intent = set()
        lattice = Lattice(extent)
        return lattice.score_lattice(verbose=verbose)

    def complete_lattice(self):
        lattice = Lattice(self.dataset)
        lattice.build_lattice()
        return lattice

    def test_degree(self, test, verbose=False):
        extent = copy.deepcopy(self.dataset)
        for v in extent:
            v.intent = v.intent & test.intent
        lattice = Lattice(extent)
        '''
        try:
            lattice = self.lattice
        except AttributeError:
            self.lattice = Lattice(copy.deepcopy(self.dataset), verbose)
            lattice = self.lattice
        '''
        return lattice.score_similarity(verbose)

    def tagger_lattice(self, test):
        extent = copy.deepcopy(self.dataset)
        flag = False
        for v in extent:
            v.intent = v.intent & test.intent
            if v.intent: flag = True
        if flag:
            lattice = Lattice(extent)
            lattice.score_lattice()
            return lattice.get_highest_outcome()
        else:
            return False

    def run_tests(self, tests, function, **kwargs):
        return [function(test, **kwargs) for test in tests]

