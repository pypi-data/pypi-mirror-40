# -*- coding: utf-8 -*-
import re
import time
import random

def minify_html(html,
                strict_spaces=True,
                no_space_between_tags=True,
                preserve=True,
                remove_comments=True,
                html5_min_attr=True,
                html5_emptytags=True
                ):
    return Htmlfy().minify(html,strict_spaces,no_space_between_tags,preserve,remove_comments,html5_min_attr,html5_emptytags)

def minify_html_file(source_path,minified_path,
                strict_spaces=True,
                no_space_between_tags=True,
                preserve=True,
                remove_comments=True,
                html5_min_attr=True,
                html5_emptytags=True
                ):
    
    return Htmlfy().minify_file(source_path,minified_path,strict_spaces,no_space_between_tags,preserve,remove_comments,html5_min_attr,html5_emptytags)


class Htmlfy():

    _preserves = None
    _preserves_count = None

    def __init__(self):
        self._preserves = {}
        self._preserves_count = 0

    def minify(self,html,
                strict_spaces=True,
                no_space_between_tags=True,
                preserve=True,
                remove_comments=True,
                html5_min_attr=True,
                html5_emptytags=True):

        
        if remove_comments:
            html = self._remove_comments(html)
        if preserve:    
            html = self._save_preserves(html)
            html = self._save_preserves_inline(html)
        if strict_spaces:
            html = self._strict_spaces(html)
        if no_space_between_tags:
            html = self._no_space_between_tags(html)
        if html5_min_attr:
            html = self._html5_min_attr(html)
        if html5_emptytags:
            html = self._html5_emptytags(html)
        if preserve: 
            html = self._restore_preserves(html)
        html = self._strict_overall(html)
        return html

    def minify_file(self,source_path,minified_path,strict_spaces=True,no_space_between_tags=True,preserve=True,remove_comments=True,html5_min_attr=True,html5_emptytags=True):
       
        with open(source_path, "r") as f:
            html = f.read()
            f.close()
        
        min_html = self.minify(html,strict_spaces,no_space_between_tags,preserve,remove_comments,html5_min_attr,html5_emptytags)
        
        with open(minified_path, "w") as f:
            f.write(min_html)
            f.close()

    def _strict_overall(self,input_html):
        return re.sub(r"(^\s+)|(\s+$)",'',input_html)

    def _strict_spaces(self,input_html):
        input_html = re.sub(r"\s{2,}",' ',input_html)
        input_html =  re.sub(r"(>[^<]+?)\s<",r"\1<",input_html)
        input_html =  re.sub(r">\s([^>]+?<)",r">\1",input_html)
        input_html =  re.sub(r"{\s(.+?)\s}",r"{\1}",input_html)
        return input_html

    def _no_space_between_tags(self,input_html):
        return re.sub(r">\s+?<",'><',input_html)

    def _remove_comments(self,input_html):
        input_html = re.sub(r"(^\s*?//.+?\r*\n)|(\s+?//.+?$)",'',input_html,flags=re.M)
        input_html = re.sub(r"(^\s*/\*.+?\*/\s*\r*\n)|(/\*.+?\*/)",'',input_html,flags=re.M|re.S)
        input_html = re.sub(r"(<!--[^!\[].+?-->)",'',input_html,flags=re.M|re.S)
        return input_html

    def _html5_min_attr(self,input_html):
        return re.sub(r"(selected|disabled|checked)=\".+?\"",r"\1",input_html)

    def _html5_emptytags(self,input_html):
        return re.sub(r"(<.+?)(\s*/)(>)",r"\1\3",input_html)

    def _save_preserves(self,input_html):
        input_html = re.sub(r"<script.*?>.+?</script>",self._save_preserves_callback,input_html,flags=re.I|re.M|re.S)
        input_html = re.sub(r"<pre.*?>.+?</pre>",self._save_preserves_callback,input_html,flags=re.I|re.M|re.S)
        input_html = re.sub(r"<textarea.*?>.+?</textarea>",self._save_preserves_callback,input_html,flags=re.I|re.M|re.S)
        return input_html

    def _save_preserve_add(self,html):
        self._preserves_count += 1
        preserve_name = "%s_%s" % (self._preserves_count,self._uniqid())
        self._preserves[preserve_name] = html
        return preserve_name

    def _save_preserves_callback(self,html_source):
        return "<preserve:%s>" % self._save_preserve_add(html_source.group(0))

    def _save_preserves_inline(self,input_html):
        input_html = re.sub(r"<\?(=|php).+?\?>",self._save_preserves_inline_callback,input_html,flags=re.I|re.M|re.S)
        return input_html

    def _save_preserves_inline_callback(self,html_source):
        return "{preserve:%s}" % self._save_preserve_add(html_source.group(0))

    def _restore_preserves(self,html_preserved):
        return re.sub(r"[<{]preserve:(\d+?_[a-z0-9]+?)[>}]",self._restore_preserves_callback,html_preserved)

    def _restore_preserves_callback(self,preserve_name):
        return self._preserves[preserve_name.group(1)]

    def _uniqid(self):
        return str(hex(int(time.time()))[8:10] + hex(int(time.time()*1000000) % 0x100000)[5:7] + hex(int(random.random()*100000))[2:5])


    
