from copy import deepcopy
from Queue import PriorityQueue
import sys

sys.setrecursionlimit(10000)

class Visit(object):
    def __init__(self, grid, prev, node, color, f):
        self._grid = grid
        self._prev = prev
        self._next = None
        self.node = node
        self.color = color
        self.f = f
        
    def _backtrack(self, save):
        if self._prev:
            steps = self._prev._backtrack(save)
            steps.append(self)
        else:
            steps = [self]
        if save:
            self._grid._save(self)
        return steps
        
    def path(self, save=False):
        return self._backtrack(save)
        
    def save(self):
        self._backtrack(True)
    
    @property
    def direction(self):
        if self._prev == None and self._next == None:
            return 'none'
        elif self._prev == None:
            if self._next.node[0] == self.node[0]:
                return 'horizontal'
            elif self._next.node[1] == self.node[1]:
                return 'vertical'
        elif self._next == None:
            if self._prev.node[0] == self.node[0]:
                return 'horizontal'
            elif self._prev.node[1] == self.node[1]:
                return 'vertical'
        else:
            if self._prev.node[0] == self.node[0] and self._next.node[0] == self.node[0]:
                return 'horizontal'
            elif self._prev.node[1] == self.node[1] and self._next.node[1] == self.node[1]:
                return 'vertical'
            else:
                return 'both'
                
    def move(self, node):
        f = self.f+10
        if self.direction == 'none' and self.node[0] == node[0]:
            # First direction.
            pass
            #f = self.f+10
        elif self.direction == 'horizontal' and self.node[0] == node[0]:
            # Staying horizontal
            #f = self.f+10
            pass
        elif self.direction == 'vertical' and self.node[1] == node[1]:
            # Staying vertical
            #f = self.f+10
            pass
        else:
            # Changing direction frm horizontal
            if self.direction == 'horizontal':
                f += 50
        visit = Visit(self._grid, self, node, self.color, f)
        # Penalty for vertical far from center
        if visit.direction == 'vertical':
            visit.f += abs(visit.node[1])*5
        return visit
    
    def show(self):
        path = self.path()
        for step in path:
            print step.node, step.direction, step.f
                     
    def options(self):
        current = self.node
        moves = [
            (current[0]-1, current[1]),
            (current[0]+1, current[1]),
            (current[0], current[1]-1),
            (current[0], current[1]+1)
        ]
        for node in moves:
            if node not in self._grid._grid.keys():
                continue
            visit = self.move(node)
            if visit.direction not in self._grid.directions(node):
                yield visit
            else:
                possible = True
                for item in self._grid._grid[node]:
                    if visit.direction == item.direction and visit.color != item.color:
                        possible = False
                        break
                if possible:
                    yield visit
    
    def g(self, node):
        g = self.f
        g += abs(self.node[0] - node[0])*11
        g += abs(self.node[1] - node[1])*11
        return g

class Grid(object):
    def __init__(self, rows, columns=None):
        self.rows = rows
        self.columns = columns or rows
        self._grid = self._build()

    def _build(self):
        grid = {}
        grid[(0,0)] = []
        for row in range(self.rows+1):
            for column in range(self.columns+1):
                grid[(row,column)] = []
                grid[(-row,-column)] = []
                grid[(-row,column)] = []
                grid[(row,-column)] = []
        return grid
                
    def _save(self, item):
        self._grid[item.node].append(item)
        
    def directions(self,node):
        d = set()
        for node in self._grid[node]:
            d.add(node.direction)
            if node._prev:
                d.add(node._prev.direction)
        return d
    
    def start(self, row, column, color):
        return Visit(self, None, (row, column), color, 0)
        
    def show(self):
        for row in range(-self.rows, self.rows+1):
            for column in range(-self.columns, self.columns+1):
                nodes = self._grid[(row, column)]
                if nodes:
                    print nodes[0].color,
                else:
                    print ' ',
            print

class Solver(object):
    def __init__(self, rows, columns=None):
        self.grid = Grid(rows, columns)
        
    def solve(self, start, end, color=0):
        if start not in self.grid._grid:
            raise ValueError('Start not in grid range.')
        if end not in self.grid._grid:
            raise ValueError('End not in grid range.')
        self.openset = PriorityQueue()
        self.closedset = PriorityQueue()
        self.visited = set()
        visit = self.grid.start(start[0], start[1], color)
        self.visited.add(visit.node)
        self.openset.put((visit.g(end), visit))
        return self._iterate(end)
        
    def _iterate(self, end):
        moved = False
        _, visit = self.openset.get()
        self.closedset.put((visit.f, visit))
        for move in visit.options():
            if move.node in self.visited:
                continue
            self.visited.add(move.node)
            moved = True
            if move.node == end:
                return move
            self.openset.put((move.g(end), move))
        if not moved and self.openset.empty():
            print self.openset
            print self.closedset
            raise ValueError('No solution found.')
        return self._iterate(end)
        
class Graph(object):
    def __init__(self, context):
        self.data = context['energy']
        self.categories = set(
            [item for item in[self.data[key] for key in self.data.keys()]]
        )
        self.fellows = self.data.keys()
        self.solver = Solver(len(self.fellows) * len(self.categories))

if __name__ == '__main__':
    from context import context
    import pprint
    g = Graph(context)
    g.build()
    pprint.pprint(s.grid)
