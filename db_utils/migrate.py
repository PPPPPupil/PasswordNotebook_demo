import sqlite3


def migrate():
    conn = sqlite3.connect("./db.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS `tbl_password` ;""")
    cursor.execute("""CREATE TABLE `tbl_password` (
    `id` integer primary key not null ,
    `username` varchar(256) not null ,
    `password` varchar(256) not null ,
    `place` varchar(256) not null     
    );""")


class MyConnection(object):
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def add_record(self, *args):
        self.cursor.execute("""INSERT INTO `tbl_password`(`username`, `password`, `place`) VALUES(?, ?, ?) """, args)
        self.conn.commit()

    def delete_record(self, id=None):
        if id is not None:
            self.cursor.execute("""DELETE FROM `tbl_password` WHERE `id`=?""", (id,))
            self.conn.commit()

    def modify_record(self,*args):
        self.cursor.execute("""UPDATE `tbl_password` SET `username`=?,  `password`=? , `place`=? WHERE `id`=?""",args)
        self.conn.commit()

    def query_records(self, place=None):
        if place is None:
            self.cursor.execute("""SELECT `id`, `username`, `password`, `place` FROM `tbl_password`""")
        else:
            self.cursor.execute("""SELECT `id`, `username`, `password`, `place` FROM `tbl_password` WHERE `place`=?""",
                                (place,))

        return self.cursor.fetchall()



if __name__ == '__main__':
    # migrate()
    my_conn = MyConnection()
    my_conn.delete_record("3")
    my_conn.add_record("my_name", "my_password", "TestCode")

    print(my_conn.query_records())
