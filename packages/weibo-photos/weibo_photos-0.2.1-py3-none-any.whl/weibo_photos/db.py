import sqlite3

class SQLiteHelper(object):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()
    
    def print_error_msg(self, e):
        print('An error occurred:', e.args[0])
    
    def build_question_mark(self, count):
        question_mark = ''
        for i in range(count):
            if question_mark != '':
                question_mark += ','
            question_mark += '?'
        return question_mark

    def check_exists(self):
        assert self.cursor.arraysize == 1
        try:
            result = self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            self.print_error_msg(e)
            return False
        if result == 1:
            return True
        return False
    
    def check_table_exists(self, table_name):
        sql = 'SELECT COUNT(*) FROM sqlite_master where type="table" and name=?'
        try:
            self.cursor.execute(sql, (table_name,))
        except sqlite3.Error as e:
            self.print_error_msg(e)
            return False
        return self.check_exists()
    
    def check_row_exists(self, table_name, field_name, field_value):
        sql = 'SELECT COUNT(*) FROM %s where %s=?' % (table_name, field_name)
        try:
            self.cursor.execute(sql, (field_value,))
        except sqlite3.Error as e:
            self.print_error_msg(e)
            return False
        return self.check_exists()

    def clear_table(self, table_name):
        sql = 'DELETE FROM ?'
        try:
            self.cursor.execute(sql, table_name)
            self.conn.commit()
        except sqlite3.Error as e:
            self.print_error_msg(e)

    def create_albums_table(self):
        sql = '''CREATE TABLE ALBUMS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            caption TEXT NOT NULL,
            comments_count INTEGER NOT NULL,
            likes_count INTEGER NOT NULL,
            photos_count INTEGER NOT NULL,
            retweets_count INTEGER NOT NULL,
            cover_photo_id TEXT NOT NULL,
            cover_pic TEXT NOT NULL,
            created_at TEXT NOT NULL,
            description TEXT NOT NULL,
            is_favorited INTEGER NOT NULL,
            is_private INTEGER NOT NULL,
            status INTEGER NOT NULL,
            type INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            updated_at_int INTEGER NOT NULL
        )'''
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            self.print_error_msg(e)
    
    def insert_albums_table(self, album):
        album_id = album['album_id']
        uid = album['uid']
        caption = album['caption']
        photos_count = album['count']['photos']
        comments_count = album['count']['comments']
        likes_count = album['count']['likes']
        retweets_count = album['count']['retweets']
        cover_photo_id = album['cover_photo_id']
        cover_pic = album['cover_pic']
        created_at = album['created_at']
        description = album['description']
        is_favorited = album['is_favorited']
        is_private = album['is_private']
        status = album['status']
        timestamp = album['timestamp']
        types = album['type']
        updated_at = album['updated_at']
        updated_at_int = album['updated_at_int']
        sql = 'INSERT INTO ALBUMS VALUES(NULL, %s)' % self.build_question_mark(18)
        values = (album_id, uid, caption, comments_count, likes_count, photos_count, 
                retweets_count, cover_photo_id, cover_pic, created_at, description, 
                is_favorited, is_private, status, timestamp, types, updated_at, updated_at_int)
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except sqlite3.Error as e:
            self.print_error_msg(e)
        
    def create_photos_table(self):
        sql = '''CREATE TABLE PHOTOS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_id TEXT NOT NULL,
            album_id TEXT NOT NULL REFERENCES ALBUMS(album_id),
            uid TEXT NOT NULL,
            caption TEXT NOT NULL,
            caption_render  TEXT NOT NULL,
            clicks_count INTEGER NOT NULL,
            comments_count INTEGER NOT NULL,
            likes_count INTEGER NOT NULL,
            retweets_count INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            from TEXT NOT NULL,
            geo_description TEXT NOT NULL,
            is_cover INTEGER NOT NULL,
            is_favorited INTEGER NOT NULL,
            is_liked INTEGER NOT NULL,
            latitude INTEGER NOT NULL,
            longitude INTEGER NOT NULL,
            longtitude INTEGER NOT NULL,
            mid TEXT NOT NULL,
            original_time INTEGER NOT NULL,
            pic_host TEXT NOT NULL,
            pic_name TEXT NOT NULL,
            pic_pid TEXT NOT NULL,
            pic_type INTEGER NOT NULL,
            pid TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT NOT NULL,
            tags TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            types INTEGER NOT NULL,
            updated_at TEXT NOT NULL,
            visible TEXT NOT NULL,
        )
        '''
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            self.print_error_msg(e)

    def insert_photos_table(self, photo):
        photo_id = photo['photo_id']
        album_id = photo['album_id']
        uid = photo['uid']
        caption = photo['caption']
        caption_render = photo['caption_render']
        clicks_count = photo['count']['clicks']
        comments_count = photo['count']['comments']
        likes_count = photo['count']['likes']
        retweets_count = photo['count']['retweets']
        created_at = photo['created_at']
        froms = photo['from']
        geo_description = photo['geo_description']
        is_cover = photo['is_cover']
        is_favorited = photo['is_favorited']
        is_liked = photo['is_liked']
        latitude = photo['latitude']
        longitude = photo['longitude']
        longtitude = photo['longtitude']
        mid = photo['mid']
        original_time = photo['original_time']
        pic_host = photo['pic_host']
        pic_name = photo['pic_name']
        pic_pid = photo['pic_pid']
        pic_type = photo['pic_type']
        pid = photo['pid']
        source = photo['source']
        status = photo['status']
        tags = photo['tags']
        timestamp = photo['timestamp']
        types = photo['type']
        updated_at = photo['updated_at']
        visible = photo['visible']

        values = (photo_id, album_id, uid, caption, caption_render,
                clicks_count, comments_count, likes_count, retweets_count, created_at,
                froms, geo_description, is_cover, is_favorited, is_liked, latitude,
                longitude, longtitude, mid, original_time, pic_host, pic_name, pic_pid,
                pic_type, pid, source, status, tags, timestamp, types, updated_at, visible)
        sql = 'INSERT INTO PHOTOS VALUES(NULL, %s)' % self.build_question_mark(32)
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except sqlite3.Error as e:
            self.print_error_msg(e)


if __name__ == "__main__":
    helper = SQLiteHelper('D:/test.db')
    s = helper.build_question_mark(14)
    print(s)
    res = helper.check_table_exists('COMPANY')
    res = helper.check_table_exists('company')
    res = helper.check_row_exists('COMPANY', 'name', 'bug')
    res = helper.check_row_exists('t_student', 'id', 1)
    x = 1
