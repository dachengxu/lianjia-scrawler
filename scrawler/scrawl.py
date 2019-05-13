# -*- coding: UTF-8 -*-
import settings
from scrawler import core, model


def get_communitylist(city):
    res = []
    for community in model.Community.select():
        if community.city == city:
            res.append(community.title)
    return res

if __name__ == "__main__":
    regionlist = settings.REGIONLIST  # only pinyin support
    city = settings.CITY
    model.database_init()
    #core.GetHouseByRegionlist(city, regionlist)
    #core.GetRentByRegionlist(city, regionlist)
    # Init,scrapy celllist and insert database; could run only 1st time
    #core.GetCommunityByRegionlist(city, regionlist)
    #communitylist = get_communitylist(city)  # Read celllist from database
    #core.GetSellByCommunitylist(city, communitylist)
    communitylist = [u'合景叠翠峰',u'尹山湖韵佳苑', u'保利居上', u'保利悦玺']
    core.GetHouseByCommunitylist(city, communitylist)
    core.GetSellByCommunitylist(city, communitylist)
