import sqlite3
 
class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('user_posts.db')
        self.create_user_table()
        self.create_posts_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_posts_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "posts" (
          pid INTEGER PRIMARY KEY,
          post_title TEXT,
          posts_description TEXT,
          is_read boolean DEFAULT 0,
          is_deleted boolean DEFAULT 0,
          created_timestamp Date DEFAULT CURRENT_DATE,
          uid INTEGER FOREIGNKEY REFERENCES User(uid)
        );
        """

        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "users" (
        uid INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT NOT NULL, 
        useremail TEXT, 
        created_timestamp Date default CURRENT_DATE
        );
        """
        self.conn.execute(query)


class PostsModel:
    TABLENAME = "posts"

    def __init__(self):
        self.conn = sqlite3.connect('user_posts.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_uid(self, uid):
        where_clause = f"AND id={uid}"
        return self.list_items(where_clause)

    def create(self, params):
        print (params)
        query = f'insert into {self.TABLENAME} ' \
                f'(post_title, posts_description, UserId) ' \
                f'values ("{params.get("post_title")}","{params.get("posts_description")}",' \
                f'{params.get("uid")}")'
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, post_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted =  {1} " \
                f"WHERE id = {post_id}"
        print (query)
        self.conn.execute(query)
        return self.list_items()

    def update(self, post_id, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = " ".join([f'{column} = {value}'
                     for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {post_id}"
        self.conn.execute(query)
        return self.get_by_id(post_id)

    def list_items(self, where_clause=""):
        query = f"SELECT pid, post_title, posts_description, is_read " \
                f"from {self.TABLENAME} WHERE is_deleted != {1} " + where_clause
        print (query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class User:
    TABLENAME = "users"

    def create(self, name, email):
        query = f'insert into {self.TABLENAME} ' \
                f'(username, useremail) ' \
                f'values ({name},{email})'
        result = self.conn.execute(query)
        return result