'''
    t0mm0 test XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import re
import string
import sys
import urllib2
import urllib
import hashlib

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import urlresolver

import CommonFunctions


class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        #print "Cookie Manip Right Here"
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

def getASPCookie():
    url = 'http://online.film4vn.us/verify/enter-button.html?returnUrl=/'
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12 CNS_UA; AD_LOGON=4C47452E4E4554; (.NET CLR 3.5.30729)'
#    values = {'__EVENTTARGET' : '',
#              '__EVENTARGUMENT' : '',
#              '__VIEWSTATE' : '/wEPDwUKMjA0OTM4MTAwNGRk6/gi1r+te8ii+Gfus7DJ6/WrilY=',
#              '__EVENTVALIDATION' : '/wEWAgLas/iiBQKXt8D4AQjKVvCdBBvdahftoTWOBpnFyOMB',
#              'btnEnter' : 'Enter'}
    values = {'__RequestVerificationToken' : 'OhO0plxukS8gnryD9ekj3j1bVnAbdarvKQXBrditF7mb4x8Lm9mu2jBgip3XcrCeGOR6tUJXEImaqsd99km7WIxoFZVCz0rsD5ioes0a9HU59ujBIJLNiajUvMIizaatXmg0HA=='}
    headers = { 'User-Agent' : user_agent, 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language' : 'en-us,en;q=0.5','Accept-Encoding' : 'gzip,deflate','Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Connection' : 'keep-alive','Keep-Alive' : '115','Cookie' : '__RequestVerificationToken_Lw__=cIInOcGSRFVm4qxDw6igCu2YV7qwkI+FfEaVvwNusI0G6F6kLkKfR4n78kE6MF3ViQ+hZxfu2E+8ErROcON+LV8nyhwucKM0sqlpeFdTWucMV8jH03M3Ay48xbdvcxtcWdN0Pg==','Referer' : 'http://online.film4vn.us/verify/enter-button.html?returnUrl=/','Content-Type' : 'application/x-www-form-urlencoded'}


    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)


    redirect_handler = urllib2.HTTPRedirectHandler()

    cookieprocessor = urllib2.HTTPCookieProcessor()

    opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
    urllib2.install_opener(opener)

    response =urllib2.urlopen(req)
    
    return

def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())

def utf8decode(html):
    try:
        html1 = html.decode('utf-8','ignore')
        return html1
    except:
        print "Unicode error"
        return html

common = CommonFunctions
common.plugin = "veetv"

common.dbg = True # Default
common.dbglevel = 3 # Default

addon = Addon('plugin.video.t0mm0.test', sys.argv)
net = Net()

logo = os.path.join(addon.get_path(), 'art','logo.jpg')

base_url = 'http://tubeplus.me'

mode = addon.queries['mode']
play = addon.queries.get('play', None)

if play:
    url = addon.queries.get('url', '')
    
    #add resolve url for giaitri.com
    site = addon.queries.get('site', '')
    if site.find("giaitricom")>=0:
        v_url = urllib.unquote(net.http_GET(url).content)
        url = v_url[v_url.find("http://"):]
    
    
    host = addon.queries.get('host', '')
    media_id = addon.queries.get('media_id', '')
    #stream_url = urlresolver.resolve(play)
    stream_url = urlresolver.HostedMediaFile(url=url, host=host, media_id=media_id).resolve()
    addon.resolve_url(stream_url)

elif mode == 'resolver_settings':
    urlresolver.display_settings()

elif mode == 'test':
    url = "http://giaitri.com/new/index.php?cat=12"
    html = net.http_GET(url).content
    ret = common.parseDOM(html, "div", attrs = { "class": "s1'" })
    v_urls = common.parseDOM(ret, "a", attrs = { "class": "image_border" })
    print repr(v_urls)
    addon.add_video_item({'host': 'dailymotion.com','media_id':'xsla2x'},{'title': 'dailymotion test 1'})
    addon.add_video_item({'host': 'youtube.com','media_id':'_fUi2NnjPCE'},{'title': 'youtube test 1'})



elif mode == 'giaitricom_tap_play':
    tap_url = addon.queries.get('tap_url', '')  
    v_url = urllib.unquote(net.http_GET(tap_url).content)
    print v_url
    addon.add_video_item({'url': v_url[v_url.find("http://"):]},{'title': 'Play...'})
    
                
elif mode == 'giaitricom_tap_list':
    url = addon.queries.get('phim_url', '')
    html = utf8decode(net.http_GET(url).content)
    #print html.encode('ascii', 'xmlcharrefreplace')
    
    #page
    tap_page = int(addon.queries.get('page', '1'))
    print "tap_page::" + str(tap_page)
    
    #get tap_num
    pindex = html.find("var totalitems = ")
    s1 = html[pindex+17:pindex+22]
    tap_num = 1000
    try:
        tap_num = int(s1[0:s1.find(";")])   
    except:
        print "tap_num error..."
        
    print "tap_num::" + str(tap_num)
    
    #get tid
    pindex = url.find("id=")
    stemp = url[pindex + 3:]
    tid = stemp[:stemp.find("&")]
    print "tid::" + tid
    
    for i in range((tap_page-1)*20+1, min((tap_page-1)*20+21,tap_num+1)):
        tap_url = "http://giaitri.com/new/loadplayer.php?tid=" + tid + "&sid=" + str(i)
        #addon.add_directory({'mode': 'giaitricom_tap_play', 'tap_url' : tap_url}, {'title': 'Tap  ' + str(i)})
        addon.add_video_item({'url': tap_url, 'site' : 'giaitricom'},{'title': 'Tap  ' + str(i)})
    
    if tap_num > (tap_page*20):
        addon.add_directory({'mode': 'giaitricom_tap_list','phim_url' : url, 'page' : str(tap_page+1)}, {'title': 'Next page ...  ' + str(((tap_page)*20 +1)) + ' to ' + str(min(tap_num,(tap_page+1)*20))})
    
elif mode == 'giaitricom_cat':
    url = addon.queries.get('cat_url', '')
    
    #page
    cat_page = addon.queries.get('cat_page', '1')
    print "cat_page::" + cat_page
    
    url1 = url + "&page=" + cat_page
    
    html = utf8decode(net.http_GET(url1).content)
    
    ret = common.parseDOM(html, "div", attrs = { "class": "s1'" })
    if not ret:
        ret = common.parseDOM(html, "div", attrs = { "class": "s1_alt" })
        
    v_urls = common.parseDOM(ret, "a", attrs = { "class": "image_border" }, ret = "href")
    v_img_urls = common.parseDOM(ret, "img", attrs = { "class": "imgResize" }, ret = "src")
    v_title = common.parseDOM(ret, "img", attrs = { "class": "imgResize" }, ret = "title")
    if not v_img_urls:
        v_img_urls = common.parseDOM(ret, "img", attrs = { "border": "0" }, ret = "src")
        v_title = common.parseDOM(ret, "img", attrs = { "border": "0" }, ret = "title")
    
    #print repr(v_urls)
    for i in range(0, len(v_urls)):
        addon.add_directory({'mode': 'giaitricom_tap_list','phim_url' : v_urls[i], 'page' : '1'}, {'title': v_title[i]},img=v_img_urls[i].replace("thumb_default","default"))
     
    addon.add_directory({'mode': 'giaitricom_cat', 'cat_url' : url, 'cat_page' : str((int(cat_page)+1))}, {'title': 'Next page...'})
    
elif mode == 'giaitricom':
    url = "http://giaitri.com/new/index.php"
    html = utf8decode(net.http_GET(url).content)
    ret = common.parseDOM(html, "div", attrs = { "class": "dropmenudiv" })
    v_urls = common.parseDOM(ret, "a", ret = "href")
    v_names = common.parseDOM(ret, "a")
    for i in range(0, len(v_urls)):
        if v_names[i].find("<") > 0:
            cat_name = v_names[i][:v_names[i].find("<")]
        else:
            cat_name = v_names[i]
        addon.add_directory({'mode': 'giaitricom_cat', 'cat_url' : v_urls[i], 'cat_page' : '1'}, {'title': cat_name})
                
elif mode == 'film4vn':
    getASPCookie()
    response =urllib2.urlopen("http://online.film4vn.us/the-loai-phim-bo-han-quoc.html")
    print response.read()

elif mode == 'main':
    #addon.show_small_popup('t0mm0 test addon', 'Is now loaded enjoy', 6000,logo)
    
    addon.add_directory({'mode': 'giaitricom'}, {'title': 'GiaiTri.com'})
    addon.add_directory({'mode': 'film4vn'}, {'title': 'online.film4vn.us'})

if not play:
    addon.end_of_directory()


