import random

class AI:
    # Kuinka syvälle minimax käy pelipuussa
    MAX_DEPTH = 3

    def choose(self, state):
        """
        Pääfunktio:
        - käy kaikki mahdolliset siirrot
        - simuloi ne
        - valitsee parhaan minimax-arvion perusteella
        """

        best_val = -9999   # paras löydetty arvo
        best_move = None    # paras siirto

        # Käydään läpi kaikki AI:n mahdolliset siirrot
        for move in self._all_moves(state, 1):

            # Simuloidaan siirto (AI = pelaaja 1)
            child = self._apply(state, move, 1)

            # Arvioidaan siirto minimaxilla
            val = self._minimax(child, self.MAX_DEPTH - 1, False)

            # Tallennetaan paras siirto
            if val > best_val:
                best_val = val
                best_move = move

        return best_move


    def _minimax(self, state, depth, maximizing):
        """
        Minimax-algoritmi:
        - maximizing = AI yrittää maksimoida tulosta
        - muuten vastustaja yrittää minimoida
        """

        # Tarkistetaan pelin lopputila
        winner = state.winner()

        # AI voitti
        if winner == 1:
            return 1000

        # AI hävisi
        if winner == 0:
            return -1000

        # Syvyys loppui → käytetään heuristiikkaa
        if depth == 0:
            return self._heuristic(state)

        # Valitaan kuka pelaa tässä solmussa
        player = 1 if maximizing else 0

        # Kaikki mahdolliset siirrot
        moves = self._all_moves(state, player)

        if maximizing:
            # AI yrittää saada mahdollisimman suuren arvon
            best = -9999

            for move in moves:
                child = self._apply(state, move, player)
                val = self._minimax(child, depth - 1, False)
                best = max(best, val)

            return best

        else:
            # Vastustaja yrittää minimoida AI:n tulosta
            best = 9999

            for move in moves:
                child = self._apply(state, move, player)
                val = self._minimax(child, depth - 1, True)
                best = min(best, val)

            return best


    def _heuristic(self, state):
        """
        Arvio pelitilasta (ei etsi loppuun asti)

        Idea:
        - mitä pienempi etäisyys AI:lla maaliin → hyvä
        - mitä suurempi etäisyys vastustajalla → hyvä
        """

        d_player = state.bfs_dist(0)  # ihmispelaaja
        d_ai = state.bfs_dist(1)      # AI

        # Positiivinen = hyvä AI:lle
        return d_player - d_ai


    def _all_moves(self, state, player):
        """
        Generoi kaikki mahdolliset siirrot:
        1. nappulaliikkeet
        2. seinäliikkeet (jos jäljellä)
        """

        moves = []

        # ── 1. Nappulaliikkeet ─────────────────────
        for c, r in state.legal_moves(player):
            moves.append(("move", c, r))

        # ── 2. Seinät ──────────────────────────────
        if state.walls[player] > 0:

            wall_moves = []

            # kaikki mahdolliset seinäpaikat
            for wr in range(8):
                for wc in range(8):
                    for horiz in [True, False]:

                        # tarkistetaan onko laillinen
                        if state.can_place_wall(horiz, wc, wr):
                            wall_moves.append(("wall", horiz, wc, wr))

            # nopeutus: jos liian monta → otetaan satunnaisotos
            if len(wall_moves) > 20:
                wall_moves = random.sample(wall_moves, 20)

            moves.extend(wall_moves)

        return moves


    def _apply(self, state, move, player):
        """
        Simuloi siirto ilman että oikea pelitila muuttuu
        (tärkeää minimaxille)
        """

        # kopioidaan tila (ettei rikota alkuperäistä)
        new_state = state.clone()

        # nappulasiirto
        if move[0] == "move":
            _, c, r = move
            new_state.pos[player] = [c, r]

        # seinäsiirto
        else:
            _, horiz, wc, wr = move
            new_state.place_wall(horiz, wc, wr)

        # vaihdetaan vuoro
        new_state.turn = 1 - player

        return new_state