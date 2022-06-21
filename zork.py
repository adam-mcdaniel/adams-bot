
from subprocess import Popen, PIPE

DEFAULT_LEAFLET = ['Taken.', 'Welcome to Dungeon!', '', 'Dungeon is a game of adventure, danger, and low cunning.  In it', 'you will explore some of the most amazing territory ever seen by mortal', 'man.  Hardened adventurers have run screaming from the terrors contained', 'within.', '', 'In Dungeon, the intrepid explorer delves into the forgotten secrets', 'of a lost labyrinth deep in the bowels of the earth, searching for', 'vast treasures long hidden from prying eyes, treasures guarded by', 'fearsome monsters and diabolical traps!', '', 'No DECsystem should be without one!', '', 'Dungeon was created at the Programming Technology Division of the MIT', 'Laboratory for Computer Science by Tim Anderson, Marc Blank, Bruce', 'Daniels, and Dave Lebling.  It was inspired by the Adventure game of', 'Crowther and Woods, and the Dungeons and Dragons game of Gygax', 'and Arneson.  The original version was written in MDL (alias MUDDLE).', 'The current version was translated from MDL into FORTRAN IV by', 'a somewhat paranoid DEC engineer who prefers to remain anonymous,', 'and was later translated to C.', '', 'On-line information may be obtained with the commands HELP and INFO.']

class Zork:
    def __init__(self, init_text: str, leaflet_text: str, cwd: str):
        self.process = Popen(['./zork'], stdin=PIPE, stdout=PIPE, cwd=cwd)
        self.init_text = init_text
        self.leaflet_text = leaflet_text
        self.stdin = self.process.stdin
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.output_lines = iter(self.stdout.readline, b'')

    def read(self) -> list[str]:
        self.stdout.flush()

        result = []
        if self.init_text:
            result.append(self.init_text)
            next(self.output_lines)
            self.init_text = None

        for line in self.output_lines:
            if line == b'>\n':
                break
            result.append(line.decode('ascii').strip())

        if result == DEFAULT_LEAFLET:
            result = self.leaflet_text.splitlines()
        return result

    def write(self, command: str) -> bool:
        if command.strip() == '':
            return False
        self.stdin.write(bytes(command.strip() + '\n', 'ascii'))
        self.stdin.flush()
        return True

    def close(self):
        self.process.kill()


if __name__ == '__main__':
    zork = Zork('Welcome to Adam\'s Dungeon!', '''Welcome to Adam's Dungeon!
This dungeon is essentially just Zork plugged into my bot to work in Discord.
I hope you enjoy it!
-- Adam McDaniel''', './zork')
    while lines := zork.read():
        print('\n'.join(lines))
        while not zork.write(input('users> ')): pass