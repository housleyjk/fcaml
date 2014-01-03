'''
Created on Aug 1, 2011

@author: Jason
'''
import yaml
from krajc import find_children
from vectors import Vector

class Lattice(yaml.YAMLObject):
    '''
    Galois lattice class using the Krajca algorithm to find the concepts and the iPred algorithm to calculate the hasse connections.
    It also contains some utility functions for performing Analogical Modeling on the lattice.
    '''
    yaml_tag = "!Lattice"

    def __init__(self, extent, verbose=False):
        #lattice intents and extents are for the whole lattice, so they are the complete set of all attributes and objects respectively

        if verbose:
            print "Initializing lattice "
            self.extent = extent
            self.extent_len = len(extent)
            print "Extent length ", self.extent_len
            self.intent = list(frozenset().union(*[v.intent for v in extent]))
            self.intent_len = len(self.intent)
            print "Intent length ", self.intent_len
            print "Compiling Tables "
            self.extent_table = [frozenset([inde for inde, v in enumerate(extent) if i in v.intent]) for i in self.intent]
            self.intent_table = [[(i in v.intent) for i in self.intent] for v in self.extent]
            print "Finished initializing lattice "
            self.count = 0
            self.contexts = {}
        else:
            self.extent = extent
            self.extent_len = len(extent)
            self.intent = list(frozenset().union(*[v.intent for v in extent]))
            self.intent_len = len(self.intent)
            self.extent_table = [frozenset([inde for inde, v in enumerate(extent) if i in v.intent]) for i in self.intent]
            self.intent_table = [[(i in v.intent) for i in self.intent] for v in self.extent]
            self.count = 0
            self.contexts = {}

    def make_hasse(self, contexts, verbose=False):
        #This uses the improved Valtchev iPred border algorithm
        contexts.sort(key=lambda x: len(x.intent))
        border = set()
        #if verbose:
            #print contexts
        for context in contexts:
            self.contexts[context.intent] = context # I should be able to use either the intent or a set of the extent
            intents = set()
            for b in border:
                intents.add(frozenset(b.intent & context.intent))
            for i in intents:
                if not self.contexts[i].faces & context.intent:
                    parent = self.contexts[i]
                    parent.children.add(context)
                    context.parents.add(parent)
                    parent.faces |= context.intent - parent.intent
            border -= context.parents
            border.add(context)
        return contexts

    def build_lattice(self, verbose=False):
        top = (frozenset([ind for ind, v in enumerate(self.extent)]), [0 for i in self.intent])
        tops = find_children([], top, 0, self, False, verbose=verbose)
        contexts = self.make_hasse(tops, verbose=verbose)
        return contexts

    def make_concepts_only(self):
        top = (frozenset([ind for ind, v in enumerate(self.extent)]), [0 for i in self.intent])
        find_children([], top, 0, self, False)

    def make_vectors_from_lattice(self):
        return [Vector('|'.join(frozenset([self.extent[e].outcome for e in self.contexts[c].extent])),
                       [self.intent[int(i)] for i in self.contexts[c].intent],
                       str(self.contexts[c].intent),
                       ordered=False) for c in self.contexts if len(self.contexts[c].extent) > 1] #make sure to exclude the universal context

    def compare_lattice(self, lattice, type='extent'):
        if type == 'extent':
            lattice_one = {}
            for c in self.contexts: lattice_one[frozenset(self.contexts[c].extent)] = self.contexts[c]
            lattice_two = {}
            for c in lattice: lattice_two[frozenset(lattice[c].extent)] = lattice[c]
            #print "L1 ", frozenset(lattice_one.keys())
            #print "L2 ", frozenset(lattice_two.keys())
            return frozenset(lattice_one.keys()) == frozenset(lattice_two.keys())

    def score_lattice(self, verbose=False, all=False):
        for c in self.build_lattice(verbose=verbose)[::-1]:
            c.score_vectors()
        self.outcomes = set(v.outcome for v in self.extent)
        verbose = True
        if verbose:
            for o in self.outcomes:
                if sum([v.score for v in self.extent if v.outcome == o]):
                    print o,'\t', sum([v.score for v in self.extent if v.outcome == o]),'\t', '%f' % (sum([v.score for v in self.extent if v.outcome == o])/float(sum([v.score for v in self.extent])))#, [v for v in self.extent if v.outcome == o and v.intent]
                elif all:
                    print o, '%f' % (sum([v.score for v in self.extent if v.outcome == o])/float(sum([v.score for v in self.extent])))
            print '-' * 50
        return self.outcomes

    def score_similarity(self, verbose=False):
        degree = 0
        for c in self.build_lattice()[::-1]:
            if len(c.extent):
                if len(c.intent) >= degree:
                    degree = len(c.intent)
                else:
                    break
        return degree

    def get_highest_outcome(self):
        possible = []
        for o in self.outcomes:
            possible.append((o, sum([v.score for v in self.extent if v.outcome == o])))
        possible.sort(key=lambda x: x[1], reverse=True)
        return (possible[0][0], possible[0][1]/float(sum([v.score for v in self.extent])))



