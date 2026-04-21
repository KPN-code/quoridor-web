from collections import deque

BOARD = 9

class QuoridorState:
    def __init__(self):
        self.pos = [[4,0],[4,8]]
        self.walls = [10,10]
        self.h_walls = [[False]*8 for _ in range(8)]
        self.v_walls = [[False]*8 for _ in range(8)]
        self.turn = 0

    # ── clone (nopeampi kuin deepcopy) ─────────────────────────────
    def clone(self):
        s = QuoridorState()
        s.pos = [p[:] for p in self.pos]
        s.walls = self.walls[:]
        s.h_walls = [row[:] for row in self.h_walls]
        s.v_walls = [row[:] for row in self.v_walls]
        s.turn = self.turn
        return s

    # ── seinäblokit ────────────────────────────────────────────────
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

    # ── liikkeet + hypyt ───────────────────────────────────────────
    def neighbors(self, c, r, oc, or_):
        dirs = [(0,-1),(0,1),(-1,0),(1,0)]
        res = []

        for dc, dr in dirs:
            nc, nr = c+dc, r+dr

            if not (0 <= nc < BOARD and 0 <= nr < BOARD):
                continue

            # seinä estää
            if dr == -1 and self.blocked_h(c, r-1): continue
            if dr ==  1 and self.blocked_h(c, r):   continue
            if dc == -1 and self.blocked_v(c-1, r): continue
            if dc ==  1 and self.blocked_v(c, r):   continue

            # jos vastustaja edessä → hyppy
            if (nc, nr) == (oc, or_):
                jc, jr = nc+dc, nr+dr

                jump_ok = (0 <= jc < BOARD and 0 <= jr < BOARD)

                if jump_ok:
                    if dr == -1 and self.blocked_h(nc, nr-1): jump_ok = False
                    if dr ==  1 and self.blocked_h(nc, nr):   jump_ok = False
                    if dc == -1 and self.blocked_v(nc-1, nr): jump_ok = False
                    if dc ==  1 and self.blocked_v(nc, nr):   jump_ok = False

                if jump_ok:
                    res.append((jc, jr))
                else:
                    # viistohypyt
                    for sdc, sdr in dirs:
                        if (sdc, sdr) == (dc, dr): continue
                        sc, sr = nc+sdc, nr+sdr

                        if not (0 <= sc < BOARD and 0 <= sr < BOARD):
                            continue

                        if sdr == -1 and self.blocked_h(nc, nr-1): continue
                        if sdr ==  1 and self.blocked_h(nc, nr):   continue
                        if sdc == -1 and self.blocked_v(nc-1, nr): continue
                        if sdc ==  1 and self.blocked_v(nc, nr):   continue

                        res.append((sc, sr))
            else:
                res.append((nc, nr))

        return res

    def legal_moves(self, p):
        c, r = self.pos[p]
        oc, or_ = self.pos[1-p]
        return self.neighbors(c, r, oc, or_)

    # ── BFS ───────────────────────────────────────────────────────
    def bfs_dist(self, p):
        goal = 8 if p == 0 else 0
        start = tuple(self.pos[p])
        opp = tuple(self.pos[1-p])

        q = deque([(start,0)])
        vis = {start}

        while q:
            (c,r),d = q.popleft()
            if r == goal:
                return d

            for nc,nr in self.neighbors(c, r, opp[0], opp[1]):
                if (nc,nr) not in vis:
                    vis.add((nc,nr))
                    q.append(((nc,nr),d+1))

        return 9999

    def has_path(self, p):
        return self.bfs_dist(p) < 9999

    # ── seinän validointi ─────────────────────────────────────────
    def can_place_wall(self, horiz, wc, wr):
        if not (0 <= wc < 8 and 0 <= wr < 8):
            return False

        if horiz:
            if self.h_walls[wr][wc]: return False
            if self.v_walls[wr][wc]: return False
            self.h_walls[wr][wc] = True
        else:
            if self.v_walls[wr][wc]: return False
            if self.h_walls[wr][wc]: return False
            self.v_walls[wr][wc] = True

        ok = self.has_path(0) and self.has_path(1)

        # rollback
        if horiz:
            self.h_walls[wr][wc] = False
        else:
            self.v_walls[wr][wc] = False

        return ok

    def place_wall(self, horiz, wc, wr):
        if not self.can_place_wall(horiz, wc, wr):
            return False

        if horiz:
            self.h_walls[wr][wc] = True
        else:
            self.v_walls[wr][wc] = True

        self.walls[self.turn] -= 1
        return True

    # ── voittaja ─────────────────────────────────────────────────
    def winner(self):
        if self.pos[0][1] == 8: return 0
        if self.pos[1][1] == 0: return 1
        return None
