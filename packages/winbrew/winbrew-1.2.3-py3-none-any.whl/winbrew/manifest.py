import os
import sqlite3

import winbrew
import winbrew.util

class Manifest:
    """
    Stores a list of all files installed by a formula.  This class is used to
    determine which files to uninstall, and to check for conflicts between
    formulas.
    """

    def __init__(self, name):
        self.files = []
        self.name = name

    def save(self):
        """
        Write the manifest to the manifest file directory
        """
        query = 'DELETE FROM InstalledFile where formula=?'
        self.db().cursor().execute(query, (self.name,))

        values = [(path, self.name) for path in self.files]
        query = 'INSERT INTO InstalledFile (path, formula) VALUES (?, ?)'
        self.db().cursor().executemany(query, values)

        self.db().commit()

    def load(self):
        """
        Read the manifest from the manifest file directory
        """
        query = 'SELECT path FROM InstalledFile WHERE formula=?'
        results = self.db().cursor().execute(query, (self.name,))
        self.files = [result[0] for result in results]

    def delete(self):
        """
        Delete the manifest
        """
        query = 'DELETE FROM InstalledFile WHERE formula=?'
        self.db().cursor().execute(query, (self.name,))
        self.db().commit()

    @property
    def installed(self):
        """
        Returns true if the Manifest indicates the formula is installed
        """
        query = 'SELECT DISTINCT formula FROM InstalledFile WHERE formula=? LIMIT 1'
        results = self.db().cursor().execute(query, (self.name,))
        return len(list(results)) > 0

    @classmethod
    def all(self):
        """
        List all installed packages
        """
        query = 'SELECT DISTINCT formula FROM InstalledFile'
        results = self.db().cursor().execute(query)
        return [Manifest(result[0]) for result in results]
        # FIXME: This may be inefficient

    @classmethod
    def db(self):
        if not getattr(self, '_db', None):
            winbrew.util.mkdir_p(winbrew.manifest_path)
            self._db = sqlite3.connect(os.path.join(winbrew.manifest_path, 'manifest.db'))
            self.migrate()
        return self._db

    @classmethod
    def migrate(self):
        """
        Execute database migrations
        """
        installedFile = """CREATE TABLE IF NOT EXISTS InstalledFile (
            path TEXT NOT NULL UNIQUE,
            formula TEXT NOT NULL,
            PRIMARY KEY(path, formula))"""
        self._db.cursor().execute(installedFile)

