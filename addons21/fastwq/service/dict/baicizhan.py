#-*- coding:utf-8 -*-
import json
import os
from collections import defaultdict
from ..base import *


@register([u'百词斩', u'Baicizhan'])
class Baicizhan(WebService):

    bcz_download_mp3 = True
    bcz_download_img = True

    def __init__(self):
        super(Baicizhan, self).__init__()

    def _get_from_api(self):
        url = u"http://mall.baicizhan.com/ws/search?w={}".format(self.quote_word)
        result = {
            "accent": u"",
            "img": u"",
            "mean_cn": u"",
            "st": u"",
            "sttr": u"",
            "tv": u"",
            "word": u"",
            "df": u'',
        }
        try:
            html = self.get_response(url, timeout=5)#urllib2.urlopen(url, timeout=5).read()
            result.update(json.loads(html))
        except:
            pass
        return self.cache_this(result)

    @export('发音')
    def fld_phonetic(self):
        url = u'http://baicizhan.qiniucdn.com/word_audios/{}.mp3'.format(self.quote_word)
        audio_name = get_hex_name(self.unique.lower(), url, 'mp3')
        if self.bcz_download_mp3:
            if os.path.exists(audio_name) or self.download(url, audio_name, 5):
                with open(audio_name, 'rb') as f:
                    if f.read().strip() == '{"error":"Document not found"}':
                        res = ''
                    else:
                        res = self.get_anki_label(audio_name, 'audio')
                if not res:
                    os.remove(audio_name)
            else:
                res = ''
            return res
        else:
            return url

    @export('音标')
    def fld_phon(self):
        return self._get_field('accent')

    @export('图片')
    def fld_img(self):
        url = self._get_field('img')
        if url and self.bcz_download_img:
            filename = url[url.rindex('/') + 1:]
            if os.path.exists(filename) or self.download(url, filename):
                return self.get_anki_label(filename, 'img')
        #return self.get_anki_label(url, 'img')
        return ''

    @export(u'象形' )
    def fld_df(self):
        url = self._get_field('df')
        if url and self.bcz_download_img:
            filename = url[url.rindex('/') + 1:]
            if os.path.exists(filename) or self.download(url, filename):
                return self.get_anki_label(filename, 'img')
        #return self.get_anki_label(url, 'img')
        return ''

    @export(u'中文释义')
    def fld_mean(self):
        return self._get_field('mean_cn')

    @export(u'英文例句')
    def fld_st(self):
        url=self._get_field('st')
        # str_list=url.split()
        # for i in range(len(str_list)):#对相应的word加粗,用于Anki遮挡
        #     if str_list[i].find(self.word)!=-1:
        #         # str_list[i]= "<b>"+self.word+"</b>"
        #         str_list[i]=str_list[i].replace(self.word, "<b>"+self.word+"</b>")
        #         break
        # return " ".join(str_list)
        return url.replace(self.word, "<b>"+self.word+"</b>")

    @export('例句翻译')
    def fld_sttr(self):
        return "<b>"+self._get_field('sttr')+"</b>"

    @export(u'单词tv')
    def fld_tv_url(self):
        video = self._get_field('tv')
        if video:
            return self.get_anki_label(video, 'video')
        return ''
    
    @export(u'图片2')
    def fld_img2(self):#返回HTML代码
        return "<img src="+self._get_field('img')+">"