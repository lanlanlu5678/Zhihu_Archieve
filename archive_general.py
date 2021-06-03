#coding=utf-8

from bs4 import BeautifulSoup
import requests
import random
import time
import lxml
import re
import os


def crawl_zhihu(url, atype, imgflag, linkflag):
    
    mb = BeautifulSoup(open('template/Article.html', 'r', encoding='utf-8'), 'lxml')

    h = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
        'Accept-Encoding': 'gzip, deflate', 
        'Cookie': 'SESSIONID=DOmOjnyKAdFNSo4MNp3O3hcRtEsTuSKdxwitUTHQNln; JOID=VlEUAk7ZeULbu5tHQtzl0OVvcdFWtj8Phv35FgSpICCJi_UjOJqKEL63nk9GNEQ0Xyv1h0QyR4qzSShKPEk5PeQ=; osd=UFoRBUPfckfctp1MR9vo1u5qdtxQvToIi_vyEwOkJiuMjPglM5-NHbi8m0hLMk8xWCbzjEE1Soy4TC9HOkI8Ouk=; SESSIONID=qZE3uLDgRc73XIoivFFEYDQyrNiAxIrK21pzypMqjUD; JOID=VlAXAEOu8tJH7ZqhL6liQ3o3cjs4wLaeFab58mjTqrIU0vnEVw8MjiDtnKol8cIESCNgHqXEBwJa6iQrqFCNuY8=; osd=W1ATA0ij8tZE5pehK6ppTnozcTA1wLKdHqv59mvYp7IQ0fLJVwsPhS3tmKku_MIASyhtHqHHDA9a7icgpVCJuoQ=; _zap=1d41f72b-c947-4462-83cf-1a6a7f09713d; _xsrf=UcS62NUitMZXofbQai6zOXRu98ppzy8d; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1616229097,1616230418,1616306151,1616308895; d_c0="ADAaBM_vmhGPTgnRn5czYKGuvpM2snGk6wY=|1595235405"; _ga=GA1.2.1547157586.1595235440; q_c1=3a32177a4fd14d30a45a181024d55ad9|1615014477000|1595235412000; tst=f; __utma=51854390.1547157586.1595235440.1603864489.1603864489.1; __utmz=51854390.1603864489.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/427689825; __utmv=51854390.100-1|2=registration_date=20150121=1^3=entry_date=20150121=1; z_c0="2|1:0|10:1610798544|4:z_c0|92:Mi4xSUVUcUFBQUFBQUFBTUJvRXotLWFFU1lBQUFCZ0FsVk4wQ1B3WUFBQlBSVklVekk1czlYOUEtQnBGc2o0MU9KOV93|44039a8f6a13b4ea1dd99ad554afa3553dd08d16b736c2d3bd75a4183cdfba87"; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1616317179; KLBRSID=ca494ee5d16b14b649673c122ff27291|1616317370|1616306146; SESSIONID=bNMYGoYFqTjR4oirqDiYvb27jwzxXY7tC11F53IYhrW; JOID=VF4QAkzyDCUg-GSXdPWdsREqjAxmkEFsf74LzTaCWEx2ygr-Bf3ncUf5Z5B2ZvhVpOMyv3dY7KiqHWA0ancOSLY=; osd=VloSB0LwCCcl9maTdvCTsxUoiQJklENpcbwPzzOMWkh0zwT8Af_if0X9ZZV4ZPxXoe0wu3Vd4qquH2U6aHMMTbg=',
        'Host': 'www.zhihu.com', 
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }

    pich = {
        'Accept': 'image/webp,*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'pic4.zhimg.com',
        'TE': 'Trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    pich['Referer'] = url

    with open('template/Article.html', 'r', encoding='utf-8') as f:
        t = f.read()

    r = requests.get(url,headers=h)
    s = BeautifulSoup(r.content.decode(), 'lxml')

    for i in mb.main.find_all('div', {'class': 'cover-content'}):
        mb_header = i
        break
    # title
    title = s.main.meta['content']
    mb_header.div.h1.string = title
    # author
    for i in s.main.find_all('span', {'class': 'UserLink AuthorInfo-name'}):
        if len(i.contents) > 1:
            mb_header.div.div.a['href'] = 'https:' + i.a['href']
            mb_header.div.div.a.string = i.a.string
        else:
            mb_header.div.div.a.string = i.string

    # article
    for i in mb.main.find_all('div', {'id': 'post-content'}):
        mb_body = i
        break
    for span in s.main.find_all('span'):
        if span.has_attr('class') and span['class'][0] == 'RichText':

            # link card
            for c in span.find_all(True, {'data-draft-type': 'link-card'}, recursive=False):
                if linkflag:
                    link_link = 'https:' + re.sub(r'h.+?A', '', c['href'])
                    c['href'] = link_link
                    # link_tag = s.new_tag('a')
                    # link_tag['href'] = link_link
                    # c.replace_with(link_tag)
                else:
                    c.decompose()
            
            # imgs
            figs = span.find_all('figure')
            for fig in figs:
                if imgflag:
                    img = fig.find_all('img', recursive=False)[0]['data-actualsrc']
                    imgc = '1'
                    while len(imgc) < 167:
                        imgc = requests.get(img, headers=pich).content
                    img = re.findall('http.+/(.+?)\?', img)[0]
                    img = time.strftime('%Y%m%d%M', time.localtime()) + img
                    with open(atype+'/imgs/'+img, 'wb') as f:
                        f.write(imgc)
                    img_tag = s.new_tag('img')
                    img_tag['src'] = 'imgs/' + img
                    img_tag['alt'] = r'[你瞅啥]'
                    fig.replace_with(img_tag)
                    img_tag.wrap(s.new_tag('p'))
                    time.sleep(random.random())
                else:
                    fig.decompose()

            for i in span.find_all('div', {'class': 'RichText-ZVideoLinkCardContainer'}):
                i.decompose()
            cnum = len(span.contents)
            for i in range(cnum):
                mb_body.append(span.contents[0])
            
            break


    # date
    for i in s.main.find_all('div', {'class': 'ContentItem-time'}):
        date_tag = s.new_tag('a')
        date_tag['style'] = 'font-size:20px;'
        date_tag['href'] = url
        date_tag.string = i.span.string
        mb_body.append(date_tag)
        date_tag.wrap(s.new_tag('br'))

    return title[:-1], mb.prettify()


def crawl_zhzl(url, atype, imgflag, linkflag):

    mb = BeautifulSoup(open('template/Article.html', 'r', encoding='utf-8'), 'lxml')

    h = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
        'Accept-Encoding': 'gzip, deflate', 
        'Cookie': 'SESSIONID=eE3DQGNUXVsRmKBy7bkpMtMMEtU6Qp4tFpb43721L01; JOID=UloRAUIU5SVl0NZ4YxZ-tlMNO-l2J7sXALCDLD1wkG1arZEbH3AAkAfb0nhuB-ALd_4zm7oLpCWmb5jD8ztrxN0=; osd=UFEcAUIW7ihl0NRzbhZ-tFgAO-l0LLYXALKIIT1wkmZXrZEZFH0AkAXQ33huBesGd_4xkLcLpCetYpjD8TBmxN0=; _zap=1d41f72b-c947-4462-83cf-1a6a7f09713d; _xsrf=UcS62NUitMZXofbQai6zOXRu98ppzy8d; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1622512842,1622514018,1622603232,1622728701; d_c0="ADAaBM_vmhGPTgnRn5czYKGuvpM2snGk6wY=|1595235405"; _ga=GA1.2.1547157586.1595235440; q_c1=3a32177a4fd14d30a45a181024d55ad9|1620437338000|1595235412000; tst=f; __utma=51854390.1547157586.1595235440.1603864489.1603864489.1; __utmv=51854390.100-1|2=registration_date=20150121=1^3=entry_date=20150121=1; z_c0="2|1:0|10:1610798544|4:z_c0|92:Mi4xSUVUcUFBQUFBQUFBTUJvRXotLWFFU1lBQUFCZ0FsVk4wQ1B3WUFBQlBSVklVekk1czlYOUEtQnBGc2o0MU9KOV93|44039a8f6a13b4ea1dd99ad554afa3553dd08d16b736c2d3bd75a4183cdfba87"; tshl=; KLBRSID=9d75f80756f65c61b0a50d80b4ca9b13|1622730080|1622728699; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1622730079; SESSIONID=1X4niWRXmwN9vNaz4E3j7X4ytz4Vfd1NZWv7vS46wwM; JOID=UVsVB0h4F90BcZvzRn-HSTCic2lUSUztaBjMohoVYJA8ANWSP4XPZmZxmPRFbGK9rBZ_RUID2i9S38xIQpkv51U=; osd=VF0dAEN9EdUGep71TniMTDaqdGJRT0TqYx3Kqh0eZZY0B96XOY3IbWN3kPNOaWS1qx16Q0oE0SpU18tDR58n4F4=',
        'Host': 'zhuanlan.zhihu.com', 
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }

    pich = {
        'Accept': 'image/webp,*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'pic4.zhimg.com',
        'TE': 'Trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    pich['Referer'] = url

    with open('template/Article.html', 'r', encoding='utf-8') as f:
        t = f.read()

    r = requests.get(url,headers=h)
    s = BeautifulSoup(r.content.decode(), 'lxml')

    # # debug
    # with open('t.html', 'w', encoding='utf-8') as f:
    #     print(s.prettify(), file=f)

    art = s.article
    for i in mb.main.find_all('div', {'class': 'cover-content'}):
        mb_header = i
        break
    # titile
    title = art.h1.string
    mb_header.div.h1.string = title
    # author
    for m in art.div.div.find_all('meta', recursive=False):
        if m['itemprop'] == 'name':
            mb_header.div.div.a.string = m['content']
        elif m['itemprop'] == 'url':
            mb_header.div.div.a['href'] = m['content']


    # article
    for i in mb.main.find_all('div', {'id': 'post-content'}):
        mb_body = i
        break
    for div in art.find_all('div'):
        if div.has_attr('class') and div['class'][0] == 'RichText':

            # link card
            for c in div.find_all(True, {'data-draft-type': 'link-card'}, recursive=False):
                if linkflag:
                    link_link = 'https:' + re.sub(r'h.+?A', '', c['href'])
                    c['href'] = link_link
                    # link_tag = s.new_tag('a')
                    # link_tag['href'] = link_link
                    # c.replace_with(link_tag)
                else:
                    c.decompose()
            
            # imgs
            figs = div.find_all('figure')
            for fig in figs:
                if imgflag:
                    img = fig.find_all('img', recursive=False)[0]['data-actualsrc']
                    imgc = requests.get(img, headers=pich).content
                    img = re.findall('http.+/(.+)', img)[0]
                    img = time.strftime('%Y%m%d%M', time.localtime()) + img
                    with open(atype+'/imgs/'+img, 'wb') as f:
                        f.write(imgc)
                    img_tag = s.new_tag('img')
                    img_tag['src'] = 'imgs/' + img
                    img_tag['alt'] = r'[你瞅啥]'
                    fig.replace_with(img_tag)
                    img_tag.wrap(s.new_tag('p'))
                    time.sleep(random.random())
                else:
                    fig.decompose()

            cnum = len(div.contents)
            for i in range(cnum):
                if div.contents[0].has_attr('class') and div.contents[0]['class'] == 'RichText-ZVideoLinkCardContainer':
                    div.contents[0].decompose()
                else:
                    mb_body.append(div.contents[0])
            
            break


    return title, mb.prettify()

def crawling(url, atype, imgflag, linkflag):
    source = re.findall(r'//(.+?)/', url)[0]

    if source == 'www.zhihu.com':
        title, content = crawl_zhihu(url, atype, imgflag, linkflag)
    elif source == 'zhuanlan.zhihu.com':
        title, content = crawl_zhzl(url, atype, imgflag, linkflag)
    elif source == 'www.guancha.cn':
        title, content = crawl_guancha(url, atype, imgflag, linkflag)

    edit_date = time.strftime('%Y-%m-%d', time.localtime())
    
    with open(atype+'/'+edit_date+'_'+title+'.html','w', encoding='utf-8') as f:
        print(content,file=f)




def translate_markdown():

    filelist = os.listdir('the_md')

    with open('template/Markdown.html', 'r', encoding='utf-8') as f:
        t = f.read()

    for fi in filelist:
        if 'html' in fi:
            with open('the_md/'+fi, 'r', encoding='utf-8') as f:
                s = f.read()
            body = re.findall(r'<body class="vscode-light">(.+?)</body>', s, flags=re.DOTALL)[0]
            s = re.sub(r'thezjccontent', body, t)

            with open('个人笔记/'+fi, 'w', encoding='utf-8') as f:
                f.write(s)

if __name__ == '__main__':

    atype_list = ['class0', 'class1', 'class2', 'class3']

    crawling('zhihu answer link or zhuanlan link',
                                                                        atype_list[],
                                                                        0,  # img flag
                                                                        0)  # link flag


    # translate_markdown()
