from .interpreter import InterpretError
from .component import Component

class ConsoleTerminal:
    def __init__(self):
        import sys
        try:
            import readline
        except ImportError:
            pass

        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.stdin = sys.stdin
        self._input_listeners = []

    def add_prompt_listener(self, l):
        self._input_listeners.append(l)

    def prompt(self, prompt=''):
        i = input(prompt)
        for l in self._input_listeners:
            l(prompt, i)
        return i

    def clear(self):
        import os
        os.system('clear')
    
    def run(self, shell):
        shell.init()

        more = False
        while True:
            try:
                prompt = '... ' if more else '>>> '
                try:
                    line = self.prompt(prompt) # TODO: Handle if we want to use something else besides stdin
                except EOFError:
                    self.stdout.write('\n')
                    break
                else:
                    try:
                        more = not shell.process_input(line, self.stdout, self.stderr, self.stdin)
                    except InterpretError as e:
                        print(e)

            except KeyboardInterrupt:
                self.stdout.write('\nKeyboardInterrupt\n')
                # Clear the input buffer
                shell._buffer.clear()
                more = False

class ConsoleCommands(Component):
    def __init__(self, console):
        self._console = console
        super().__init__('console_commands')

    # The commands
    def clear(self):
        self._console.clear()

    def init(self, shell):
        shell.set_local('clear', self.clear)

    def dispose(self, shell):
        shell.unset_local('clear')
