'''
Rubik's cube solvers.
'''

import rubiks_cube as r
import rubiks_control as c


class Solver_2x2:
    '''
    Faster memory-saving brute force 2x2 rubik's cube solver. 
    '''

    def __init__(self, cube):
        '''
        Initialize the solver.
        
        Arguments:
        cube -- cube to be solved
        
        Attributes:
        face_order -- list denoting the order used to create and read string
                      representations of cubes throughout the program
        moves      -- dictionary linking the cube moves that will be used
                      throughout the program to the associated inputs
                      to the cube move_slice method and the inverse move
        scrambles  -- dictionary linking cube states from the scrambled state
                      to moves lists for reaching said states
        solves     -- dictionary linking cube states from the solved state to
                      moves lists for reaching said states
        '''
        solved = r.RubiksCube(2)
        while solved.rep.get_row('F', 0)[1] != cube.rep.get_row('F', 0)[1] or \
                solved.rep.get_row('U', 1)[1] != cube.rep.get_row('U', 1)[1] or \
                solved.rep.get_row('R', 0)[0] != cube.rep.get_row('R', 0)[0]:
            solved.random_rotations(1)
        self.face_order = ['U', 'D', 'L', 'R', 'F', 'B']
        self.moves = {"l": ['L', 0, "l'"], "l'": ['R', 1, "l"],
                      "d": ['D', 0, "d'"], "d'": ['U', 1, "d"],
                      "b": ['B', 0, "b'"], "b'": ['F', 1, "b"]}
        self.scrambles = {self.get_rep(cube): ''}
        self.solves = {self.get_rep(solved): ''}

    def get_rep(self, cube):
        '''
        Generates a compact string representation of a cube in the form 
        'uuuuddddllllrrrrffffbbbb'
        
        Arguments:
        cube -- cube to represent
        
        Return -- string representation of cube
        '''
        rep = ''
        for key in self.face_order:
            rep += cube.rep.get_row(key, 0)[0]
            rep += cube.rep.get_row(key, 0)[1]
            rep += cube.rep.get_row(key, 1)[0]
            rep += cube.rep.get_row(key, 1)[1]
        return rep

    def get_cube(self, str_rep):
        '''
        Generates a cube with the scramble specified by a string
        representation.
        
        Arguments:
        str_rep -- string representation of a cube
        
        Return -- cube with scramble represented by str_rep
        '''
        cube = r.RubiksCube(2)
        index = 0
        for face in self.face_order:
            cube.rep.set_row(face, 0, [str_rep[index], str_rep[index + 1]])
            cube.rep.set_row(face, 1, [str_rep[index + 2], str_rep[index + 3]])
            index += 4
        return cube

    def move(self, dict, str_rep, move):
        '''
        Generates a string representation and moves list for a move applied to
        a cube state in the scrambles or solves attributes.
        
        Arguments:
        dict    -- dictionary from which the cube state is sourced
        str_rep -- string representation of cube state from which to execute a
                   move
        move    -- move to execute on the cube state represented by str_rep
        '''
        cube = self.get_cube(str_rep)
        cube.move_slice(self.moves[move][0], self.moves[move][1], '+')
        return self.get_rep(cube), dict[str_rep] + move + ' '

    def next_moves(self, dict):
        '''
        Updates either scrambles or solves with the next moves.
        
        Arguments:
        dict -- dictionary to update - either scrambles or solves
        '''
        old_states = list(dict)
        for str_rep in old_states:
            for move in self.moves:
                state_moves = dict[str_rep].split()
                if len(state_moves) == 0:
                    new_state = self.move(dict, str_rep, move)
                    dict[new_state[0]] = new_state[1]
                else:
                    last_move = state_moves[len(state_moves) - 1]
                    if move != self.moves[last_move][2]:
                        new_state = self.move(dict, str_rep, move)
                        dict[new_state[0]] = new_state[1]
        for key in old_states:
            del dict[key]

    def sol_lst(self, str_scrambles, str_solves):
        '''
        Generates a list of moves from the scrambled state that results in a
        solve given moves from the scrambled and solved states that result in
        an equivalent representation.
        
        Arguments:
        str_scrambles -- string of moves from the scrambled state that results
                         in cube state A
        str_solves    -- string of moves from the solved state that results in
                         cube state A
                         
        Return -- a list of moves from the scrambled state that results in a
        solve
        '''
        moves_list = str_scrambles.split()
        str_solves = str_solves.split()[::-1]
        for move in str_solves:
            moves_list.append(self.moves[move][2])
        return moves_list

    def solve(self):
        '''
        Returns a list of moves for an optimal solve of the cube
        '''
        while True:
            for key in self.scrambles:
                if key in self.solves:
                    return self.sol_lst(self.scrambles[key], self.solves[key])
            self.next_moves(self.scrambles)
            for key in self.solves:
                if key in self.scrambles:
                    return self.sol_lst(self.scrambles[key], self.solves[key])
            self.next_moves(self.solves)


