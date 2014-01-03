'''
Created on Aug 25, 2011

@author: Jason
'''
import yaml

def intent_representer(dumper, data):
    return dumper.represent_scalar(u'!Intent', u'%s' % data)

def intent_constructor(loader, node):
    value = loader.construct_scalar(node)
    l = value.split(":")
    return Intent(l)

class Intent(frozenset):
    '''
    classdocs
    '''
    def __repr__(self):
        return "(["+':'.join(self)+"])"
        #return '<Intent-'+':'.join(self)+'>'

yaml.add_representer(Intent, intent_representer)
yaml.add_constructor(u"!Intent", intent_constructor)