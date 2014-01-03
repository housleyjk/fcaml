'''
Created on Aug 25, 2011

@author: Jason
'''
import yaml
from intent import Intent


class Context(yaml.YAMLObject):
    """
    Analogical context class. This is where most of the essential steps
    in calculating the analogical set are made.

    """

    yaml_tag = "!Vector"
    def __init__(self, extent, intent, lattice=None):
        self.extent = extent
        self.intent = Intent([str(ind) for ind, e in enumerate(intent) if e])
        self.lattice = lattice
        self.parents = set()
        self.children = set()
        self.faces = set()
        self._active = True

    def get_empty(self):
        #empty is the number of expected subcontexts minus the number of actual occuring subcontexts
        try:
            return self._empty
        except AttributeError:
            self._empty = 2**len(self.intent) - (sum([p.empty for p in self.ancestors])+len(self.ancestors)+1) #this is the most important contribution from Jason
            #print self, self._empty
            return self._empty

    def get_ancestors(self):
        try:
            return self._ancestors
        except AttributeError:
            _ancestors = set(self.parents)
            for p in self.parents: _ancestors |= p.ancestors
            self._ancestors = _ancestors
            return self._ancestors

    def is_homogeneous(self):
        try:
            return self._homogeneous
        except AttributeError:
            self._homogeneous = True
            incoming = set()
            for c in self.children:
                incoming |= set([self.lattice.extent[v].outcome for v in c.extent])
                if len(incoming) > 1:
                    self._homogeneous = False
                    break
            if incoming and not incoming == set([self.lattice.extent[v].outcome for v in self.extent]):
                self._homogeneous = False
            #print "Homo ", self, self._homogeneous
            return self._homogeneous

    def get_active(self):
        return self._active

    def set_active(self, value):
        if self._active: #this means only False values affect the whole tree
            self._active = value
            for p in self.parents: p.active = value

    def score_vectors(self):
        if self.active:
            if self.homogeneous:
                for v in self.extent:
                    #print "Got ", self.lattice.extent[v], " with current ", self.lattice.extent[v].score,
                    self.lattice.extent[v].score += len(self.extent) * (self.empty + 1)
                    #print " now ", self.lattice.extent[v].score
            else:
                self.active = False
                #for a in self.parents: a.active = False
                #print 50 * '-'
                #for v in self.lattice.contexts: print self.lattice.contexts[v], self.lattice.contexts[v].active
                #print 50 * '-'


    def get_tuple(self):
        return (self.extent, self.intent)

    def __repr__(self):
        return "<"+' '.join([str((self.lattice.extent[x].outcome)) for x in self.extent])+' | '+' '.join([self.lattice.intent[int(i)] for i in self.intent])+">"
    #, self.lattice.extent[x].notes

    homogeneous = property(is_homogeneous)
    empty = property(get_empty)
    ancestors = property(get_ancestors)
    active = property(get_active, set_active)

