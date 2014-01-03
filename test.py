'''
Created on Aug 25, 2011

@author: Jason
'''
from fcanalogy import Query, Vector, Lattice

if __name__ == '__main__':
    query = Query('fcanalogy/resources/data-aan') # load the data set "data-main"
    with open('fcanalogy/resources/test-aan') as file: # open the test file
        lines = [line.split(',') for line in file.readlines()] # parse test items
        vectors = [Vector(big[0].rstrip(' '), big[1].split(), big[2]) for big in lines] # format test items
    query.run_tests(vectors, query.minimal_lattice) # run classical AM (minimal lattice) with kracj algorithm
    #l = Lattice([Vector("0", ["A", "C", "F", "H"], ordered=False),
                 #Vector("0", ["A", "C", "G", "I"], ordered=False),
                 #Vector("0", ["A", "D", "G", "I"], ordered=False),
                 #Vector("0", ["B", "C", "F", "H"], ordered=False),
                 #Vector("0", ["B", "E", "G"], ordered=False) ])
    #import cProfile as prof
    #prof.run("for x in xrange(0, 10000): l.make_concepts_only()")