class Solver_3x3:

    def __init__(self, cube):
        '''
        Initializes a control object representing a given cube and a moves list
        
        Arguments:
        cube -- cube to be solved
        
        Attributes:
        control -- control representing cube
        moves   -- list of moves to solve the cube
        '''
        self.control = c.RubiksControl(3)
        self.control.cube.rep.set_contents(cube.rep.get_contents())
        self.moves = []

    def solve(self):
        '''
        Solves the cube.
        
        Return -- moves list
        '''
        self.solve_corners()
        self.solve_ledges(3)
        self.solve_redges(4)
        self.solve_last_ledge()
        self.match_centers_to_corners()
        self.flip_midges()
        self.place_midges()
        return self.moves

    def solve_corners(self):
        '''
        Solves the corners of the cube so that the left side is white, 
        and updates moves_list
        '''

        def w_corners_on_left():
            '''
            Checks if the corners on the left are white.
            
            Return -- boolean representing whether left corners are white.
            '''
            return self.control.cube.rep.get_row('L', 0)[0] == 'w'

        def w_centers_on_left():
            '''
            Checks if the center on the left is white.
            
            Return -- boolean representing whether left centers are white.
            '''
            return self.control.cube.rep.get_row('L', 1)[1] == 'w'

        def match_corners():
            '''
            Solves the corners relative to each other, not including centers.
            '''
            cube = r.RubiksCube(2)
            for face in cube.rep.contents:
                row_0 = self.control.cube.rep.get_row(face, 0)
                row_2 = self.control.cube.rep.get_row(face, 2)
                cube.rep.set_row(face, 0, [row_0[0], row_0[2]])
                cube.rep.set_row(face, 1, [row_2[0], row_2[2]])
            sub_solver = Solver_2x2(cube)
            for cmd in sub_solver.solve():
                self.move(cmd)

        match_corners()
        self.move_to_condition(["y", "y'", "z", "z'"], 2, \
                               w_corners_on_left)
        self.move_to_condition(["e", "e'", "s", "s'"], 2, \
                               w_centers_on_left)

    def solve_ledges(self, num):
        '''
        Solves num ledges.
        
        Arguments: 
        num -- number of ledges to solve
        '''

        def ledge_ready():
            '''
            If it exists, moves a ledge that is in proper position for a ledge
            solving algorithm to the L face and returns True. Otherwise returns
            False.
            
            Return -- boolean representing whether or not a move was made.
            '''
            alg = {('D', 0, 1, 'F', 2, 1): 'lbf',
                   ('F', 2, 1, 'D', 0, 1): 'lfb',
                   ('U', 1, 2, 'R', 0, 1): 'ltr',
                   ('R', 0, 1, 'U', 1, 2): 'lrt',
                   ('U', 1, 0, 'L', 0, 1): 'ltl'}
            for p in alg:
                if self.control.cube.rep.get_row(p[0], p[1])[p[2]] == 'w' and \
                        self.control.cube.rep.get_row(p[3], p[4])[p[5]] == \
                        self.control.cube.rep.get_row('U', 0)[0]:
                    self.move(alg[p])
                    return True
            return False

        def ledge_obstructing():
            '''
            If it exists, moves a ledge that is in a position that will never be
            in proper position for a ledge solving algorithm regardless of 
            rotation of the cube to a position that a ledge solving algorithm
            can deal with and returns True. Otherwise returns False.
            
            Return -- boolean representing whether or not a move was made.
            '''
            alg = {('L', 0, 1, 'U', 1, 0): ["u'", "m", "u"],
                   ('U', 1, 0, 'L', 0, 1): ["u'", "m", "u"]}
            for p in alg:
                if self.control.cube.rep.get_row(p[0], p[1])[p[2]] == 'w' and \
                        self.control.cube.rep.get_row(p[3], p[4])[p[5]] != \
                        self.control.cube.rep.get_row('U', 0)[0]:
                    self.move(alg[p])
                    return True
            return False

        def solve_ledge():
            '''
            Solves one ledge.
            '''
            if not self.move_to_condition( \
                    ["l", "l'"], 2, \
                    lambda: self.move_to_condition(["x", "x'"], 2, \
                                                   ledge_ready)):
                self.move_to_condition(["x", "x'"], 2, \
                                       ledge_obstructing)
                solve_ledge()

        def done():
            '''
            Determines whether or not num ledges are solved.
            
            Return -- boolean representing whether or not num ledges are solved.
            '''
            count = 0
            for p in [(0, 1, 'U'), (1, 0, 'B'), (1, 2, 'F'), (2, 1, 'D')]:
                if self.control.cube.rep.get_row('L', p[0])[p[1]] == 'w' and \
                        self.control.cube.rep.get_row(p[2], 1)[0] == \
                        self.control.cube.rep.get_row(p[2], 0)[0]:
                    count += 1
            if count >= num:
                return count
            return False

        while not done():
            solve_ledge()

    def solve_redges(self, num):
        '''
        Solves num redges.
        
        Arguments: 
        num -- number of redges to solve
        '''

        def redge_ready():
            '''
            If it exists, moves a redge that is in proper position for a redge
            solving algorithm to the R face and returns True. Otherwise returns
            False.
            
            Return -- boolean representing whether or not a move was made.
            '''
            alg = {('D', 0, 1, 'F', 2, 1): 'rbf',
                   ('F', 2, 1, 'D', 0, 1): 'rfb',
                   ('U', 1, 0, 'L', 0, 1): 'rtl',
                   ('L', 0, 1, 'U', 1, 0): 'rlt',
                   ('U', 1, 2, 'R', 0, 1): 'rtr'}
            for p in alg:
                if self.control.cube.rep.get_row(p[0], p[1])[p[2]] == 'y' and \
                        self.control.cube.rep.get_row(p[3], p[4])[p[5]] == \
                        self.control.cube.rep.get_row('U', 0)[2]:
                    self.move(alg[p])
                    return True
            return False

        def redge_obstructing():
            '''
            If it exists, moves a redge that is in a position that will never be
            in proper position for a redge solving algorithm regardless of 
            rotation of the cube to a position that a ledge solving algorithm
            can deal with and returns True. Otherwise returns False.
            
            Return -- boolean representing whether or not a move was made.
            '''
            alg = {('R', 0, 1, 'U', 1, 2): ["u", "m", "u'"],
                   ('U', 1, 2, 'R', 0, 1): ["u", "m", "u'"]}
            for p in alg:
                if self.control.cube.rep.get_row(p[0], p[1])[p[2]] == 'y' and \
                        self.control.cube.rep.get_row(p[3], p[4])[p[5]] != \
                        self.control.cube.rep.get_row('U', 0)[2]:
                    self.move(alg[p])
                    return True
            return False

        def solve_redge():
            '''
            Solves one redge.
            '''
            if not self.move_to_condition( \
                    ["r", "r'"], 2, \
                    lambda: self.move_to_condition( \
                            [["x", "l"], ["x'", "l'"]], 2, \
                            redge_ready)):
                self.move_to_condition( \
                    [["x", "l"], ["x'", "l'"]], 2, \
                    redge_obstructing)
                solve_redge()

        def done():
            '''
            Determines whether or not num redges are solved.
            
            Return -- boolean representing whether or not num redges are solved.
            '''
            count = 0
            for p in [(0, 1, 'U'), (1, 2, 'B'), (1, 0, 'F'), (2, 1, 'D')]:
                if self.control.cube.rep.get_row('R', p[0])[p[1]] == 'y' and \
                        self.control.cube.rep.get_row(p[2], 1)[2] == \
                        self.control.cube.rep.get_row(p[2], 0)[2]:
                    count += 1
            if count >= num:
                return count
            return False

        def is_pref_rot():
            '''
            Determines if the unsolved white ledge is on the U edge.
            
            Return -- boolean representing whether or not the unsolved white
            ledges is on the U edge.
            '''
            if self.control.cube.rep.get_row('L', 0)[1] != 'w' or \
                    self.control.cube.rep.get_row('U', 1)[0] != \
                    self.control.cube.rep.get_row('U', 0)[0] or done() == 4:
                return True
            return False

        self.move_to_condition(["x", "x'"], 2, is_pref_rot)
        while not done():
            solve_redge()

    def solve_last_ledge(self):
        '''
        Solves the last ledge without disturbing the fully solved right face.
        '''

        def ledge_ready():
            '''
            If it exists, moves a ledge that is in proper position for a last 
            ledge solving algorithm to the L face and returns True. Otherwise
            returns False.
            
            Return -- boolean representing whether or not a move was made.
            '''
            alg = {('U', 1, 0, 'L', 0, 1): 'ltt',
                   ('F', 2, 1, 'D', 0, 1): 'llbf',
                   ('B', 0, 1, 'D', 2, 1): 'llbb'}
            for p in alg:
                if self.control.cube.rep.get_row(p[0], p[1])[p[2]] == 'w' and \
                        self.control.cube.rep.get_row(p[3], p[4])[p[5]] == \
                        self.control.cube.rep.get_row('U', 0)[0]:
                    self.move(alg[p])
                    return True
            return False

        self.move_to_condition( \
            [["x", "l"], ["x'", "l'"]], 2, \
            ledge_ready)

    def match_centers_to_corners(self):
        '''
        Moves the L and R faces so that the corners and centers are solved.
        '''

        def centers_match_corners():
            '''
            Determines whether or not the corners and centers are solved.
            '''
            return self.control.cube.rep.get_row('F', 0)[0] == \
                   self.control.cube.rep.get_row('F', 0)[2] and \
                   self.control.cube.rep.get_row('F', 0)[0] == \
                   self.control.cube.rep.get_row('F', 1)[1]

        self.move_to_condition(["l", "l'", "r", "r'"], 4, centers_match_corners)

    def flip_midges(self):
        '''
        Flips any midges that are not in position for a place midges algorithm.
        '''

        def flip():
            '''
            If a midge is in need of flipping, flips said midge and returns
            True. Otherwise returns False.
            '''
            for p in [['o', 'r'], ['g', 'b']]:
                if self.control.cube.rep.get_row('U', 0)[1] in p and \
                        self.control.cube.rep.get_row('U', 1)[1] not in p:
                    self.move('fm')
                    return True
            return False

        while self.move_to_condition(["x", "x'"], 2, flip): pass

    def place_midges(self):
        '''
        Solves midges.
        '''

        def place():
            '''
            If midges are in position for a midge solving algorithm,
            solves said midges and returns True. Otherwise returns False.
            '''
            alg = {('g', 'b', 'r', 'o', 'b', 'g', 'r', 'o'): 'mfc',
                   ('b', 'g', 'r', 'o', 'g', 'b', 'r', 'o'): 'mbc',
                   ('g', 'g', 'r', 'r', 'b', 'b', 'o', 'o'): 'mtb',
                   ('b', 'b', 'r', 'r', 'g', 'g', 'o', 'o'): 'md'}
            for p in alg:
                if self.control.cube.rep.get_row('U', 0)[1] == p[0] and \
                        self.control.cube.rep.get_row('U', 2)[1] == p[1] and \
                        self.control.cube.rep.get_row('F', 0)[1] == p[2] and \
                        self.control.cube.rep.get_row('F', 2)[1] == p[3] and \
                        self.control.cube.rep.get_row('D', 0)[1] == p[4] and \
                        self.control.cube.rep.get_row('D', 2)[1] == p[5] and \
                        self.control.cube.rep.get_row('B', 0)[1] == p[6] and \
                        self.control.cube.rep.get_row('B', 2)[1] == p[7]:
                    self.move(alg[p])
                    return True
            return False

        def is_pref_rot():
            '''
            Rotates the cube so that the top face is green.
            '''
            return self.control.cube.rep.get_row('U', 1)[1] == 'g'

        self.move_to_condition(["x", "x'"], 2, is_pref_rot)
        i = 0
        while not self.move_to_condition(["mfc", "mbc", "mtb", "md"], i, place):
            i += 1

    def move(self, cmd):
        '''
        Applies a cmd to control, or if cmd is a list, calls move on the
        contents of the list. Updates the moves list.
        
        Arguments:
        cmd -- move to make
        '''
        if type(cmd) is str:
            self.control.do_command(cmd)
            self.moves.append(cmd)
        elif type(cmd) is list:
            for move in cmd:
                self.move(move)

    def move_to_condition(self, moves, depth, condition):
        '''
        Given a list of moves to make and a depth (how many moves to consider
        in the worst case), makes the least number of moves required to 
        achieve a condition and returns True, or returns False if this is
        impossible.
        
        Arguments:
        moves     -- list of allowed moves
        depth     -- maximum number of moves to make
        condition -- method that evaluates to a boolean
        
        Return -- boolean representing whether or not a move was made
        '''

        def permutations(list, depth):
            '''
            Returns a list of every combination of the elements of list up
            to a given depth, sorted by length.
            Ex: ['a', 'b'], 0 --> [[]]
                ['a', 'b'], 1 --> [[], ['a'], ['b']]
                ['a', 'b'], 2 --> [[], ['a'], ['b'], ['a', 'a'], ['a', 'b'], \
                                   ['b', 'a'], ['b', 'b']]
                                   
            Arguments:
            list  -- list of elements to permute
            depth -- maximum number of elements in a sublist
            '''

            def permute(list, permutation, permutations, depth):
                '''
                Helper method for permutations, does recursive work. Adds every
                combination of elements of list up to a given depth to 
                a copy of permutation, and adds this to permutations.
                
                Arguments:
                list         -- list of elements to permute
                permutation  -- a permutation of elements to which to add
                                new combinations of the elements of list
                permutations -- result list with every combination of elements
                                of list up to a given depth
                depth        -- maximum number of elements in a sublist
                '''
                permutations.append(permutation)
                if depth > 0:
                    for i in range(len(list)):
                        permute(list, permutation + [list[i]], permutations, \
                                depth - 1)

            permutations = []
            permute(list, [], permutations, depth)
            permutations.sort(key=len)
            return permutations

        orig_contents = self.control.cube.rep.get_contents()
        orig_moves = self.moves[:]
        for permutation in permutations(moves, depth):
            self.move(permutation)
            is_pref = condition()
            if is_pref:
                return True
            else:
                self.control.cube.rep.set_contents(orig_contents)
                while self.moves != orig_moves:
                    self.moves.pop(len(self.moves) - 1)
        return False


if __name__ == '__main__':
    cube = r.RubiksCube(3)
    cube.scramble()
    solver = Solver_3x3(cube)
    solver.solve()
