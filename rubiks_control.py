'''
Rubik's cube controller (interactive interface).
'''

import copy, random
import rubiks_cube as c
import rubiks_utils as u
import solver as s


class BadCommand(Exception):
    '''
    This exception is raised when an invalid command is received.
    '''
    pass


class RubiksControl:
    '''
    This class implements an interactive Rubik's cube puzzle.
    '''

    def __init__(self, size, scramble=True):
        '''
        Initialize the cube representation.
        Initialize the set of basic commands.

        Arguments:
          size     -- the size of the cube (must be > 1)
                   -- 2 means a 2x2x2 cube; 3 means a 3x3x3 cube; etc
          scramble -- True if you want the cube scrambled
        '''
        assert size in [2, 3]
        self.cube = c.RubiksCube(size)
        self.history = []
        if scramble:
            self.cube.scramble()

        # Built-in commands.
        # Use lower-case for ease of typing.
        # Use double quotes since some commands use the single quote character.
        self.face_moves = \
            ["u", "u'", "d", "d'", "f", "f'",
             "b", "b'", "l", "l'", "r", "r'"]
        self.rotations = ["x", "x'", "y", "y'", "z", "z'"]
        self.user_commands = copy.deepcopy(u.user_commands)

    def do_save_commands(self, filename):
        '''Save user commands to a file.'''
        with open(filename, 'w') as outfile:
            for (cmd, contents) in self.user_commands.items():
                print(f'{cmd} {contents}', file=outfile)

    def do_load_commands(self, filename):
        '''Load user commands from a file.'''
        self.user_commands = {}
        with open(filename) as infile:
            for line in infile:
                words = line.split()
                assert len(words) >= 2
                cmd = words[0]
                contents = words[1:]
                self.user_commands[cmd] = contents

    def do_print_commands(self):
        '''Print user commands to the terminal.'''
        for (cmd, contents) in self.user_commands.items():
            print(f'{cmd} : {contents}')

    def do_add_command(self, name, cmds):
        '''
        Add a user command.

        Arguments:
          name -- the name of the command
          cmds -- a list of the commands that the name should expand to

        Return value: none
        '''
        assert type(name) is str
        assert type(cmds) is list
        cmd_sequence = ''
        for cmd in cmds:
            cmd_sequence += cmd + ' '
        self.user_commands[name] = cmd_sequence.strip()

    def do_command(self, cmd):
        '''
        Execute a command.

        Arguments: 
          cmd -- a command

        Return value: none
        '''
        assert type(cmd) is str
        f_rots = {"u": ['U', '+'], "u'": ['U', '-'], "d": ['D', '+'],
                  "d'": ['D', '-'], "f": ['F', '+'], "f'": ['F', '-'],
                  "b": ['B', '+'], "b'": ['B', '-'], "l": ['L', '+'],
                  "l'": ['L', '-'], "r": ['R', '+'], "r'": ['R', '-']}
        c_rots = {"x": ['X', '+'], "x'": ['X', '-'], "y": ['Y', '+'],
                  "y'": ['Y', '-'], "z": ['Z', '+'], "z'": ['Z', '-']}
        cmds = cmd.split()
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if cmd in self.face_moves:
                self.cube.move_slice(f_rots[cmd][0], 0, f_rots[cmd][1])
            elif cmd in self.rotations:
                self.cube.rotate_cube(c_rots[cmd][0], c_rots[cmd][1])
            elif cmd in self.user_commands:
                new_cmd = self.user_commands[cmd]
                self.do_command(new_cmd)
            else:
                raise BadCommand('Unknown user command - ' + cmd)

    def do_undo(self):
        '''
        Undo the last move(s), restoring the previous state.
        '''
        if self.history == []:
            raise BadCommand('No moves to undo!')
        (rep, count) = self.history.pop()
        self.cube.put_state(rep, count)

    def do_solve(self, filename):
        '''
        Saves the output of the solution to a rubiks cube to a file.
        '''
        with open(filename, 'w') as outfile:
            if self.cube.rep.size == 2:
                solver = s.Solver_2x2(self.cube)
            else:
                solver = s.Solver_3x3(self.cube)
            solution = solver.solve()
            c_cube = c.RubiksCube(self.cube.rep.size)
            c_cube.rep.set_contents(self.cube.rep.get_contents())
            control = RubiksControl(self.cube.rep.size)
            control.cube = c_cube
            print('Initial state:', file=outfile)
            print(control.cube.display(), file=outfile)
            for cmd in solution:
                control.do_command(cmd)
                print(cmd, file=outfile)
                print(control.cube.display(), file=outfile)
            print('Solution length (qt): ' + str(c_cube.count), file=outfile)

    def play(self, check_solved=True):
        '''Interactively solve Rubik's cube.'''

        while True:
            print(self.cube.display())
            print(f'Move count: {self.cube.count}\n')

            if check_solved and self.cube.is_solved():
                print('SOLVED!')
                break

            cmd = input('cube> ')
            cmds = cmd.split()
            if len(cmds) < 1:
                continue

            try:
                if cmds[0] in ['q', 'quit']:
                    break

                # Undo a move.
                if len(cmds) == 1 and cmds[0] in ['-', 'undo']:
                    self.do_undo()

                # Save the commands to a file.
                elif len(cmds) == 2 and cmds[0] == 'save':
                    self.do_save_commands(cmds[1])

                # Load commands from a file.
                elif len(cmds) == 2 and cmds[0] == 'load':
                    self.do_load_commands(cmds[1])

                # Solve the cube and print the solution to a file
                elif len(cmds) == 2 and cmds[0] == 'solve':
                    self.do_solve(cmds[1])

                # Print all commands.
                elif len(cmds) == 1 and cmds[0] == 'cmds':
                    self.do_print_commands()

                # Add a new command if the second word is ':'.
                elif len(cmds) > 2 and cmds[1] == ':':
                    self.do_add_command(cmds[0], cmds[2:])

                else:
                    # Save the cube state before moving.
                    self.history.append(self.cube.get_state())

                    for subcmd in cmds:
                        self.do_command(subcmd)

            except BadCommand as b:
                print(f'Invalid command line: {cmd}')
                print(b)


if __name__ == '__main__':
    # Leave 'scramble' as True normally.
    # Make it False if you want to test rotations on a solved cube.
    scramble = True
    check_solved = scramble
    cube = RubiksControl(2, scramble)
    cube.play(check_solved)
