import re

from urlwatch import filters
from urlwatch import jobs
from urlwatch import reporters

#
#  This model suppresses all the dynamic variation in the state sites
#  by manipulating the DOM.
#
#  The hard states get their own functions but most of the work is generalized.
#
#  It tries to make the minimum set of changes required.
#
#  public function is:
#      text = regularize_text(text)
#

from typing import List, Union
from lxml import html, etree

def safe_starts_with(val: Union[str, None], prefix: str) -> bool:
    if val == None: return False
    return val.startswith(prefix)

def safe_contains(val: Union[str, None], prefix: str) -> bool:
    if val == None: return False
    return prefix in val

def check_title(elem: html.Element, txt: str) -> bool:
    titles = elem.xpath('//title')
    if titles == None: return False
    for t in titles:
        if safe_contains(t.text, txt): return True
    return False

def regularize_if_la(elem: html.Element) -> bool:
    " special case for lousiana "
    
    if not check_title(elem, "Louisiana Department of Health"): return False

    def clobber(xelem: html.Element):
        if "id" in xelem.attrib: del xelem.attrib["id"]
        if "class" in xelem.attrib: del xelem.attrib["class"]
        if "aria-label" in xelem.attrib: del xelem.attrib["aria-label"]

        if xelem.tag == "script":
            xelem.text = "[removed]"
        elif xelem.tag == "link":
            xelem.attrib["href"] = "[removed]"
            xelem.attrib["data-bootloader-hash"] = "[removed]"
        elif xelem.tag == "a":
            xelem.attrib["href"] = "[removed]"
            if "ajaxify" in xelem.attrib: del xelem.attrib["ajaxify"]
        elif xelem.tag == "img":
            xelem.attrib["src"] = "[removed]"

        for ch in xelem: clobber(ch)

    clobber(elem)
    return True

def regularize_if_co_data(elem: html.Element) -> bool:
    " special case for colorado data url "

    if not check_title(elem, "Colorado COVID-19 Fast Facts"): return False

    def clobber(xelem: html.Element):
        if xelem.attrib.get("id"): xelem.attrib["id"] = ""
        if xelem.attrib.get("class"): xelem.attrib["class"] = ""

        if xelem.tag == "script" and xelem.text != None:
            if xelem.attrib.get("nonce") != None:
                xelem.attrib["nonce"] = "[removed]"
                xelem.text = "[removed]"
        elif xelem.tag == "style":
            if xelem.attrib.get("nonce") != None:
                xelem.attrib["nonce"] = "[removed]"
            elif safe_starts_with(xelem.text, ".lst-kix"):
                xelem.text = "[removed]"            
        elif xelem.tag == "img":
            if xelem.attrib["alt"] == "Colorado Public Health logo":
                xelem.attrib["src"] = "[removed]"                 
        elif xelem.tag == "a":
            if safe_contains(xelem.attrib.get("href"), "urldefense.proofpoint.com"):
                xelem.attrib["href"] = "[removed]"

        for ch in xelem: clobber(ch)

    clobber(elem)
    return True

def regularize_other(elem: html.Element):
    " other cases "

    if elem.tag == "input":
        # AZ
        if elem.attrib.get("type") == "hidden":
            elem.attrib["value"] = "[removed]"

    elif elem.tag == "div":
        # CA
        if elem.attrib.get("id") == "DeltaFormDigest":
            elem.text = "[removed]"
            while len(elem) > 0: elem.remove(elem[0])
        # IL
        elif safe_starts_with(elem.attrib.get("class"), "view view-tweets"):          
            elem.attrib["class"] = "[removed]"
        # OH
        elif safe_contains(elem.attrib.get("class"), " id-"):          
            elem.attrib["class"] = "[removed]"

    elif elem.tag == "script":

        # CO
        if safe_starts_with(elem.text, "jQuery.extend(Drupal.setting"):
            elem.text = "[removed]"
        elif safe_starts_with(elem.text, "window.NREUM"):
            elem.text = "[removed]"
        # OH
        elif safe_contains(elem.text, "var WASReqURL = ") or safe_contains(elem.text, "wpModules.theme.WindowUtils"):
            elem.text = "[removed]"
        elif safe_contains(elem.attrib.get("src"), "/wps/contenthandler"):
            elem.attrib["src"] = "/wps/contenthandler"
        # KY
        elif safe_contains(elem.text, "var formDigestElement = "):
            elem.text = "[removed]"
        elif safe_contains(elem.text, "RegisterSod("):
            elem.text = "[removed]"
        # MO and NJ
        elif safe_contains(elem.attrib.get("src"), "_Incapsula_Resource"):
            elem.attrib["src"] = "/_Incapsula_Resource"
        # NE
        elif safe_contains(elem.text, "var g_correlationId = '"):
            elem.text = "[removed]"
        # PA
        elif safe_contains(elem.text, "var MSOWebPartPageFormName = 'aspnetForm'"):
            elem.text = "[removed]"
        # RI
        elif safe_contains(elem.text, 'window["blob') or safe_contains(elem.text, 'window["bob'):
            elem.text = "[removed]"
        # TX
        elif safe_starts_with(elem.attrib.get("id"), "EktronScriptBlock"):
            elem.attrib["id"] = "EktronScriptBlock"
            elem.text = "[removed]"
    elif elem.tag == "noscript":        
        # RI and WA
        elem.text = ""
        while len(elem) > 0: elem.remove(elem[0])
    elif elem.tag == "meta":
        # CT
        if elem.attrib.get("name") == "VIcurrentDateTime":
            elem.attrib["content"] = "[removed]"
    elif elem.tag == "link":
        # OH
        if safe_starts_with(elem.attrib.get("href"), "/wps/portal/gov"):
            elem.attrib["id"] = "[removed]"
            elem.attrib["href"] = "[removed]"
    elif elem.tag == "a":
        # OH
        if elem.attrib.get("class") == "left-navigation__link":
            elem.attrib["href"] = "[removed]"
            elem.text = ""
    elif elem.tag == "body":
        # KY
        if safe_starts_with(elem.attrib.get("class"), "brwsr-safari"):
            elem.attrib["class"] = "brwsr-safari"

    for ch in elem:
        regularize_other(ch)

def regularize(data, method, options):
    " regularize html content for cov-19 state sites "

    if type(data) == bytes:
        doc = html.fromstring(data)
    elif type(data) == str:
        doc = html.fromstring(data.encode())
    elif type(data) == html.Element:
        doc = data 
    else:
        raise Exception(f"Invalid input type ({type(data)}, should be str, bytes, or html.Element")

    if regularize_if_la(doc):
        pass
    elif regularize_if_co_data(doc):
        pass
    else:
        regularize_other(doc)

    if type(data) == bytes:
        content = html.tostring(doc)
    elif type(data) == str:
        content = html.tostring(doc).decode()
    return content

class Cov19RegularizeFilter(filters.FilterBase):
    """Remove items that vary with every request for COV19 state reporting sites"""

    __kind__ = 'cov19regularize'

    def filter(self, data, subfilter=None):

        if subfilter is None:
            method = 're'
            options = {}
        elif isinstance(subfilter, dict):
            method = subfilter.pop('method')
            options = subfilter
        elif isinstance(subfilter, str):
            method = subfilter
            options = {}

        return regularize(data, method=method, options=options)