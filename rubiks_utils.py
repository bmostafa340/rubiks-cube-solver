'''
Utility data and functions for use with Rubik's cube program.
'''

import string

#
# Utility data.
#

# Built-in user commands.
user_commands = {
    # ---------------------------------------------------------------------- 
    # Basic moves.
    # ---------------------------------------------------------------------- 

    # Cube slices.
    "m": "x' l' r",
    "m'": "x  l  r'",
    "e": "y' u  d'",
    "e'": "y  u' d",
    "s": "z  f' b",
    "s'": "z' f  b'",

    # Double moves.
    "u2": "u u",
    "d2": "d d",
    "f2": "f f",
    "b2": "b b",
    "l2": "l l",
    "r2": "r r",

    "m2": "m m",
    "e2": "e e",
    "s2": "s s",

    "x2": "x x",
    "y2": "y y",
    "z2": "z z",

    # ---------------------------------------------------------------------- 
    # Algorithms.
    # ---------------------------------------------------------------------- 

    #
    # Top layer.
    #

    # Move edge cube to top layer.
    "df->uf'": "f' u' r u",

    # Move corner cube from top to bottom layer.
    "ufr->dfr": "r' d' r d",
    # Move corner cube from bottom to top layer.
    "dfr->ufr": "f d f'",

    # Orient corner cube in top layer.
    "ufr": "f d f' d' f d f'",
    "ufr'": "r' d' r d r' d' r",

    #
    # Middle layer.
    #

    "uf->fr": "u r u' r' f r' f' r",
    "uf->lf": "u' l' u l f' l f l'",

    #
    # Last layer.
    #

    # Edge orientation.
    "fur": "f u r u' r' f'",
    "fru": "f r u r' u' f'",

    # Edge permutation.
    "ep": "r u r' u r u2 r' u",

    # Corner orientation.
    "cyc3": "r' u l u' r u l' u'",
    "cyc3'": "u l u' r' u l' u' r",

    # Corner permutation.
    "rd": "r d r' d' r d r' d'",
    "dr": "d r d' r' d r d' r'",
    "rot2": "rd u' dr u",
    "rot2'": "dr u' rd u",
    "rot2d": "rd u2 dr u2",
    "rot2d'": "dr u2 rd u2",
    "rot3": "rd u' rd u' rd u2",
    "rot3'": "dr u' dr u' dr u2",

    # Ledges.
    "lbf": "u' m' u",
    "lfb": "u m2 u'",
    "ltr": "u' m u",
    "lrt": "u m u2 m' u",
    "ltl": "u' m u2 m2 u'",

    # Last ledges.
    "llbf": "u' m u2 m u'",
    "llbb": "u m' u2 m' u",
    "ltt": "d l2 d' m2 d2 m d' l2 d'",

    # Redges.
    "rbf": "u m' u'",
    "rfb": "u' m2 u",
    "rtl": "u m u'",
    "rlt": "u' m u2 m' u'",
    "rtr": "u m u2 m2 u",

    # Flip midges.
    "fm": "m' u m' u m' u2 m u m u m u2",

    # Place midges.
    "mfc": "u2 m u2 m'",
    "mbc": "u2 m' u2 m",
    "mtb": "u2 m2 u2 m2",
    "md": "e2 m e2 m",
}


#
# Utility functions.
#

def move_to_string(face, dir):
    '''
    Return the string representation of a quarter-turn move.
    '''
    assert face in ['U', 'D', 'F', 'B', 'L', 'R', 'X', 'Y', 'Z']
    assert dir in ['+', '-']
    face = face.lower()
    if dir == '+':
        dir = ''
    else:
        dir = "'"  # the ' character
    return face + dir


def adjacent(face1, face2):
    '''
    Test if two faces are adjacent.
    '''
    all_faces = ['U', 'D', 'L', 'R', 'F', 'B']
    assert face1 in all_faces
    assert face2 in all_faces
    non_adjacents = [
        ('U', 'D'), ('D', 'U'),
        ('L', 'R'), ('R', 'L'),
        ('F', 'B'), ('B', 'F')
    ]
    return (face1, face2) not in non_adjacents


