import re
from ..utils import config, get_longest_common_sub_string
from lxml.html import HtmlElement
from ..defaults import TITLE_HTAG_XPATH, TITLE_SPLIT_CHAR_PATTERN


class TitleNewspaperExtractor:
    def extract_by_xpath(self, element, title_xpath):
        if title_xpath:
            title_list = element.xpath(title_xpath)
            if title_list:
                return title_list[0].strip()
            else:

                return ''
        return ''

    def extract_by_title(self, element):
        title_list = element.xpath('//title/text()')
        if not title_list:
            return ''
        title = re.split(TITLE_SPLIT_CHAR_PATTERN, title_list[0])
        if title:
            if len(title[0]) >= 4:
                if self.black_url_list_url(title[0]):
                    return ""
                return title[0]
        else:
            return ''

    def black_url_list_url(self,title) -> bool:
        black_title_list = ["。","作者:","收藏本文", "推荐好友", "本报记者", "上一篇", "下一篇", "日报", "晚报", "晨报", "数字报", "时间:", "本版新闻", "一版","打印本页","导航"]
        for black_url in black_title_list:
            if re.findall(black_url,title):
                return True
        else:
            return False

    def extract_by_htag(self, element):
        title_list = element.xpath(TITLE_HTAG_XPATH)

        if not title_list:
            return ""
        if self.black_url_list_url(title_list[0]):
            return ""
        if len(title_list[0].strip())>3:
            return title_list[0].strip()
        else:
            return ""

    def extract_by_htag_and_title(self, element: HtmlElement) -> str:
        """
        一般来说，我们可以认为 title 中包含新闻标题，但是可能也含有其他文字，例如：
        GNE 成为全球最好的新闻提取模块-今日头条
        新华网：GNE 成为全球最好的新闻提取模块

        同时，新闻的某个 <h>标签中也会包含这个新闻标题。

        因此，通过 h 标签与 title 的文字双向匹配，找到最适合作为新闻标题的字符串。
        但是，需要考虑到 title 与 h 标签中的文字可能均含有特殊符号，因此，不能直接通过
        判断 h 标签中的文字是否在 title 中来判断，这里需要中最长公共子串。
        :param element:
        :return:
        """
        # 第一结队 优先权重高的标题标签
        h_tag_texts_list1 = element.xpath('(//h1//text() | //founder-title//text() |//h2//text())')
        for h_tag_text in h_tag_texts_list1:
            h_tag_text = h_tag_text.strip()
            if self.black_url_list_url(h_tag_text):
                continue
            if len(h_tag_text)>3:
                return h_tag_text
        # 第二结队 优先权重占比低
        h_tag_texts_list2 = element.xpath('(//h3//text() | //h4//text() | //h5//text())')
        for h_tag_text in h_tag_texts_list2:
            h_tag_text = h_tag_text.strip()
            if self.black_url_list_url(h_tag_text):
                continue
            if len(h_tag_text)>3:
                return h_tag_text
        return ""
        """
            lcs = get_longest_common_sub_string(title_text, h_tag_text)
            if len(lcs) > len(news_title):
                news_title = lcs
        return news_title if len(news_title) > 4 else ''
        """
    def re_title(self,html):
        title = ""
        is_title = False
        if not is_title:
            title = "".join(re.findall("<founder-title>(.*?)</founder-title>", html, re.S | re.M | re.I))
            title = title.strip()
            if len(title)>1:
                if len(title)>20 and "<" in title:
                    title = re.sub(r'<!--.*?-->', '', title)
                    title = re.sub(r'<[^>]+>','', title)
                    is_title = True
                    return title
                else:
                    return title
        if not is_title:
            title = "".join(re.findall("<!--<npm:article-title>-->(.*?)<!--</npm:article-title>", html, re.S | re.M | re.I))
            title = title.strip()
            if len(title)>1:
                is_title = True
                return title
        return title




    def extract(self, element: HtmlElement,html, title_xpath="") -> str:
        title_xpath = title_xpath or config.get('title', {}).get('xpath')
        # print("extract_by_htag_and_title:",self.extract_by_htag_and_title(element))
        # print("extract_by_title:",self.extract_by_title(element))
        # print("extract_by_htag:",self.extract_by_htag(element))
        title = (self.extract_by_xpath(element, title_xpath)
                 or self.extract_by_htag(element)
                 or self.extract_by_title(element)
                 or self.extract_by_htag_and_title(element)
                 or self.re_title(html)
                 )
        return title
