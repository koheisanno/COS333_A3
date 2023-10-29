#-----------------------------------------------------------------------
# reg_db.py
# Author: Bob Dondero, Jacob Colchamiro, Kohei Sanno
#-----------------------------------------------------------------------

import contextlib
import sqlite3

DATABASE_URL = 'file:reg.sqlite?mode=ro'

# create custom exception to catch when no class matches id
class NoSuchClassError(Exception):
    pass

def connect_to_db(args, query_type):
    with sqlite3.connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            if query_type=='get_overviews':
                stmt_str = (
                    'SELECT classid, dept, coursenum, area, title '
                    'FROM crosslistings, courses, classes '
                    'WHERE courses.courseid==crosslistings.courseid '
                    'AND classes.courseid==courses.courseid '
                    r'AND dept LIKE ?  ESCAPE "\" '
                    r'AND coursenum LIKE ?  ESCAPE "\" '
                    r'AND area LIKE ?  ESCAPE "\" '
                    r'AND title LIKE ?  ESCAPE "\" '
                    'ORDER BY dept, coursenum, classid'
                )

                cursor.execute(stmt_str, args)

                table = cursor.fetchall()

            elif query_type=='get_detail':
                stmt_str = (
                    'SELECT classes.courseid, days, starttime, '
                    'endtime, bldg, roomnum '
                    'FROM classes WHERE classes.classid==?'
                )

                cursor.execute(stmt_str, [args])
                class_data = cursor.fetchone()

                if not class_data:
                    raise NoSuchClassError(('no class with classid '
                                    f'{args} exists'))

                course_id = class_data[0]

                stmt_str = ('SELECT area, title, descrip, prereqs '
                    f'FROM courses WHERE courses.courseid=={course_id}')

                cursor.execute(stmt_str)
                course_data = cursor.fetchone()

                stmt_str = ('SELECT dept, coursenum from crosslistings '
                    f'WHERE crosslistings.courseid=={course_id} '
                    'ORDER BY dept, coursenum')

                cursor.execute(stmt_str)
                dept_data = cursor.fetchall()

                stmt_str = ('SELECT profname from coursesprofs, profs '
                    f'WHERE coursesprofs.courseid=={course_id} '
                    'AND profs.profid==coursesprofs.profid '
                    'ORDER BY profname')

                cursor.execute(stmt_str)
                prof_data = cursor.fetchall()

                table = [class_data, course_data, dept_data, prof_data]

    return table
