#!/usr/bin/python3
"""Defines the unnitsts for console.py file"""

import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class Testconsolepromt(unittest.TestCase):
    """unittest for testing the consoles prompting."""

    def test_promptmsg(self):
        """Test the consoles prompt message."""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        """Test for empty line parsing by the console."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual("", f.getvalue().strip())


class Test_console_help(unittest.TestCase):
    """unittest for testing the consoles help command."""

    def test_help_quit(self):
        """Test the help command for quit method."""

        msg = ("Exits the console/program.\n        "
               "Usage: $ quit")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help_EOF(self):
        """Test the help command for EOF method."""

        msg = ("Quits the program on EOF signal.")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help_create(self):
        """Test the help command for create method."""

        msg = ("Creates and prints id of a new instance.\n        "
               "Usage: $ create <class name>")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help_show(self):
        """Test the help command for show method."""

        msg = ("Prints a str representation of an instance.\n        "
               "Usage: $ show <classname> <instance id>")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help_destroy(self):
        """Test the help command for destroy method."""

        msg = ("Deletes an intance based on the class name and id.\n        "
               "usage: $ destroy <classname> <instance id>")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help_all(self):
        """Test the help command for all method."""

        msg = ("Prints all string representation of all instances.\n        "
               "Usage: $ all <class name>(optional)")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help_update(self):
        """Test the help command for update method."""

        msg = ("Updates an instance based on the class name and id.\n        "
               "Usage: update <class name> <id> <attribute name> "
               "<attribute value>")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help_count(self):
        """Test the help command for count method."""

        msg = ("Prints the number of instances of a class.\n        "
               "Usage: $ count <class> / $ <class>.count()")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help count")
            self.assertEqual(msg, f.getvalue().strip())

    def test_help(self):
        msg = ("Documented commands (type help <topic>):\n"
               "========================================\n"
               "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(msg, output.getvalue().strip())


class Test_console_quit(unittest.TestCase):
    """unittsests for testing the consoles EOF & quit commands."""

    def test_quit(self):
        """Test the consoles quit command."""

        with patch("sys.quit", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF(self):
        """Test the consoles EOF functionality."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class Test_console_create(unittest.TestCase):
    """unittests for testing the consoles create command."""

    @classmethod
    def preptest(self):
        """Renames the json file to maintain original data."""

        try:
            os.rename("file.json", "tempfile")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def cleanup(self):
        """Removes the new json file and restores the original."""

        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tempfile", "json.file")
        except IOError:
            pass

    def test_create_missing_classname(self):
        """Test the create command without a classname."""

        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_create_invalid_classname(self):
        """Test the create command with an invalid classname."""

        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Invalid"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_create_unknown_syntax(self):
        """Test the create command with an unknown syntax."""

        errormsg = "*** Unknown syntax: Invalid.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Invalid.create()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        errormsg2 = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(errormsg2, output.getvalue().strip())

    def test_create_valid_objects(self):
        """Test the create command."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertTrue(len(output.getvalue().strip()) > 0)
            test_id = output.getvalue().strip()
            test_model = "BaseModel." + test_id
            self.assertIn(test_model, storage.all().keys())

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertTrue(len(output.getvalue().strip()) > 0)
            test_id = output.getvalue().strip()
            test_model = "User." + test_id
            self.assertIn(test_model, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertTrue(len(output.getvalue().strip()) > 0)
            test_id = output.getvalue().strip()
            test_model = "State." + test_id
            self.assertIn(test_model, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertTrue(len(output.getvalue().strip()) > 0)
            test_id = output.getvalue().strip()
            test_model = "City." + test_id
            self.assertIn(test_model, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertTrue(len(output.getvalue().strip()) > 0)
            test_id = output.getvalue().strip()
            test_model = "Amenity." + test_id
            self.assertIn(test_model, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertTrue(len(output.getvalue().strip()) > 0)
            test_id = output.getvalue().strip()
            test_model = "Place." + test_id
            self.assertIn(test_model, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertTrue(len(output.getvalue().strip()) > 0)
            test_id = output.getvalue().strip()
            test_model = "Review." + test_id
            self.assertIn(test_model, storage.all().keys())
