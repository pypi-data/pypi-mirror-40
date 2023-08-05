from modelx import *
from modelx.core.cells import CellPointer

funcs = ['lx', 'dx', 'qx']

def lx(x):
    if x == 0:
        return 100000
    else:
        return lx[x - 1] - dx[x - 1]

def dx(x):
    return lx[x] * qx[x]

def qx(x):
    return 0.01


if __name__ == "__main__":
    space = new_model().new_space()

    g = globals()
    for name in funcs:
        g[name] = space.new_cells(name, g[name])

    print(lx(10))

    graph = cur_model().cellgraph

    print(graph)

    # # print(ptr in graph)
    # for i in range(10):
    #     ptr = CellPointer(lx, i)
    #     print(ptr, graph.predecessors(ptr), graph.successors(ptr))
    #
    # for i in range(10):
    #     ptr = CellPointer(dx, i)
    #     print(ptr, graph.predecessors(ptr), graph.successors(ptr))




