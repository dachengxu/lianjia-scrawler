from flask import Flask
from jinja2 import Environment, PackageLoader
from scrawler import settings
from peewee import *


app = Flask(__name__)

database = MySQLDatabase(
    settings.DBNAME,
    host=settings.DBHOST,
    port=settings.DBPORT,
    user=settings.DBUSER,
    passwd=settings.DBPASSWORD,
    charset='utf8',
    use_unicode=True,
)



@app.route('/')
def hello_world():
    jinja_env = Environment(loader=PackageLoader('static', 'templates'))
    jinja_env.tests['startswith']=unicode.startswith

    template = jinja_env.get_template('index.tmpl')

    sql = '''
    SELECT * FROM ershoufang.houseinfo
    WHERE
        SUBSTR(validdate, 1, 10) NOT IN (SELECT 
                SUBSTR(MAX(validdate), 1, 10)
            FROM
                ershoufang.houseinfo)
    ORDER BY validdate; 
    '''
    xxx = database.execute_sql(sql)
    return template.render(description=xxx.description, rows=xxx.fetchall())


if __name__ == '__main__':
    app.run()