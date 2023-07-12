#!/usr/bin/python3
"""Defines the entry point of our command interprator."""
import cmd


class HBNBCommand(cmd.Cmd):
    """Defines the console intrprator.
       Attr:
           :: prompt(str): The consoles prompt."""

    prompt = "(hbnb) "

    def emptyline(self):
        """Does nothing on empty line + Enter key."""

        pass

    def do_EOF(self, arg):
        """Quits the program on EOF signal. """

        return True

    def do_quit(self, arg):
        """Exits the console/program. """

        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
