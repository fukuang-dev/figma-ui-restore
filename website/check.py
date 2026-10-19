#!/usr/bin/env python3
"""Check the actual generated pages, SEO relationships, links and public assets."""
from html.parser import HTMLParser
from pathlib import Path
import json
import hashlib
import re
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'dist/site'
BASE = 'https://fukuang-dev.github.io/figma-ui-restore/'
PREFIX = '/figma-ui-restore/'

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags=[];self.ids=set();self.h1=0;self.json=[];self.in_json=False;self.buffer='';self.title='';self.in_title=False
        self.feed(source)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append((tag,attrs))
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate HTML id'
            self.ids.add(attrs['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.in_title=True
        if tag=='script' and attrs.get('type')=='application/ld+json':self.in_json=True;self.buffer=''
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.in_json:self.buffer+=data
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='script' and self.in_json:self.json.append(json.loads(self.buffer));self.in_json=False
    def attributes(self,tag,**match):
        return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in match.items())]

def check():
    files=sorted(SITE.rglob('*.html'))
    assert len(files)==9, 'Expected eight localized pages and one 404'
    pages={p:Page(p.read_text(encoding='utf-8')) for p in files}
    urls={BASE+p.relative_to(SITE).as_posix().removesuffix('index.html'):p for p in files if p.name!='404.html'}
    titles=set();descriptions=set();links=0
    for p,page in pages.items():
        assert page.h1==1,(p,'Exactly one meaningful H1 required')
        assert page.attributes('html')[0]['lang'] in {'zh-CN','en'},p
        assert page.attributes('meta',name='viewport'),p
        assert page.attributes('link',rel='icon'),p
        dialog=page.attributes('dialog',id='feedback-dialog')
        assert len(dialog)==1 and dialog[0].get('aria-labelledby')=='feedback-title',p
        forms=page.attributes('form',id='feedback-form')
        assert len(forms)==1 and forms[0]['action']=='https://api.web3forms.com/submit',p
        key=forms[0].get('data-form-key','')
        assert not key or re.fullmatch(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}',key),p
        message=page.attributes('textarea',id='feedback-message')[0]
        assert 'required' in message and message['maxlength']=='3000',p
        assert page.attributes('input',id='feedback-email')[0]['type']=='email',p
        assert len(page.attributes('input',name='category'))==3,p
        assert page.attributes('input',name='botcheck'),p
        assert any(a.get('src','').split('?')[0].endswith('/feedback.mjs') for a in page.attributes('script',type='module')),p
        robots=page.attributes('meta',name='robots')[0]['content']
        if p.name=='404.html':
            assert 'noindex' in robots,p
        else:
            assert 'noindex' not in robots,p
            canonical=page.attributes('link',rel='canonical')
            expected=BASE+p.relative_to(SITE).as_posix().removesuffix('index.html')
            assert len(canonical)==1 and canonical[0]['href']==expected,(p,'Incorrect canonical')
            alternate=page.attributes('link',rel='alternate')
            assert {a['hreflang'] for a in alternate}=={'zh-Hans','en','x-default'},p
            for a in alternate:
                assert a['href'] in urls,(p,'Missing language target')
                target=pages[urls[a['href']]]
                assert any(b['href']==expected for b in target.attributes('link',rel='alternate')),(p,'Nonreciprocal language link')
            assert page.title and page.title not in titles,p
            titles.add(page.title)
            description=page.attributes('meta',name='description')[0]['content']
            assert description and description not in descriptions,p
            descriptions.add(description)
            assert page.attributes('meta',property='og:url')[0]['content']==expected,p
            image=urlsplit(page.attributes('meta',property='og:image')[0]['content'])
            assert image.scheme+'://'+image.netloc+image.path==BASE+'assets/social.png' and image.query=='v='+hashlib.sha256((SITE/'assets/social.png').read_bytes()).hexdigest()[:10],p
            assert page.attributes('meta',name='twitter:card')[0]['content']=='summary_large_image',p
            assert len(page.json)==1 and page.json[0]['@context']=='https://schema.org',p
            assert any(v['@type']=='WebPage' and v['url']==expected for v in page.json[0]['@graph']),p
        for tag,attrs in page.tags:
            if tag=='a':value=attrs.get('href','')
            elif tag in {'script','img'}:value=attrs.get('src','')
            elif tag=='link':value=attrs.get('href','')
            else:continue
            if not value:continue
            parsed=urlsplit(value)
            if parsed.scheme or parsed.netloc:continue
            if parsed.path.startswith('/'):
                assert parsed.path.startswith(PREFIX),(p,'Escapes project site base path',value)
                dest=SITE/unquote(parsed.path[len(PREFIX):])
            else:dest=p.parent/unquote(parsed.path)
            if dest.is_dir():dest/='index.html'
            assert dest.is_file(),(p,'Broken local target',value)
            if parsed.path.startswith(PREFIX+'assets/'):
                assert parsed.query=='v='+hashlib.sha256(dest.read_bytes()).hexdigest()[:10],(p,'Stale asset fingerprint',value)
            if parsed.fragment and dest in pages:assert unquote(parsed.fragment) in pages[dest].ids,(p,'Broken anchor',value)
            links+=1
    sitemap=ET.parse(SITE/'sitemap.xml').getroot()
    locs={x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
    assert locs==set(urls), 'Sitemap does not match canonical pages'
    assert (SITE/'assets/social.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    # Any concrete design-file URL is inappropriate for these public generic sources.
    private_link=re.compile(r'https?://(?:www\.)?figma\.com/(?:design|proto|file|board|slides|make)/[^\s<>"\x27]+',re.I)
    for directory in [ROOT/'website',SITE]:
        for p in directory.rglob('*'):
            if p.is_file() and p.suffix in {'.html','.js','.mjs','.css','.svg','.py','.md','.json','.xml'}:
                content=p.read_text(encoding='utf-8')
                assert not private_link.search(content),(p,'Concrete Figma file URL is not publishable')
    print(f'PASS: {len(urls)} crawlable localized pages, {links} local links/assets, reciprocal languages, canonical/sitemap/JSON-LD and public-content checks')

if __name__=='__main__':check()
