from lxml.html.clean import Cleaner
from html import unescape
from lxml.html import HtmlElement, fromstring
from lxml import etree
import numpy as np
import unicodedata
import re


class CJM_ContentExtractor:

    TAGS_CAN_BE_REMOVE_IF_EMPTY = ['section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']

    USELESS_ATTR = {'share', 'contribution', 'copyright', 'copy-right', 'disclaimer', 'recommend', 'related', 'footer',
                    'comment', 'social', 'submeta', 'report-infor'}

    NOISE_NODE_TAG = ['html', 'head', 'body', 'script', 'table', 'select', 'form', 'textarea', 'img', 'object', 'a',
                      'iframe', 'link', 'meta', 'td', 'tr', 'strong', 'span', 'li', 'ul', 'input', 'embed', 'h1', 'h2',
                      'h3', 'h4', 'h5', 'title', 'noscript', 'em', 'p']

    punctuation = set('''！，。？、；：“”‘’《》%（）,.?:;'"!%()''')  # 常见的中英文标点符号
    endpunctuation = set('。')

    cleaner = Cleaner(style=True, scripts=True, comments=True, javascript=True, page_structure=False,
                      safe_attrs_only=False)  # Cleaner参数说明：

    def normalize_text(self,html):
        """
        使用 NFKC 对网页源代码进行归一化，把特殊符号转换为普通符号
        :param html:
        :return:
        """
        return unicodedata.normalize('NFKC', html)

    def count_punctuation_num(self,text):
        count = 0
        ecount = 0
        for char in text:
            if char in self.punctuation:
                count += 1
                if char in self.endpunctuation:
                    ecount += 1
        return count, ecount

    def count_text_tag(self,element, tag='p'):
        return len(self,element.xpath(f'.//{tag}'))

    def is_empty_element(self,node: HtmlElement):
        return not node.getchildren() and not node.text

    def remove_node(self,node: HtmlElement):
        """
        this is a in-place operation, not necessary to return
        :param node:
        :return:
        """
        parent = node.getparent()
        if parent is not None:
            parent.remove(node)

    def normalize_node(self,node: HtmlElement):
        # inspired by readability.
        if node.tag.lower() in self.TAGS_CAN_BE_REMOVE_IF_EMPTY and self.is_empty_element(node):
            self.remove_node(node)

        # merge text in span or strong to parent p tag
        if node.tag.lower() == 'p':
            etree.strip_tags(node, 'span')
            etree.strip_tags(node, 'strong')
        # if a div tag does not contain any sub node, it could be converted to p node.
        if node.tag.lower() == 'div' and not node.getchildren():
            node.tag = 'p'
        if node.tag.lower() == 'span' and not node.getchildren():
            node.tag = 'p'

        class_name = node.get('class')
        if class_name:
            if class_name in self.USELESS_ATTR:
                self.remove_node(node)

    def CJMContentExtraction(self,html):
        html_cleaner = self.cleaner.clean_html(re.sub('</?(br?|span).*?>', '', html))
        html_normalize = self.normalize_text(html_cleaner)

        html = etree.HTML(html_normalize)
        tree = html.getroottree()
        body_node = html.xpath('//body')[0]

        all_nodes = body_node.xpath('//*')

        node_info = dict()
        xpath2node = dict()
        index= 0
        for node in all_nodes:
            index += 1/len(all_nodes)
            if node.tag not in self.NOISE_NODE_TAG:
                self.normalize_node(node)
                node_hash = hash(node)
                lti_text_list = []
                lti_text = ''
                for element in node.xpath('.//a'):
                    text = element.text
                    if not text:
                        continue
                    clear_text = re.sub(' +', ' ', text, flags=re.S)
                    clear_text = clear_text.replace('\n', '')
                    lti_text_list.append(clear_text)
                    lti_text += clear_text
                ti_text_list = []
                ti_text = ''
                ti_count = 0
                lti_count = 0
                sum_ti_punctuation = 0
                sum_lti_punctuation = 0
                sum_ti_end_punctuation = 0
                sum_lti_end_punctuation = 0
                shorttext_cnt = 0
                longtext_cnt = 0
                for text in node.xpath('.//text()'):
                    text = text.strip()
                    if not text:
                        continue
                    clear_text = re.sub(' +', ' ', text, flags=re.S)
                    clear_text = clear_text.replace('\n', '').strip()
                    ti_text += '\n' + clear_text
                    ti_count += 1
                    count_punctuation, end_count_punctuation = self.count_punctuation_num(clear_text)
                    if '版权' in clear_text or '转载' in clear_text or '免责' in clear_text or '书面授权' in clear_text or '未经授权' in clear_text or '特别声明' in clear_text:
                        count_punctuation = 0
                        end_count_punctuation = 0
                    sum_ti_punctuation += count_punctuation
                    sum_ti_end_punctuation += end_count_punctuation
                    text1 = re.sub('[^\u4e00-\u9fa5！，。？、；：“”‘’《》%（）,.?:;\'"!%()]', '', text, flags=re.S)
                    if len(text1) > 0:
                        if len(text1) < 15:
                            shorttext_cnt += 1
                        elif len(text1) >= 15 or (len(text1) > 8 and '。' in text1):
                            longtext_cnt += 1
                    if text in lti_text_list:
                        lti_count += 1
                        ti_text_list.append(('lti_text', len(clear_text), count_punctuation, clear_text))
                        #sum_ti_punctuation += count_punctuation
                        sum_lti_end_punctuation += end_count_punctuation
                    else:
                        ti_text_list.append(('ti_text', len(clear_text), count_punctuation, clear_text))
                ShortTextRate = shorttext_cnt / (ti_count + 1)
                PunctuaDensity = (sum_ti_punctuation - sum_lti_punctuation) / (ti_count - lti_count + 1)
                if ti_text != '' and node.tag not in ['p'] and ShortTextRate < 2.0 and len(ti_text.lstrip('\n')) > 10 and PunctuaDensity > 0.0:
                    text_tag_count = longtext_cnt #- count_text_tag(node, tag='p')
                    TextDensity = (len(ti_text) - len(lti_text)) / (ti_count - lti_count + 1)
                    EndPunctuaDensity = (sum_ti_end_punctuation - sum_lti_end_punctuation) / (sum_ti_punctuation - sum_lti_punctuation + 1)
                    LinkDensity = len(lti_text) / len(ti_text)
                    LinkRate = lti_count / (ti_count + 1.0)
                    ComDensity = TextDensity * np.log10(text_tag_count + 1.25) * PunctuaDensity * (1.0 - ShortTextRate) * (20.0 / (1.0 + np.exp(LinkDensity*10))) * (20.0 / (1.0 + np.exp(LinkRate*10))) * EndPunctuaDensity
                    path = tree.getpath(node)
                    node_info[node_hash] = dict.fromkeys(('ComDensity', 'ShortTextRate', 'index', 'LinkDensity', 'LinkRate', 'TextDensity', 'PunctuaDensity', 'EndPunctuaDensity', 'text_tag_count', 'xpath', 'ti_text', 'body_source_code', 'tag'))
                    node_info[node_hash]['ComDensity'] = ComDensity
                    node_info[node_hash]['ShortTextRate'] = ShortTextRate
                    node_info[node_hash]['index'] = index
                    node_info[node_hash]['LinkDensity'] = LinkDensity
                    node_info[node_hash]['LinkRate'] = LinkRate
                    node_info[node_hash]['TextDensity'] = TextDensity
                    node_info[node_hash]['PunctuaDensity'] = PunctuaDensity
                    node_info[node_hash]['EndPunctuaDensity'] = EndPunctuaDensity
                    node_info[node_hash]['text_tag_count'] = text_tag_count
                    node_info[node_hash]['xpath'] = path
                    node_info[node_hash]['ti_text'] = ti_text.lstrip('\n')
                    node_info[node_hash]['tag'] = node.tag

                    xpath2node[path] = node
        if len(node_info) > 0:
            node_info_list = sorted(node_info.items(), key=lambda x: (x[1]['ComDensity'], x[1]['EndPunctuaDensity']), reverse=True)

            EndPunctuaDensity = node_info_list[0][1]['EndPunctuaDensity']
            org_path = node_info_list[0][1]['xpath']
            Path = re.sub(r'(/p(\[[0-9]+\])*(/(font|section)\[[0-9]+\])*$)|(/[^dD][a-zA-Z]{1,6}\[[0-9]\]$)', '', org_path)
            body_source_code = ''
            if xpath2node.get(Path) != None:
                body_source_code = unescape(etree.tostring(xpath2node.get(Path), encoding='utf-8').decode())
                # 获取主体内容并清洗
                body_source_code = re.sub(r'</?div.*?>', '', body_source_code)
                body_source_code = re.sub('</?(br?|span).*?>', '', body_source_code)
                body_source_code = re.sub('\n', '', body_source_code)
                body_source_code = re.sub('\r', '', body_source_code)

            #"""
            res = body_node.xpath(Path + '//*')
            ContentList = list()
            Link_tag_cnt = 0
            textline_cnt = 0
            short_text_cnt = 0
            for node in res:
                text = node.text
                tail = node.tail
                tag = node.tag
                if tag in ['script']:
                    continue
                if not text:
                    if tag in ['img', 'video', 'audio']:
                        images_list = node.xpath('./@_src') + node.xpath('./@src')
                        for image in images_list:
                            if len(image) < 200:
                                ContentList.append((tag, image))
                        if tail:
                            clear_text = re.sub('((^( |\n|\r|\t)+)|(( |\n|\r|\t)+$))', '', tail, flags=re.S)
                            clear_text = re.sub(' +', ' ', clear_text.replace('\n', ''), flags=re.S)
                            if clear_text != ' ' and clear_text != '' and clear_text != '  ':
                                ContentList.append((tag, clear_text))
                                text1 = re.sub('[^\u4e00-\u9fa5！，。？、；：“”‘’《》%（）,.?:;\'"!%()]', '', clear_text, flags=re.S)
                                if len(text1) > 0:
                                    textline_cnt += 1
                                    if len(text1) <= 8:
                                        short_text_cnt += 1
                                    if node.tag == 'a' and '。' not in clear_text:
                                        Link_tag_cnt += 1
                else:
                    if tail:
                        text += ' ' + tail
                    clear_text = re.sub('((^( |\n|\r|\t)+)|(( |\n|\r|\t)+$))', '', text, flags=re.S)
                    clear_text = re.sub(' +', ' ', clear_text.replace('\n', ''), flags=re.S)
                    if clear_text != ' ' and clear_text != '' and clear_text != '  ':
                        if clear_text in ['分享让更多人看到', '本文转自:', '相关新闻', '阅读下一篇:', '大小新闻,未经授权不得转载', '上一篇:', '扫一扫在手机打开当前页', '打印本页', '关闭窗口', '3176086-37771-43-工作动态', '下载附件:', '返回顶部']:
                            break
                        for clear_subtext in clear_text.split('\r\n'):
                            clear_subtext = re.sub('((^( |\n|\r|\t)+)|(( |\n|\r|\t)+$))', '', clear_subtext, flags=re.S)
                            clear_text = re.sub(' +', ' ', clear_text.replace('\n', ''), flags=re.S)
                            if clear_subtext != '':
                                ContentList.append((tag, clear_subtext))
                                text1 = re.sub('[^\u4e00-\u9fa5！，。？、；：“”‘’《》%（）,.?:;\'"!%()]', '', clear_text, flags=re.S)
                                if len(text1) > 0:
                                    textline_cnt += 1
                                    if len(text1) <= 8:
                                        short_text_cnt += 1

                                    if node.tag == 'a' and '。' not in clear_subtext:
                                        Link_tag_cnt += 1

            WarnInfo = "异常"
            if short_text_cnt / (textline_cnt - short_text_cnt + 1) < 2 and EndPunctuaDensity > 0 and Link_tag_cnt / (textline_cnt - Link_tag_cnt + 1) < 1.0:
                WarnInfo = "正常"
            #"""

            body_source_code = self.CleanBodyHtml(body_source_code)
            result = {
                      'body_html': body_source_code,
                      'warn_info': WarnInfo,
                      }

            return result
        return {"body_html":"","warn_info":"异常"}

    def CleanBodyHtml(self,body_html):
        body_html = re.sub(
            r'<p( [^\u4e00-\u9fa5]{0,100})?>[\t\n\r ]*.{0,3}(微信|手机).{0,2}扫一扫[\t\n\r ]*.{0,3}关注.{0,2}公众号[\t\n\r ]*.{0,3}</p( [^\u4e00-\u9fa5]{0,100})?>',
            '', body_html)
        body_html = re.sub(
            r'<p( [^\u4e00-\u9fa5]{0,100})?>[\t\n\r ]*.{0,3}(上一?篇)[\t\n\r ]*.{0,3}(下一?篇)[\t\n\r ]*.{0,3}</p( [^\u4e00-\u9fa5]{0,100})?>',
            '', body_html)
        body_html = re.sub(
            r'<p( [^\u4e00-\u9fa5]{0,100})?>[\t\n\r ]*.{0,3}([来稿]源于?|本文转自)[：|:| |丨|/]\s*[\t\n\r ]*([\u4e00-\u9fa5-_a-zA-Z]{1,8})[\t\n\r ]*.{0,3}</p( [^\u4e00-\u9fa5]{0,100})?>',
            '', body_html)
        return body_html