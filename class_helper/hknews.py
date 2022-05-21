import urllib.request
import urllib.parse
import json

def urllibpost(url = None, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}, data = None):
    'A post method by urllib'
    data = urllib.parse.urlencode(data).encode('utf-8')
    try:
        req = urllib.request.Request(url=url,
                                data=data,
                                headers=headers,
                                method='POST')
    except:
        raise 'url is invalid'
    else:
        response = urllib.request.urlopen(req)
        if response.status == 200:
            return json.loads(response.read().decode('utf-8'))
        else:
            return {'error': response.status}

class HK:

    def _template(self, xid):
        r = urllibpost('http://www.hnkjedu.cn/posthome.aspx',data={
            'id':xid,
            'type': 'news',
            'cid': 5,
            'count': 26
        })
        templist = []
        if 'error' in r:
            return r
        
        tempt = r[0]['News_time']
        for i in r:
            if xid == 12 or xid == 22:
                News_url = 'http://www.hnkjedu.cn/show.aspx?id={}'.format(i['News_id'])
            if xid == 374:
                News_url = 'http://www.hnkjedu.cn/column_show.aspx?id=31&zid={}'.format(i['News_id'])
            if xid == 108:
                News_url = 'http://jwc.hnkjedu.cn/shownews.aspx?id={}'.format(i['News_id'])
            if xid == 111:
                News_url = 'http://kyzx.hnkjedu.cn/show.aspx?id={}'.format(i['News_id'])
            
            # 这个结构可以获取到最新的消息
            if i['News_time'] == tempt:
                templist.append({
                    "News_url": News_url,
                    "News_titleall": i['News_titleall'],
                    "News_time": i['News_time']
                })
        return templist

    def hkxw(self):
        """海科新闻"""
        self.data_hkxw = self._template(12)
        return self.data_hkxw

    def tzgg(self):
        """通知公告"""
        self.data_tzgg = self._template(22)
        return self.data_tzgg
    
    def ldjh(self):
        """领导讲话"""
        self.data_ldjh = self._template(374)
        return self.data_ldjh
    
    def jwtz(self):
        """教务通知"""
        self.data_jwtz = self._template(108)
        return self.data_jwtz
        
    def kytz(self):
        """科研通知"""
        self.data_kytz = self._template(111)
        return self.data_kytz
    
    def mtbd(self):
        """媒体报道"""
        r = urllibpost('http://www.hnkjedu.cn/posthome.aspx',data={
            'type': 'mtbd'
        })
        templist = []
        if 'error' in r:
            return r

        tempt = r[0]['News_time']
        for i in r:
            if i['News_time'] == tempt:
                templist.append({
                    "News_url": i['mtbd_link'],
                    "News_titleall": i['News_titleall'],
                    "News_time": i['News_time']
                })
        self.data_mtbd = templist
        return self.data_mtbd
    
    def __init__(self):
        self.data_hkxw = self.hkxw()
        self.data_tzgg = self.tzgg()
        self.data_mtbd = self.mtbd()
        self.data_ldjh = self.ldjh()
        self.data_jwtz = self.jwtz()
        self.data_kytz = self.kytz()

if __name__ == '__main__':
    hk = HK()
    print(hk.data_hkxw)
    print(hk.data_tzgg)
    print(hk.data_mtbd)
    print(hk.data_ldjh)
    print(hk.data_jwtz)
    print(hk.data_kytz)