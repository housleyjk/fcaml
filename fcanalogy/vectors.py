'''
Created on Aug 25, 2011

@author: Jason
'''
import yaml


class Vector(yaml.YAMLObject):
    '''
   Yaml representation of an Analogical Modeling style vector.
    '''
    yaml_tag = "!Vector"
    def __init__(self, outcome, variables, notes='', ordered=True, ignore="="):
        '''
        '''
        self.outcome = outcome
        self.variables = variables
        self.notes = notes
        self.score = 0
        if not ordered:
            self.intent = frozenset([str(v) for v in variables if not str(v) == ignore])
        else:
            self.intent = frozenset([str(ind)+'_'+str(v) for ind, v in enumerate(variables) if not str(v) == ignore])

    def save(self):
        return self.outcome+' , '+' '.join(self.variables)+' , '+''.join(self.notes)+'\n'

    def __repr__(self):
        return "Vector <"+self.outcome+', '+self.notes.rstrip('\r\n')+' | '+' '.join(self.intent)+">"
