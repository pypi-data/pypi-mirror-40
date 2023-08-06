from lxml import etree
from readability import Document


class Parser(object):
    @staticmethod
    def raw_to_document(raw_html):
        return etree.HTML(raw_html)

    @staticmethod
    def xpath_select(selector, xpath_lan):
        return selector.xpath(xpath_lan)

    @staticmethod
    def html_select(raw_html, xpath_lan):
        doc = Document(raw_html)
        summary_html = doc.summary()
        # print(summary_html)
        selector = etree.HTML(summary_html)
        return selector.xpath(xpath_lan)
