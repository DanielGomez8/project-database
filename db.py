"""
This module contains example code for basic SQLite usage.
Feel free to modify this file in any way.
"""
import sqlite3

# on import create or connect to an existing db
# and turn on foreign key constraints
conn = sqlite3.connect("globus_challenge.db", check_same_thread=False)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")
conn.commit()


def initialize_db():
    """
    Creates tables in the database if they do not already exist.
    Make sure to clean up old .db files on schema changes.
    """
    try:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                owner_username TEXT NOT NULL,
                project_name TEXT NOT NULL
            );
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                comment_id TEXT PRIMARY KEY,
                project_id TEXT,
                commenter_id TEXT NOT NULL,
                commenter_username TEXT NOT NULL,
                message TEXT NOT NULL
            );
            """
        )
        conn.commit()
    except Exception as e:
        print(e)


def insert_project(project):
    """
    Create a new project into the projects table
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(project_id,owner_id,owner_username,project_name)
              VALUES(?,?,?,?) '''
    c.execute(sql, project)
    conn.commit()
    return c.lastrowid

def insert_comment(comment):
    """
    Create a new comment into the comment table
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO comments(comment_id,project_id,commenter_id,commenter_username,message)
              VALUES(?,?,?,?,?) '''
    c.execute(sql, comment)
    conn.commit()
    return c.lastrowid

def get_project(project_id):
    """
        Get existing project from the projects table
        :param project_id:
        :return: project info
        """
    c.execute(" SELECT * FROM projects WHERE project_id=?", (project_id,))
    rows = c.fetchall()
    return None if not rows else rows[0]

def get_all_comments(project_id):
    """
        Get existing project from the projects table
        :param project_id:
        :return: project info
        """
    c.execute(" SELECT * FROM comments WHERE project_id=?", (project_id,))
    rows = c.fetchall()
    return None if not rows else rows


def delete_project(project_id):
    """
            Delete existing project from the projects table and all its comments from comments table
            :param project_id:
            :return: project info
            """
    c.execute(" DELETE FROM projects WHERE project_id=?", (project_id,))
    c.execute(" DELETE FROM comments WHERE project_id=?", (project_id,))
    conn.commit()

def get_num_projects():
    """
    Example of a simple SQL query using SQLite
    """
    c.execute("SELECT COUNT(project_id) FROM projects")
    return c.fetchone()[0]
