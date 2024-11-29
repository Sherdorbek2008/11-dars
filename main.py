import psycopg2

class DataBase:
    def __init__(self):
        self.db = psycopg2.connect(
            database='11-uyu ishi',
            user='postgres',
            password='1',
            host='localhost',
        )

    def manager(self, sql, *args, commit=False, fetchone=False, fetchall=False):
        with self.db as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    result = db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
            return result


    def create_tebles(self):
        sql='''
        CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL,
        description TEXT
        );
        
        CREATE TABLE news (
        id SERIAL PRIMARY KEY,
        category_id INTEGER REFERENCES categories(category_id), 
        title VARCHAR(200) NOT NULL,  
        content TEXT NOT NULL,  
        published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        is_published BOOLEAN DEFAULT FALSE 
        );
        
        CREATE TABLE IF NOT EXISTS coments(
            id SERIAL PRIMARY KEY,
            news_id INTEGER REFERENCES news(id),
            author_name VARCHAR (100),
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        self.manager(sql, commit=True)


    def alter_table(self):
        sql='''
        ALTER TABLE news
        ADD COLUMN news_views INTEGER DEFAULT 0;
        ALTER TABLE coments
        ALTER COLUMN author_name TYPE TEXT;
        '''
        self.manager(sql, commit=True)

    def insert_into(self):
        sql='''
        INSERT INTO categories (category_name, description) VALUES
        ('Texnologiya', 'Texnologiya sohasidagi yangiliklar va rivojlanishlar'),
        ('Sport', 'Sport musobaqalari va voqealar haqida yangiliklar'),
        ('Sog‘liq', 'Sog‘liqni saqlash, tibbiyot va salomatlik haqida ma’lumotlar');
        
        INSERT INTO news (category_id, title, content, published_at, is_published) VALUES
        (1, '2024 Yildagi Sun’iy Intellekt Inqilobi', 'Bu yil sun’iy intellekt sohasida katta yutuqlar kutilmoqda...', CURRENT_TIMESTAMP, TRUE),
        (2, '2024 Yilgi Jahon Chempionati', '2024 yilgi Yozgi Olimpiya o‘yinlari ajoyib bo‘ladi...', CURRENT_TIMESTAMP, TRUE),
        (3, '2024 Yilda Sog‘lom Ovqatlanish', '2024 yilda sog‘lom turmush tarzini amalga oshirish uchun maslahatlar...', CURRENT_TIMESTAMP, TRUE);

        
        INSERT INTO coments (news_id, author_name, comment_text, created_at) VALUES
        (1, 'Ali', 'Bu sun’iy intellektdagi yirik yangilik juda ajoyib! Uning sanoatga ta’sirini kutib qolaman.', CURRENT_TIMESTAMP),
        (2, 'Bobur', 'Jahon chempionati har doim qiziqarli bo‘ladi. Umid qilamanki, jamoam g‘alaba qozonadi!', CURRENT_TIMESTAMP),
        (3, 'Shahlo', 'Sog‘lom ovqatlanish bo‘yicha juda yaxshi maslahatlar. Ba’zi tavsiyalarni sinab ko‘raman.', CURRENT_TIMESTAMP);
        '''
        self.manager(sql,commit=True)

    def update(self):
        sql='''
        UPDATE news  set news_views= news_views + 1;
        UPDATE news
        SET is_published = TRUE
        WHERE published_at <= CURRENT_TIMESTAMP - INTERVAL '1 day'
        AND is_published = FALSE;
        '''
        self.manager(sql,commit=True)

    def delete(self):
        sql='''
        DELETE FROM coments WHERE created_at<= CURRENT_TIMESTAMP- INTERVAL '1 year';
        '''
        self.manager(sql,commit=True)

    def select(self):
        sql='''
        SELECT 
        n.id AS news_id, 
        n.title AS news_title, 
        c.category_name AS name
        FROM news n
        JOIN categories c ON n.category_id = c.category_id;
        
        SELECT * FROM news JOIN categories  ON news.category_id = categories.category_id WHERE category_name = 'Technology';
        
        SELECT * FROM news LIMIT 5;
        
        SELECT * FROM news WHERE news_views BETWEEN 10 AND 100 
        
        SELECT * FROM coments WHERE author_name LIKE 'A%';
        
        SELECT * FROM coments WHERE author_name IS NULL;
        
        SELECT categories.category_name, COUNT(*) AS news_count
        FROM news
        JOIN categories ON news.category_id = categories.category_id
        GROUP BY categories.category_name;
        '''
        return self.manager(sql,fetchall=True)

    def unique(self):
        sql='''
        ALTER TABLE news
        ADD CONSTRAINT unique_title UNIQUE (title);
        '''
        self.manager(sql,commit=True)
db=DataBase()
# db.create_tebles()
# db.alter_table()
# db.insert_into()
# db.update(
# db.delete()
# print(db.select())
# db.unique()

