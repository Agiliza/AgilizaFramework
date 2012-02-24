"""
This file is part of Agiliza.

Agiliza is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Agiliza is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Agiliza.  If not, see <http://www.gnu.org/licenses/>.


Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
"""
import abc
import os


class Storage(metaclass=abc.ABCMeta):
    """
    A base storage class, providing some default behaviors that all
    other storage systems can inherit or override, as necessary.
    """

    def open(self, name, mode='rb'):
        """
        Retrieves the specified file from storage.
        """
        file = self._open(name, mode)
        return file

    def save(self, name, content):
        """
        Saves new content to the file specified by name. The content
        should be a proper File object, ready to be read from the
        beginning.
        """
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name

        name = self.get_available_name(name)
        name = self._save(name, content)

        # Store filenames with forward slashes, even on Windows
        return name.replace('\\', '/')

    def get_valid_name(self, name):
        """
        Returns a filename, based on the provided filename, that's
        suitable for use in the target storage system.
        """
        pass

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        # If the filename already exists, add an underscore and a number
        # (before the file extension, if one exists) to the filename
        # until the generated filename doesn't exist.
        count = itertools.count(1)
        while self.exists(name):
            # file_ext includes the dot.
            name = os.path.join(dir_name, "%s_%s%s" % (
                file_root, count.next(), file_ext))

        return name

    @abc.abstractmethod
    def path(self, name):
        """
        Returns a local filesystem path where the file can be retrieved
        using Python's built-in open() function. Storage systems that
        can't be accessed using open() should *not* implement this
        method.
        """
        pass

    @abc.abstractmethod
    def delete(self, name):
        """
        Deletes the specified file from the storage system.
        """
        pass

    @abc.abstractmethod
    def exists(self, name):
        """
        Returns True if a file referened by the given name already
        exists in the storage system, or False if the name is available
        for a new file.
        """
        pass

    @abc.abstractmethod
    def listdir(self, path):
        """
        Lists the contents of the specified path, returning a 2-tuple of
        lists; the first item being directories, the second item being
        files.
        """
        pass

    @abc.abstractmethod
    def size(self, name):
        """
        Returns the total size, in bytes, of the file specified by name.
        """
        pass

    @abc.abstractmethod
    def url(self, name):
        """
        Returns an absolute URL where the file's contents can be
        accessed directly by a Web browser.
        """
        pass

    @abc.abstractmethod
    def accessed_time(self, name):
        """
        Returns the last accessed time (as datetime object) of the file
        specified by name.
        """
        pass

    @abc.abstractmethod
    def created_time(self, name):
        """
        Returns the creation time (as datetime object) of the file
        specified by name.
        """
        pass

    @abc.abstractmethod
    def modified_time(self, name):
        """
        Returns the last modified time (as datetime object) of the file
        specified by name.
        """
        pass
