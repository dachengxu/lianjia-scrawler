# -*- coding: utf8 -*-

from flask import Flask
from jinja2 import Environment, PackageLoader
from scrawler import settings
from peewee import *
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except Exception:
    pass


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

COMMUNITY_LIST = [u'合景叠翠峰', u'尹山湖韵佳苑', u'保利居上', u'保利悦玺']

@app.route('/')
def hello_world():
    return show_community(COMMUNITY_LIST[0])

@app.route('/xiaoqu/<community>')
def show_community(community):
    jinja_env = Environment(loader=PackageLoader('static', 'templates'))
    jinja_env.tests['startswith']=unicode.startswith

    template = jinja_env.get_template('index.tmpl')

    communitys = [community]
    for c in COMMUNITY_LIST:
        if c != community:
            communitys.append(c)

    datas = []
    datas.append(get_houseinfo_changed(community))
    datas.append(get_houseinfo_by_square(community))
    datas.append(get_houseinfo_xiajia(community))
    datas.append(get_houseinfo_sold(community))

    return template.render(communitys = communitys, datas = datas)


def get_houseinfo_xiajia(community):
    sql = u'''
        SELECT * FROM ershoufang.houseinfo
        WHERE community = %s AND
            SUBSTR(validdate, 1, 10) NOT IN (SELECT 
                    SUBSTR(MAX(validdate), 1, 10)
                FROM
                    ershoufang.houseinfo)
        ORDER BY validdate
    '''
    cursor = database.execute_sql(sql, (community,))
    return u'下架房源', cursor.description, cursor.fetchall()


def get_houseinfo_by_square(community, min_square = 80, max_square = 100):
    sql = u'''
        SELECT houseID,
            housetype,
            LEFT(floor, 1) AS floor,
            ROUND(totalPrice * 10000 / unitPrice) AS square,
            decoration,
            case 
                when locate("车位", title) > 0 then 1 
                else 0
            end as '车位',
            totalPrice, unitPrice, link
        FROM
            ershoufang.houseinfo
        WHERE
            community = %s
                AND totalPrice * 10000 / unitPrice BETWEEN %s AND %s
                AND SUBSTR(validdate, 1, 10) IN (SELECT 
                        SUBSTR(MAX(validdate), 1, 10)
                    FROM
                        ershoufang.houseinfo)
        ORDER BY square , decoration DESC , (unitPrice + 0);
    '''
    cursor = database.execute_sql(sql, (community, min_square, max_square))
    return u'{}-{}平在售房源'.format(min_square,max_square), cursor.description, cursor.fetchall()



def get_houseinfo_changed(community):
    sql = u'''
        SELECT * FROM
            (SELECT 
                houseId, COUNT(*), GROUP_CONCAT(totalPrice)
            FROM
                ershoufang.hisprice
            WHERE
                community = %s
            GROUP BY houseId
            HAVING COUNT(*) > 1) t
                LEFT JOIN
            houseinfo h ON t.houseId = h.houseId;
    '''
    cursor = database.execute_sql(sql, (community,))
    return u'价格变动的房源', cursor.description, cursor.fetchall()


def get_houseinfo_sold(community):
    sql = u'''
        SELECT * FROM ershoufang.sellinfo where community = %s order by dealdate desc;
    '''
    cursor = database.execute_sql(sql, (community,))
    return u'已售房源信息', cursor.description, cursor.fetchall()



if __name__ == '__main__':
    app.run()