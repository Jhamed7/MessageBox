from sqlite3 import connect
from datetime import datetime


class DataBase:

    @staticmethod
    def insert(name, text):
        try:
            my_con = connect('messagebox.db')
            my_cursor = my_con.cursor()

            time = datetime.now()
            time = time.strftime("%Y-%m-%d %H:%M")
            my_cursor.execute(f"INSERT INTO messages(name, text,time) VALUES('{name}','{text}', '{time}')")
            my_con.commit()
            my_con.close()
            return True
        except:
            False

    @staticmethod
    def select():
        try:
            my_con = connect('messagebox.db')
            my_cursor = my_con.cursor()
            my_cursor.execute("SELECT * FROM messages")
            result = my_cursor.fetchall()
            my_con.close()
            return result
        except:
            return []

    @staticmethod
    def delete(id_):
        my_con = connect('messagebox.db')
        my_cursor = my_con.cursor()
        my_cursor.execute(f"DELETE FROM messages WHERE id={id_}")
        my_con.commit()
        my_con.close()

    @staticmethod
    def delete_all():
        my_con = connect('messagebox.db')
        my_cursor = my_con.cursor()
        my_cursor.execute(f"DELETE FROM messages")
        my_con.commit()
        my_con.close()

    @staticmethod
    def update():
        pass

    @staticmethod
    def last_message_time_check(name, resteiction):
        my_con = connect('messagebox.db')
        my_cursor = my_con.cursor()
        my_cursor.execute(f"SELECT time FROM messages WHERE name='{name}'")
        result = my_cursor.fetchall()
        my_con.close()

        if result:
            last_msg_time = result[-1][0]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

            last_sec = int(last_msg_time[-5:-3]) * 3600 + int(last_msg_time[-2:]) * 60
            current_sec = int(current_time[-5:-3]) * 3600 + int(current_time[-2:]) * 60

            if (current_time[0:4] > last_msg_time[0:4]) or (current_time[5:7] > last_msg_time[5:7]) or (
                    current_time[8:10] > last_msg_time[8:10]):
                return True, None
            elif abs(current_sec - last_sec) >= resteiction:
                return True, None
            else:
                return False, abs(resteiction - abs(current_sec - last_sec))
        else:  # first message of user
            return True, None
