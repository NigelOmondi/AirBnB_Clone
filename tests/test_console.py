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


class Test_console_show(unittest.TestCase):
    """unittests for testing the consoles show command."""

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

    def test_show_missing_classname(self):
        """Test the show command without a classname."""

        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_invalid_classname(self):
        """Test the show command with an invalid classname."""

        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Invalid"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Invalid.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_missing_id_dot_syntax(self):
        """Test the show command without an id using dot syntax."""

        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_missing_id(self):
        """Test the show command without an id.(space syntax)"""

        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_invalid_id_dot_syntax(self):
        """Test the show command with an invalid id.(dot notation)"""

        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                HBNBCommand().onecmd("Amenity.show(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                HBNBCommand().onecmd("Place.show(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                HBNBCommand().onecmd("Review.show(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_show_invalid_id(self):
        """Test the show command with an invalid id.(space noation)"""

        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                HBNBCommand().onecmd("show Amenity 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                HBNBCommand().onecmd("show Place 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(
                HBNBCommand().onecmd("show Review 69"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_successful_show_dot(self):
        """Test the show command with a valid id.(dot notation)"""

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_BasemodelId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["BaseModel." + test_BasemodelId]
            runcmd = "BaseModel.show(" + test_BasemodelId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_UserId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["User." + test_UserId]
            runcmd = "User.show(" + test_UserId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_StateId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["State." + test_StateId]
            runcmd = "State.show(" + test_StateId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_CityId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["City." + test_CityId]
            runcmd = "City.show(" + test_CityId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_AmenityId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Amenity." + test_AmenityId]
            runcmd = "Amenity.show(" + test_AmenityId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_PlaceId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Place." + test_PlaceId]
            runcmd = "Place.show(" + test_PlaceId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_ReviewId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Review." + test_ReviewId]
            runcmd = "Review.show(" + test_ReviewId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())

    def test_successful_show(self):
        """Test the show command with a valid id.(space notation)"""

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_BasemodelId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["BaseModel." + test_BasemodelId]
            runcmd = "show BaseModel " + test_BasemodelId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_UserId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["User." + test_UserId]
            runcmd = "show User " + test_UserId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_StateId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["State." + test_StateId]
            runcmd = "show State " + test_StateId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_CityId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["City." + test_CityId]
            runcmd = "show City " + test_CityId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_AmenityId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Amenity." + test_AmenityId]
            runcmd = "show Amenity " + test_AmenityId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_PlaceId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Place." + test_PlaceId]
            runcmd = "show Place " + test_PlaceId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_ReviewId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Review." + test_ReviewId]
            runcmd = "show Review " + test_ReviewId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertEqual(data.__str__(), output.getvalue().strip())


class Test_console_destroy(unittest.TestCase):
    """unittests for the destroy command"""

    @classmethod
    def pretest(self):
        """Renames the json file to maintain original data."""

        try:
            os.rename("file.json", "tempfile")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def posttest(self):
        """Reverts the original json file."""

        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tempfile", "file.json")
        except IOError:
            pass

    def test_no_class(self):
        """Test the destroy command with no class."""

        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_destroy_unknwon_class(self):
        """Test the destroy command with an unknown class."""

        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Invalid"))
            self.assertEqual(errormsg, output.getvalue().strip().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Invalid.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_destroy_invalid_id_dot(self):
        """Test the console desti command with invalid id
        (dot notation)."""

        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(69)"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_destroy_invalid_id(self):
        """Test the console destroy command with invalid id."""

        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 69"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 69"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_destroy_no_id(self):
        """Test the console destroy command with no id."""

        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_destroy_no_id(self):
        """Test consoles destroy command with no id.(dot notation)"""

        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    def test_successful_destroy_dot(self):
        """Test successful destroy command with dot notation."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["BaseModel." + test_destroyId]
            runcmd = "Basemodel.destroy(" + test_destroyId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["User." + test_destroyId]
            runcmd = "User.destroy(" + test_destroyId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["State." + test_destroyId]
            runcmd = "State.destroy(" + test_destroyId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["City." + test_destroyId]
            runcmd = "City.destroy(" + test_destroyId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Amenity." + test_destroyId]
            runcmd = "Amenity.destroy(" + test_destroyId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Place." + test_destroyId]
            runcmd = "Place.destroy(" + test_destroyId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Review." + test_destroyId]
            runcmd = "Review.destroy(" + test_destroyId + ")"
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())

    def test_successful_destroy(self):
        """Tests successful destroy command.(space notation)"""

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["BaseModel." + test_destroyId]
            runcmd = "destroy BaseModel " + test_destroyId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["User." + test_destroyId]
            runcmd = "destroy User " + test_destroyId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["State." + test_destroyId]
            runcmd = "destroy State " + test_destroyId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["City." + test_destroyId]
            runcmd = "destroy City " + test_destroyId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Amenity." + test_destroyId]
            runcmd = "destroy Amenity " + test_destroyId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Place." + test_destroyId]
            runcmd = "destroy Place " + test_destroyId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_destroyId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            data = storage.all()["Review." + test_destroyId]
            runcmd = "destroy Review " + test_destroyId
            self.assertFalse(HBNBCommand().onecmd(runcmd))
            self.assertNotIn(data, storage.all())
