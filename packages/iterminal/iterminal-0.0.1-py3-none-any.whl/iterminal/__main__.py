from .interpreter import InterpreterSetup
from .console import ConsoleTerminal, ConsoleCommands
from .shell import Shell,LoadScript
from .commands import Commands

def run():
    shell = Shell()
    shell.add_resource_path('.')

    terminal = ConsoleTerminal()

    shell.add_component(InterpreterSetup())
    shell.add_component(Commands())
    shell.add_component(ConsoleCommands(terminal))
    shell.add_component(LoadScript('init.py'))

    terminal.run(shell)

if __name__=='__main__':
    run()
