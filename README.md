This repository extends the Fa 2019 Caltech CS 1 Final, which involved
completing a text based UI for a virtual Rubik's Cube. Caltech students 
who plan to take CS 1 in the future should not look further by the Honor 
Code.

Usage Overview:

This program implements both a 2x2x2 and 3x3x3 Rubik's cube solver.
The interactive solver is initialized on a randomly generated cube by
default when rubiks_control.py is run. It continuously requests user
input through the terminal until the cube is solved.

Some basic commands are described below.

Clockwise quarter turns:
    - f : front face
    - b : back face
    - l : left face
    - r : right face
    - d : down (bottom) face
    - u : up (top) face

Counterclockwise quarter turns:
    - f', b', l', r', d', u'

Shortcuts:
    - cmds : prints a list of commands that can be used to execute multiple
             simpler commands at once

Solve and store solution in file: solve <filename>


Solver Algorithm Overview:

2x2x2 Rubik's Cube Solver: This solver computes an optimal solution by means
of a more efficient brute force algorithm.

Optimization 1:
Rather than building up a single BFS tree from the scrambled state and searching
until the solved state is found, two BFS trees are built - one from the scrambled
state and one from the solved state. The program alternates between building the
next level of each tree. Each time it builds a new level, it compares the two trees.
If the same cube is found in both trees, combining the moves needed to get to the
solution from each tree yields a solution (where the moves from the solved state
must be reversed).

The proof of correctness follows from that of BFS. The i-th level of a BFS tree
must contain every state that is reachable from the root node in i moves. So
if an optimal solution of x moves exists, the state after the (x // 2)-th move
will exist in the (x // 2)-th level (0-indexed) of the BFS tree from the scrambled state,
as well as the (x - x // 2)-th level of the BFS tree from the solved state. If
a solution has not already been found, this solution will be found, and it will have
x moves.

Optimization 2:
A naive optimal brute force solver might attempt to move all 6 faces in both
directions when computing each new layer of the BFS tree. However, this solver
cuts the number of moves to consider on each iteration in half through a clever
trick.

First, we note that if two cubes are rotations of one another, they are an equal
number of quarter turns away from the solved state. Therefore, if two moves produce
the same cube barring a rotation, we can ignore one of them and still find an optimal
solution. In fact, this observation is of great utility, since rotations of opposite
faces produce exactly this effect; a clockwise rotation of the left face produces the
same relative motion of cubies as a clockwise rotation of the right face, for
instance. This argument suggests that we can forego consideration of half of the
moves in (l, l', r, r', u, u', d, d', f, f', b, b'). But in practice, we are left with
another challenge.

Two cubes must be considered the same if they are rotated versions of one another.
So after each new level of a BFS tree is generated, we must be able to detect whether
a cube in one BFS tree is a rotation of a cube in the other BFS tree. Doing so
computationally is prohibitively expensive. But what if there is an efficient way to
ensure that cubes are never rotations of one another to begin with? In fact, there is.
One can establish some kind of inherent "orientation" of the cubes. Then one can initialize
the algorithm by rotating the scrambled cube so its orientation matches that of a target
solved cube, and one can carefully choose which 6 of the original set of 12 moves to keep
such that they do not change a cube's inherent orientation. The specific implementation
chosen for this solver is to rotate the solved cube so that its top right front cubie is
in the same position as that of a target solved cube. The set of moves to consider is
chosen to be (l, l', b, b', d, d'), since they provide the benefit described in the
previous paragraph while maintaining the orientation of the "pivot" cubie. This enables 
detection of identical cubes in O(n) time on the size of a tree.

To give a sense of just how drastic the speed and memory improvements are,
consider the following. It has been found that the maximum number of quarter
turns required to solve a 2x2x2 cube is 14 (see God's Number for the 2x2x2 cube).
Consequently, in the worst case, a naive brute force approach would consider
approximately 12 ^ 14 states for the 14th move. In contrast, this approach would
only consider approximately 2 * 6 ^ 7 states to find a 14 move solution.
The number of cube states considered is reduced by a factor of over 2 billion.

The resulting 2x2x2 cube solver takes no more than a few seconds to solve a cube
on a VM with 10 GB RAM available to it. The time required for a solve depends
heavily on the available RAM, so your mileage may vary.

3x3x3 Rubik's Cube Solver: This solver computes a solution using the corners first
method outlined here: rubikscube.info/beginner.php

This solver generally takes a greedy approach to solving a 3x3x3 cube, brute forcing
each step in the process without regard to the global performance.

Optimization 1:
By constructing and solving a 2x2x2 cube made from the corners of the 3x3x3 cube
the corners of the 3x3x3 cube can be solved optimally.
