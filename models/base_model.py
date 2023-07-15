#!/usr/bin/python3
"""Defines a class BaseModel."""
from datetime import date, datetime
from uuid import uuid4
import models


class BaseModel:
    """Represents the Base model class for other classes. """

    def __init__(self, *args, **kwargs):
        """Initialises a new instance of the BaseModel class.
           Attr:
                :: *args(*): Unutilised.
                :: **kwargs(dict): A Key/Value pair of arguments/attributes
        """

        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Returns a string representation of an instance."""
        classname = self.__class__.__name__

        return "[{}] ({}) {}".format(classname, self.id, self.__dict__)

    def save(self):
        """Updates the updated_at attribute."""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns the dictionary representation of an instance."""

        tempdict = self.__dict__.copy()
        tempdict["created_at"] = self.created_at.isoformat()
        tempdict["updated_at"] = self.updated_at.isoformat()
        tempdict["__class__"] = self.__class__.__name__
        return tempdict
