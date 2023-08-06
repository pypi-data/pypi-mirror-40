""" database.py is a module to communicate with a database. """

import sqlite3
from typing import List


class Database:
    """ Database class initializes and manipulates SQLite3 database. """

    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.donelist = 'donelist'
        self.course = 'course'

    def close_db(self):
        """ Close the database """
        if self.con:
            self.con.close()

    def create_table(self):
        """
        Create table.

        donelist: Table for registration of date, course name and duration you studied.
        course: Table for validation of course name.
        """
        donelist = ("CREATE TABLE IF NOT EXISTS donelist ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "date TEXT NOT NULL, "
                    "course TEXT NOT NULL, "
                    "duration TEXT NOT NULL)")

        course = ("CREATE TABLE IF NOT EXISTS course ("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                  "name TEXT NOT NULL UNIQUE)")

        with self.con:
            self.cur.execute(donelist)
            self.cur.execute(course)

    def show(self, table: str):
        """  Show table """
        if table == self.course:
            ret = self.cur.execute('SELECT * FROM course').fetchall()
        elif table == self.donelist:
            ret = self.cur.execute('SELECT * FROM donelist').fetchall()
        else:
            raise RuntimeError("No such table.")
        return ret

    def insert_course(self, courses: List[str]):
        """ Insert course name.

        Insert course name into the 'course' table.
        Insertion of the course name which is already registered will be discarded.
        """
        for elem in courses:
            with self.con:
                self.con.execute('INSERT INTO course(name) VALUES (?)', (elem,))
                print("Add '{}' in course.".format(elem))

    def insert_donelist(self, date: str, course: str, duration: str):
        """ Insert donelist.

        Insert donelist into the 'donelist' table.
        The course name must be a registered name in the 'course' table.
        """
        check_course_name = self.con.execute('SELECT name FROM course WHERE name=?', (course,))
        check_course_name = check_course_name.fetchall()
        check_duplicate = self.con.execute(
            'SELECT date course FROM donelist WHERE date=? AND course=?', (
                date,
                course,
            ))
        check_duplicate = check_duplicate.fetchall()

        if not check_course_name:
            raise RuntimeError("No such course in 'course' table.")

        if check_duplicate:
            raise RuntimeError("Record already exists in 'donelist' table.")

        with self.con:
            self.con.execute('INSERT INTO donelist(date, course, duration) VALUES (?, ?, ?)', (
                date,
                course,
                duration,
            ))
            print("Add '{} {} {}' in donelist.".format(date, course, duration))

    def remove_course(self, course: str):
        """ Remove course name from 'course' table. """
        ret = self.con.execute('SELECT name FROM course WHERE name=?', (course,))
        check = ret.fetchall()

        if not check:
            raise RuntimeError("No such course in 'course' table.")

        with self.con:
            self.cur.execute('DELETE FROM course WHERE name=?', (course,))
            print("Removed '{}' from course.".format(course))

    def remove_donelist(self, date: str, course: str):
        """ Remove record from 'donelist' table.

        Search record by date and course name and if found matched record, it will be removed.
        """
        ret = self.con.execute('SELECT date, course FROM donelist WHERE date=? AND course=?', (
            date,
            course,
        ))
        check = ret.fetchall()

        if not check:
            raise RuntimeError("No such record in 'donelist' table.")

        with self.con:
            self.cur.execute('DELETE FROM donelist WHERE date=? AND course=?', (
                date,
                course,
            ))
            print('Removed record.')
