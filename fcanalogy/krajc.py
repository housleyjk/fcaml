'''
Created on Aug 25, 2011
Implementatino of the Fast Close by One algorithm.

@author: Jason
'''
from context import Context

def compute_closure(context, index, lattice):
    intent = [True for x in xrange(lattice.intent_len)]
    extent = context[0] & lattice.extent_table[index]
    for e in extent: # replace with intersection function
        for j in xrange(lattice.intent_len):
            if not lattice.intent_table[e][j]:
                intent[j] = False
    return (extent, intent)

def find_children(contexts, parent, index, lattice, start=False, verbose=False):
    if start:
        pass
    else:
        if verbose:
            print "Made <",[x+1 for x in parent[0]],[lattice.intent[i] for i, b in enumerate(parent[1]) if b],'>'
        contexts.append(Context(*parent, lattice=lattice))
    if parent[1] == lattice.intent or index > lattice.intent_len:
        return contexts
    for j in xrange(index, lattice.intent_len):
        if not parent[1][j]:
            #print "Parent <", [x+1 for x in parent[0]], [i for i, b in enumerate(parent[1]) if b],'>'
            #print "On ", lattice.intent[j], "of ", [lattice.intent[x] for x in xrange(index, lattice.intent_len)]
            #print "Parent <", [x+1 for x in parent[0]], [lattice.intent[i] for i, b in enumerate(parent[1]) if b],'>'
            #print "On ", lattice.intent[j], "of ", [lattice.intent[x] for x in xrange(index, lattice.intent_len)]
            context = compute_closure(parent, j, lattice)
            skip = False
            #print "Range ", [x for x in xrange(0, j-1)]
            for k in xrange(0, j):
                if not context[1][k] == parent[1][k]:
                    skip = True
                    break
            if not skip:
                #print "Parent <", [x+1 for x in parent[0]], [lattice.intent[i] for i, b in enumerate(parent[1]) if b],'>'
                #with open('new/out', 'a') as out:
                #    out.write("<"+' '.join([lattice.extent[x].outcome for x in context[0]])+' | '+' '.join([lattice.intent[i] for i, b in enumerate(context[1]) if b])+">\n")
                    #
                #print "Made <",[x+1 for x in context[0]],[lattice.intent[i] for i, b in enumerate(context[1]) if b],'>'
                #lattice.count += 1
                #sys.stdout.write("Input length: %d  %d \r" % (lattice.count, len(context[0])))
                #if not start:
                contexts = find_children(contexts, context, j+1, lattice, verbose=verbose)
    return contexts
