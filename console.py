#!/usr/bin/python3
"""Defines the entry point of our command interprator."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the console intrprator.
       Attr:
           :: prompt(str): The consoles prompt."""

    prompt = "(hbnb) "
    __classnames = {
            "BaseModel",
            "User",
            "Place",
            "City",
            "State",
            "Amenity",
            "Review"
            }

    def emptyline(self):
        """Does nothing on empty line + Enter key."""

        pass

    def do_EOF(self, arg):
        """Quits the program on EOF signal. """

        return True

    def do_quit(self, arg):
        """Exits the console/program.
        Usage: $ quit
        """

        return True

    def do_create(self, arg):
        """Creates and prints id of a new instance.
        Usage: $ create <Instance name>
        """

        args = parse(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classnames:
            print("** class doesn't exist **")
        else:
            print(eval(args[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints a str representation of an instance.
        Usage: $ show <classname> <instance id>
        """
        args = parse(arg)
        allinstances = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classnames:
            print("** Class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif ""{}.{}"".format(arg[0], arg[1]) not in allinstances:
            print("** no instance found**")
        else:
            print(allinstances["{}.{}".format(args[0], args[1])])

    def destroy(self, arg):
        """Deletes an intance based on the class name and id.
        usage: $ destroy <classname> <instance id>
        """

        args = parse(args)
        allinstances = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classnames:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in allinstances:
            print("** no instance found **")
        else:
            del allinstances["{}.{}".format(args[0], args[1])]
            storage.save()

    def all(self, args):
        """Prints all string representation of all instances.
        usage: $ all <class name>(optional)"""

        args = parse(arg)
        if len(args) > 0 and args[0] not in HBNBCommand.__classnames:
            print("** class doesn't exist **")
        else:
            allinstances = storage.all()
            tempdict = {}
            for instance in allintances.value():
                if len(args) > 1 and args[0] == instance.__class__.__name__:
                    tempdict.append(instance.__str__())
                elif len(args) == 0:
                    tempdict.append(instance.__str__())
            print(tempdict)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
