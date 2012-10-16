"""
    urlresolver XBMC Addon
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
"""

from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re
import urllib2, urllib
from urlresolver import common

class YoutubeResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "youtube"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()
        
        
    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        try:
            link = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error(self.name + '- got http error %d fetching %s' %
                                   (e.code, web_url))
            return False
         
        sequence = re.compile('yt\.preload\.start\("(.+?)"\);').findall(link)
        print len(sequence)
        
        #newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/', '/')
        #print newseqeunce
        
        for pre_link in sequence:
            pre_link_1 = urllib.unquote(pre_link).decode('utf8').replace('\\/', '/')
            print pre_link_1
            pre_link_1 = pre_link_1.replace("\u0026", "&")
            pre_link_1 = pre_link_1.replace(",", "%2C")
            link1 = self.net.http_GET(pre_link_1).content
        
        url_link1 = re.compile('"url_encoded_fmt_stream_map": "(.+?)"').findall(link)
        #url_link2 = urllib.unquote(url_link1[0]).decode('utf8').replace('\\/', '/')
        url_link2 = url_link1[0]
        #url_link1 = urllib.unquote(url_link1).decode('utf8').replace('\\/', '/')
        print url_link2
        
        
        #url_link3 = re.compile('itag=[1-9][0-9]\\u0026url=(.+?),').findall(url_link2)
        url_link3 = url_link2.split(",")
        print len(url_link3)
        for url_link4 in url_link3:
            if url_link4.find("itag=18")>=0:
                break
        print url_link4.decode('utf8')
        
        url_link5 = url_link4.split("\u0026")
        print len(url_link5)
        
        for url_link6 in url_link5:
            if url_link6.find("url=")>=0:
                break
        print url_link6.decode('utf8')
        
        for url_link7 in url_link5:
            if url_link7.find("sig=")>=0:
                break
        print url_link7.decode('utf8')
        url_link7 = url_link7.replace("sig=", "&signature=")
        
        url_link6 = urllib.unquote(url_link6).decode('utf8').replace('\\/', '/')
        
        url_link6 = url_link6.replace('url=', '')
        #url_link6 = url_link6.replace('%2C', ',')
        
        print url_link6
        
        videoUrl = url_link6 + url_link7 + " | Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
        
        return videoUrl


    def get_url(self, host, media_id):
        return 'http://youtube.com/watch?v=%s' % media_id
        
        
    def get_host_and_id(self, url):
        if url.find('?') > -1:
            queries = common.addon.parse_query(url.split('?')[1])
            video_id = queries.get('v', None)
        else:
            r = re.findall('/([0-9A-Za-z_\-]+)', url)
            if r:
                video_id = r[-1]
        if video_id:
            return ('youtube.com', video_id)
        else:
            common.addon.log_error('youtube: video id not found')
            return False
        
        
    def valid_url(self, url, host):
        return re.match('http://(((www.)?youtube.+?(v|embed)(=|/))|' +
                        'youtu.be/)[0-9A-Za-z_\-]+', 
                        url) or 'youtube' in host or 'youtu.be' in host

