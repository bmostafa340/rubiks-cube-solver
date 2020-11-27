'''
Rubik's cube class.
'''

import copy
import random

import rubiks_rep as r


class InvalidCube(Exception):
    '''
    This exception is raised when a cube has been determined to be in
    an invalid configuration.
    '''
    pass


class RubiksCube:
    '''
    This class implements all Rubik's cube operations.
    '''

    def __init__(self, size):
        '''Initialize the cube representation.'''
        # Cube representation.
        self.rep = r.RubiksRep(size)
        # Number of moves, quarter-turn metric.
        self.count = 0

    def get_state(self):
        '''
        Return a copy of the internal state of this object.
        '''
        rep = copy.deepcopy(self.rep)
        return rep, self.count

    def put_state(self, rep, count):
        '''
        Restore a previous state.
        '''
        self.rep = rep
        self.count = count

    ### Basic operations.

    def rotate_cube(self, axis, dir):
        '''
        Rotate the cube as a whole.
        The X axis means in the direction of an R turn.
        The Y axis means in the direction of a U turn.
        The Z axis means in the direction of an F turn.
        The + direction is clockwise.
        The - direction is counterclockwise.

        Arguments:
          axis -- one of ['X', 'Y', 'Z']
          dir  -- one of ['+', '-']

        Return value: none
        '''
        assert axis in ['X', 'Y', 'Z']
        assert dir in ['+', '-']
        direction = {'+': 1, '-': 3}
        for num in range(direction[dir]):
            self.rep.rotate_cube(axis)

    def move_to_face(self, face):
        '''
        Rotates the cube so that the F face becomes the specified face
        
        Return value -- the original face relative to the new cube orientation
        '''
        assert face in ['U', 'L', 'B', 'F', 'R', 'D']
        opp_faces = ['U', 'L', 'B', 'F', 'B', 'R', 'D']
        cube_rotations = {'U': [['X', '-']], 'D': [['X', '+']], 'F': [],
                          'B': [['Y', '+'], ['Y', '+']], 'L': [['Y', '-']],
                          'R': [['Y', '+']]}
        value = cube_rotations[face]
        for list in value:
            self.rotate_cube(list[0], list[1])
        return opp_faces[-opp_faces.index(face) - 1]

    def move_slice(self, face, index, dir):
        '''
        Move the specified slice.
        Arguments:
          -- face: one of ['U', 'D', 'L', 'R', 'F', 'B']
          -- index: 0 for face, 1 for layer behind face, up to size - 1
          -- dir: '+' for clockwise or '-' for counterclockwise

        Return value: none
        '''
        assert face in ['U', 'D', 'F', 'B', 'L', 'R']
        assert dir in ['+', '-']
        assert index in range(self.rep.size)
        direction = {'+': 1, '-': 3}
        face = self.move_to_face(face)
        for _ in range(direction[dir]):
            self.rep.move_S(index)
        self.move_to_face(face)
        self.count += 1

    def random_rotations(self, n):
        '''
        Rotate the entire cube randomly 'n' times.

        Arguments:
          n -- number of random rotations to make

        Return value: none
        '''
        for _ in range(n):
            rot = random.choice('XYZ')
            dir = random.choice('+-')
            self.rotate_cube(rot, dir)

    def random_moves(self, n):
        '''
        Make 'n' random moves.

        Arguments:
          n -- number of random moves to make

        Return value: none
        '''
        for _ in range(n):
            face = random.choice('UDFBLR')
            dir = random.choice('+-')
            index = random.choice(range(self.rep.size))
            self.move_slice(face, index, dir)

    def scramble(self, nrots=10, nmoves=50):
        '''
        Scramble the cube.

        Arguments:
          nrots  -- number of random cube rotations to make
          nmoves -- number of random face moves to make

        Return value: none
        '''
        self.random_rotations(nrots)
        self.random_moves(nmoves)
        # Reset count before solving begins.
        self.count = 0

    def is_solved(self):
        '''
        Return True if the cube is solved.

        If the cube appears solved but is invalid, raise an
        InvalidCube exception with an appropriate error message.
        '''
        faces = ['U', 'L', 'F', 'B', 'R', 'D']
        colors = []
        for face in faces:
            face_list = self.rep.get_face(face)
            color = None
            for row in face_list:
                for col in row:
                    if col != color and color != None:
                        return False
                    else:
                        color = col
            colors.append(color)
        if not {'w', 'y', 'g', 'b', 'r', 'o'}.issubset(set(colors)):
            raise InvalidCube('A color is not represented')
        face = self.move_to_face(faces[colors.index('r')])
        urdl = self.rep.get_row('U', 0)[0]
        urdl += self.rep.get_row('R', 0)[0]
        urdl += self.rep.get_row('D', 0)[0]
        urdl += self.rep.get_row('L', 0)[0]
        solved = urdl in ['wbyg', 'gwby', 'ygwb', 'bygw']
        self.move_to_face(face)
        if not solved:
            raise InvalidCube('Cube is a reflection of a valid solve')
        return solved

    def display(self):
        '''
        Return a string version of the cube representation.
        '''
        return self.rep.display()


if __name__ == '__main__':
    cube = RubiksCube(4)
    print(cube.display())
    cube.scramble()
    print(cube.display())
