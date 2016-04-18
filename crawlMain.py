# -*-  coding=utf8  -*-
import  requests,sys
from bs4 import BeautifulSoup
from PIL import Image 
from StringIO import StringIO
import time


def  getHtmlResponse(url):
    try:
        rel = requests.get(url)
    except requests.exceptions.ConnectionError:
         return None
    return rel

def  writeContentToFile(filename,data,mode='w'):
    m_mode = mode
    with open(filename,m_mode) as f:
        f.write(data)
    return True

def createImageFromUrl(url,path):
    import re
    filename = re.split("/|//", url)
    m_len = len(filename)
    m = re.match(".*\.jpg|.*\.gif",filename[m_len-1])
    if m is not None:
        time.sleep(0.1)
        res = requests.get(url)
        if res is not None:
            try:
                im = Image.open(StringIO(res.content))
                osfile =  path + filename[m_len-1]
                im.save(osfile)
            except IOError:
                print 'IOerror image, the current url is %s .',url
                pass

def  createImageFromUrls(urls,path):
    while  urls:
        url = urls.pop()
        import re
        filename = re.split("/|//", url)
        m_len = len(filename)
        m = re.match(".*\.jpg|.*\.gif",filename[m_len-1])
        if m is not None:
            time.sleep(0.1)
            print url
            m_data = url +'\n'
            writeContentToFile('imageUrls.txt',m_data,'a')
            res = getHtmlResponse(url)
            if res is not None:
                try:
                    im = Image.open(StringIO(res.content))
                    osfile =  path + filename[m_len-1]
                    im.save(osfile)
                except IOError:
                    print 'IOerror image, the current url is %s .',url
                    pass
        else:
            continue
    return True


def downImageFromUrls(urls,path):
        while  urls:
            url = urls.pop()
            import re
            filename = re.split("/|//", url)
            m_len = len(filename)
            m = re.match(".*\.jpg|.*\.gif",filename[m_len-1])
            if m is not None:
                time.sleep(0.1)
                osfile =  path + filename[m_len-1]
                try:
                    rel = requests.get(url, stream=True)
                    if rel.status_code == 200:
                        with open(osfile, 'wb') as f:
                            for chunk in rel.iter_content(1024):
                                f.write(chunk)
                except requests.exceptions.ConnectionError:
                    print 'requests is exceptions when request ',url
                    continue
                print 'the current url\'s status is ',url,rel.status_code
            else:
                print 'The url is filtered. ', url
        return True

if __name__  ==  '__main__':
    print "hello webCrawl."
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    # url = 'http://cl.clus.pw/htm_data/7/1512/1774220.html'
    url = "http://cl.clus.pw/thread0806.php?fid=7"
    urlcoding = 'gbk'
    r = getHtmlResponse(url)
    r.encoding = urlcoding

    writeContentToFile("study.html",r.text.encode('gbk'))
    img_path =  '/home/beyondkoma/work/gitProject/webCrawl/images/'

    # createImageFromUrl('http://i4.tietuku.com/408da328c806fa52.jpg',img_path)
    soup_html = BeautifulSoup(r.text,'html.parser')
    img_urls = []
    soup_html.find_all('img')
    for img_src in   soup_html.find_all('img'):
        img_urls.append(img_src['src'])
        
    # createImageFromUrls(img_urls,img_path)
        downImageFromUrls(img_urls,img_path)