def test_faces(size):
    '''
    Fill all faces of a size x size x size cube with different characters, 
    for testing.  'size' must be 2, 3, 4, or 5.
    '''
    assert size in [2, 3, 4, 5]
    chars = ''
    for char in string.printable:
        if char not in string.whitespace:
            chars += char
    chars *= 3
    faces = 'UDFBLR'
    contents = {}
    skip = size * size
    for (i, face) in enumerate(faces):
        start = i * skip
        end = start + skip
        s = chars[start:end]
        face_colors = []
        s1 = 0
        for _ in range(size):
            face_colors.append(list(s[s1:s1 + size]))
            s1 += size
        contents[face] = face_colors
    return contents


def display_face(face):
    '''
    Return a list of strings representing a single face of a cube.
    '''

    f = []
    for row in face:
        f.append(' '.join(row))
    return f


def concat_faces(face1, face2, sep=' | '):
    '''
    Horizontally concatenate two faces, given a separator 'sep'.
    Return the resulting list of strings.
    '''

    assert len(face1) == len(face2)
    ff = []
    for (i, f) in enumerate(face1):
        ff.append(f + sep + face2[i])
    return ff


def decorate_lines(lines, prefix, suffix):
    '''
    Add a prefix and a suffix to each string in a list of strings.
    Return the new list.  The original list is not modified.
    '''

    return list(map(lambda l: prefix + l + suffix, lines))


def display(cube, size):
    '''
    Return a string which represents a flattened display of a cube.
    '''

    blank_face = [[' '] * size] * size
    bl = display_face(blank_face)
    u = display_face(cube['U'])
    d = display_face(cube['D'])
    l = display_face(cube['L'])
    r = display_face(cube['R'])
    f = display_face(cube['F'])
    b = display_face(cube['B'])

    # Display the cube like this:
    #
    #     U
    #   L F R
    #     D
    #     B

    # Separator lines.

    n = 2 * size + 1
    spacer = ' ' * (n + 1)
    dashes = '-' * n
    sep1 = ' ' + spacer + '+' + dashes + '+\n'
    sep2 = ' ' + ('+' + dashes) * 3 + '+\n'

    # Put it all together.

    s = '\n'
    s += sep1

    lines1 = concat_faces(bl, concat_faces(u, bl))
    s += ''.join(decorate_lines(lines1, '   ', '\n'))
    s += sep2

    lines2 = concat_faces(l, concat_faces(f, r))
    s += ''.join(decorate_lines(lines2, ' | ', ' |\n'))
    s += sep2

    lines3 = concat_faces(bl, concat_faces(d, bl))
    s += ''.join(decorate_lines(lines3, '   ', '\n'))
    s += sep1

    lines4 = concat_faces(bl, concat_faces(b, bl))
    s += ''.join(decorate_lines(lines4, '   ', '\n'))
    s += sep1

    return s


if __name__ == '__main__':
    cube2 = {
        'U': [['w', 'w'], ['w', 'w']],
        'D': [['y', 'y'], ['y', 'y']],
        'L': [['o', 'o'], ['o', 'o']],
        'R': [['r', 'r'], ['r', 'r']],
        'F': [['g', 'g'], ['g', 'g']],
        'B': [['b', 'b'], ['b', 'b']],
    }

    cube3 = {
        'U': [['w', 'w', 'w'], ['w', 'w', 'w'], ['w', 'w', 'w']],
        'D': [['y', 'y', 'y'], ['y', 'y', 'y'], ['y', 'y', 'y']],
        'L': [['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']],
        'R': [['r', 'r', 'r'], ['r', 'r', 'r'], ['r', 'r', 'r']],
        'F': [['g', 'g', 'g'], ['g', 'g', 'g'], ['g', 'g', 'g']],
        'B': [['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']],
    }

    print(display(cube2, 2))
    print(display(cube3, 3))
