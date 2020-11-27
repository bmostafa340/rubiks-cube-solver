# Name: Basel Mostafa
# Login: bmostafa
'''
Rubik's cube representations and basic operations.
'''

import rubiks_utils as u
import copy


class RubiksRep:
    '''
    Basic functionality of Rubik's cubes.
    '''

    def __init__(self, size):
        '''
        Initialize the cube representation.
        '''
        assert size > 0
        contents = {'U': 'w',
                    'D': 'y',
                    'F': 'r',
                    'B': 'o',
                    'L': 'g',
                    'R': 'b'}
        for key in contents:
            face = []
            for row in range(size):
                face.append([])
                for col in range(size):
                    face[row].append(contents[key])
            contents[key] = face
        self.contents = contents
        self.size = size

    ### Accessors.

    def get_row(self, face, row):
        '''
        Return a copy of the indicated row on the indicated face.
        The internal representation of the cube is not altered.
        '''
        assert face in self.contents
        assert row >= 0 and row < self.size
        return self.contents[face][row][:]

    def get_col(self, face, col):
        '''
        Return a copy of the indicated column on the indicated face.
        The internal representation of the cube is not altered.
        '''
        assert face in self.contents
        assert col >= 0 and col < self.size
        column = []
        for row in self.contents[face]:
            column.append(row[col])
        return column

    def get_face(self, face):
        '''
        Return the colors of a face, as a list of lists.
        '''
        assert face in self.contents
        return copy.deepcopy(self.contents[face])

    def get_contents(self):
        return copy.deepcopy(self.contents)

    def set_row(self, face, row, values):
        '''
        Change the contents of the indicated row on the indicated face.
        The internal representation of the cube is not altered.
        '''
        assert face in self.contents
        assert row >= 0 and row < self.size
        assert type(values) is list
        assert len(values) == self.size
        self.contents[face][row] = values[:]

    def set_col(self, face, col, values):
        '''
        Change the contents of the indicated column on the indicated face.
        The internal representation of the cube is not altered.
        '''
        assert face in self.contents
        assert col >= 0 and col < self.size
        assert type(values) is list
        assert len(values) == self.size
        for i, row in enumerate(self.contents[face]):
            row[col] = values[i]

    def set_face(self, face, values):
        self.contents[face] = copy.deepcopy(values)

    def set_contents(self, contents):
        self.contents = copy.deepcopy(contents)

    ### Basic operations.

    def rotate_face_cw(self, face):
        '''
        Rotate a face clockwise.
        '''
        assert face in self.contents
        result = []
        for i in range(self.size):
            result.append(self.get_col(face, i)[::-1])
        self.contents[face] = result

    def rotate_face_ccw(self, face):
        '''
        Rotate a face counterclockwise.
        '''
        assert face in self.contents
        result = []
        for i in range(self.size):
            result.append(self.get_col(face, self.size - 1 - i))
        self.contents[face] = result

    def move_S(self, index):
        '''
        Move the slice at depth index
        '''
        last_i = self.size - 1 - index
        u_row = self.get_col('L', last_i)[::-1]
        self.set_col('L', last_i, self.get_row('D', index))
        self.set_row('D', index, self.get_col('R', index)[::-1])
        self.set_col('R', index, self.get_row('U', last_i))
        self.set_row('U', last_i, u_row)
        if index == 0:
            self.rotate_face_cw('F')
        elif index == self.size - 1:
            self.rotate_face_ccw('B')

    def rotate_cube_X(self):
        '''
        Rotate the cube in the positive X direction.
        '''
        b_face = self.get_face('U')
        self.contents['U'] = self.contents['F']
        self.contents['F'] = self.contents['D']
        self.contents['D'] = self.contents['B']
        self.contents['B'] = b_face
        self.rotate_face_cw('R')
        self.rotate_face_ccw('L')

    def rotate_cube_Y(self):
        '''
        Rotate the cube in the positive Y direction.
        '''
        r_face = self.get_face('B')
        self.contents['B'] = self.contents['L']
        self.contents['L'] = self.contents['F']
        self.contents['F'] = self.contents['R']
        self.contents['R'] = r_face
        for num in range(2):
            self.rotate_face_cw('R')
            self.rotate_face_cw('B')
        self.rotate_face_cw('U')
        self.rotate_face_ccw('D')

    def rotate_cube_Z(self):
        '''
        Rotate the cube in the positive Z direction.
        '''
        self.rotate_cube_X()
        self.rotate_cube_Y()
        for num in range(3):
            self.rotate_cube_X()

    def rotate_cube(self, axis):
        '''
        Rotate the cube in the positive direction specified by axis
        '''
        if axis == 'X':
            self.rotate_cube_X()
        elif axis == 'Y':
            self.rotate_cube_Y()
        elif axis == 'Z':
            self.rotate_cube_Z()

    def display(self):
        '''
        Return a string version of the cube representation.
        '''
        return u.display(self.contents, self.size)

    def test_faces(self):
        '''
        Load the representation with unique characters.  For testing.
        '''
        self.contents = u.test_faces(self.size)


if __name__ == '__main__':
    rep = RubiksRep(3)
    rep.test_faces()
    print(rep.display())
    rep.rotate_cube_Z()
    print(rep.display())
