import pymysql


class MysqlConnection(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    port=8889,
                                    user='root',
                                    password='root',
                                    db='scraper')

        self.cursor = self.conn.cursor()

    def close_spider(self):
        self.cursor.close()
        self.conn.close()
