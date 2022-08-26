import re
from .utils import html2element, normalize_text
from .extractor import CJM_ContentExtractor,  TimeExtractor, AuthorExtractor, ListExtractor,TitleNewspaperExtractor
from urllib.parse import urljoin
from .tool import *
from lxml import etree
def replace_by_img_tag(txt):
    begin = 0
    end = 0
    i = 1
    while True:
        end = txt.find('{img}', begin)
        if end == -1:
            break
        new = '\n{IMG:' + str(i) + '}\n'
        txt = txt.replace('{img}', new, 1)
        begin = end + len(new)
        i = i + 1
    return txt

def Get_md5(url):
    import hashlib
    a = hashlib.md5(url.encode())
    md5_str = a.hexdigest()
    return md5_str

class GeneralNewsExtractor:
    def extract(self,
                html,
                IsNewspaperParser = False,
                title_xpath='',
                author_xpath='',
                publish_time_xpath='',
                host='',
                body_xpath=''):

        # 对 HTML 进行预处理可能会破坏 HTML 原有的结构，导致根据原始 HTML 编写的 XPath 不可用
        # 因此，如果指定了 title_xpath/author_xpath/publish_time_xpath，那么需要先提取再进行
        # 预处理
        #增加稿件来源提取，采用正则方式
        source=''
        results = re.search(r">*\s*[　]*来源\s*[：\-:](</em>)*\s*(\S*?)((<)|(\s)|(/)|(，)|(）|\"))", html, re.M | re.I)

        if results:
            source= results.group(2)
            source=source.strip()
        CJM_html = html
        html = re.sub(r'<!--.*?-->', '', html, 0, re.S | re.M | re.I)

        normal_html = normalize_text(html)
        element = html2element(normal_html)
        title = TitleNewspaperExtractor().extract(element,html, title_xpath=title_xpath,)
        if IsNewspaperParser:
            title = TitleNewspaperExtractor().extract(element,html, title_xpath=title_xpath)
        publish_time = TimeExtractor.parse_time(html=html,url=host)
        author = AuthorExtractor().extractor(element, author_xpath=author_xpath)
        cjm_content_data = CJM_ContentExtractor().CJMContentExtraction(CJM_html)
        result = {'title': title,
                  'author': author,
                  'publish_time': publish_time,
                  'source':source,
                  'images': []
                  }

        if body_xpath.__len__()>0:
            html_pages = etree.HTML(html)
            content_html = html_pages.xpath(body_xpath)[0]
            content_data = etree.tostring(content_html, encoding='utf-8').decode()
            contents = re.sub("<img.*?src=.*?>", "{img}", content_data, 0, re.S | re.M | re.I)
            re_data = re.compile('>(.*?)<', re.S | re.M | re.I)
            content = re_data.findall(contents)
            content = "\n".join(content)
            result["content"] = replace_by_img_tag(content)
            result["body_html"] = content_data
            result["warn_info"] = "正常"
        else:
            result['body_html'] = cjm_content_data["body_html"]
            result['warn_info'] = cjm_content_data["warn_info"]
            content = re.sub("<img.*?src=.*?>", "{img}", result['body_html'], 0, re.S | re.M | re.I)
            content = replace_by_img_tag(content)
            re_data = re.compile('>(.*?)<', re.S | re.M | re.I)
            content = re_data.findall(content)
            result['content'] = "\n\t".join(content)
        result['body_html'] = re.sub("<a .*?href=\".*?\".*?>", "", result['body_html'], 0, re.S | re.M | re.I)
        result['body_html'] = re.sub("</a>", "", result['body_html'], 0, re.S | re.M | re.I)
        pics = re.findall("<img.*?src=\"(.*?)\".*?>", result['body_html'])
        pics_tag = re.findall("<img.*?src=\".*?\".*?>", result['body_html'])
        a = 0
        for pic in pics:
            img = pic
            # if len(pic)>0:
            pic_url = urljoin(host, pic)
            result['images'].append(pic_url)
            qny_img_url = "https://opinion-oss.jgwcjm.com/"+Get_md5(host)+"&"+Get_md5(pic_url)
            # onerror="javascript:this.src='';this.onerror=null"
            # regular_expression = '<img.*?src=\\"{}\\".*?>'.format(img)
            regular_expression = pics_tag[a]
            # print(regular_expression)

            # 不带图片样式案例
            # sub_img = '<img src="{}">'.format(qny_img_url)
            # 带图片样式案例
            src1 = "src=\"{}\"".format(img)
            src2 = "src=\"{}\"".format(qny_img_url)

            # sub_img = re.sub(src1,src2,regular_expression,re.S | re.I | re.M)
            # print("src1:{}".format(src1))
            # print("src2:{}".format(src2))
            sub_img = regular_expression.replace(src1,src2)
            # print("sub_img:{}".format(sub_img))
            # result['body_html'] = re.sub(regular_expression, sub_img, result['body_html'],0,re.S | re.I | re.M)
            result['body_html'] = result['body_html'].replace(regular_expression,sub_img)
            a+=1
        return result


class ListPageExtractor:
    def extract(self, html, feature):
        normalize_html = normalize_text(html)
        element = html2element(normalize_html)
        extractor = ListExtractor()
        return extractor.extract(element, feature)