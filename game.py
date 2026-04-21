from collections import deque
import copy

BOARD = 9

class QuoridorState:
    def __init__(self):
        self.pos = [[4,0],[4,8]]
        self.walls = [10,10]
        self.h_walls = [[False]*8 for _ in range(8)]
        self.v_walls = [[False]*8 for _ in range(8)]
        self.turn = 0

    def clone(self):
        return copy.deepcopy(self)

    def blocked_h(self, c, r):
        if r < 0 or r >= 8: return False
        if c > 0 and self.h_walls[r][c-1]: return True
        if c < 8 and self.h_walls[r][c]: return True
        return False

    def blocked_v(self, c, r):
        if c < 0 or c >= 8: return False
        if r > 0 and self.v_walls[r-1][c]: return True
        if r < 8 and self.v_walls[r][c]: return True
        return False

    def neighbors(self, c, r, oc, or_):
        dirs = [(0,-1),(0,1),(-1,0),(1,0)]
        res = []

        for dc, dr in dirs:
            nc, nr = c+dc, r+dr
            if not (0 <= nc < 9 and 0 <= nr < 9):
                continue

            if (nc, nr) == (oc, or_):
                continue

            res.append((nc, nr))

        return res

    def legal_moves(self, p):
        c, r = self.pos[p]
        oc, or_ = self.pos[1-p]
        return self.neighbors(c,r,oc,or_)

    def bfs_dist(self, p):
        goal = 8 if p == 0 else 0
        start = tuple(self.pos[p])

        q = deque([(start,0)])
        vis = {start}

        while q:
            (c,r),d = q.popleft()
            if r == goal:
                return d

            for nc,nr in self.neighbors(c,r,0,0):
                if (nc,nr) not in vis:
                    vis.add((nc,nr))
                    q.append(((nc,nr),d+1))

        return 9999

    def place_wall(self, horiz, wc, wr):
        if horiz:
            self.h_walls[wr][wc] = True
        else:
            self.v_walls[wr][wc] = True

        
