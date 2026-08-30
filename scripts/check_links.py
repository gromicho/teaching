"""Check maintained Markdown/notebook links; optionally probe public web targets.

Authentication/rate-limit responses are reported separately from definite 404s.
Notebook source/provenance archives are not web-crawled.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import unquote, urlsplit
from urllib.request import Request,urlopen


def probe(url):
    try:
        request=Request(url,headers={'User-Agent':'TeachingResourceLinkCheck/1.0'})
        with urlopen(request,timeout=25) as response:
            response.read(256)
            final=response.url
            state='authentication-required' if any(x in final for x in ['accounts.google.com','github.com/login']) else 'reachable'
            return {'url':url,'status':response.status,'state':state,'final_url':final}
    except HTTPError as error:
        return {'url':url,'status':error.code,'state':'missing' if error.code in [404,410] else 'blocked-or-requires-review'}
    except Exception as error:
        return {'url':url,'state':'unverified','error':str(error)}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path('.'))
    parser.add_argument('--online',action='store_true')
    parser.add_argument('--public-root',type=Path)
    parser.add_argument('--report',type=Path,default=Path('link-report.json'))
    args=parser.parse_args()
    root=args.root.resolve()
    catalog_data=json.loads((root/'catalog.json').read_text(encoding='utf-8'))
    repositories={catalog_data['repository']:root}
    if args.public_root:
        repositories['gromicho/teaching']=args.public_root.resolve()
    sources=[]
    for path in root.rglob('*.md'):
        relative=path.relative_to(root)
        if not any(p.startswith('.') for p in relative.parts) and 'archive' not in relative.parts:
            sources.append((path,path.read_text(encoding='utf-8')))
    catalog=root/'catalog.json'
    if catalog.exists():
        for item in json.loads(catalog.read_text(encoding='utf-8'))['notebooks']:
            if item['execution_profile']=='archive':
                continue
            path=root/item['path']
            for cell in json.loads(path.read_text(encoding='utf-8'))['cells']:
                # Code contains download URLs, which need checking too.
                sources.append((path,''.join(cell['source'])))
    urls=set(); local_errors=[]
    for path,text in sources:
        links=re.findall(r'\]\(\s*(https?://[^\s)]+|[^\s)]+)\s*\)',text)
        links+=re.findall(r'(?:src|href)=[\"\'](https?://[^\"\']+)[\"\']',text)
        links+=re.findall(r'https?://[^\s<>\"\'\)\]]+',text)
        for link in links:
            if link.startswith(('http://','https://')):
                link=link.rstrip('.,;')
                parts=urlsplit(link)
                pieces=unquote(parts.path).strip('/').split('/')
                if parts.netloc=='colab.research.google.com' and pieces[0]=='github':
                    pieces=pieces[1:]
                    host='github.com'
                else:
                    host=parts.netloc
                repo='/'.join(pieces[:2])
                if host in ['github.com','raw.githubusercontent.com'] and repo in repositories:
                    tail=pieces[2:]
                    if tail and tail[0] in ['blob','tree']:
                        tail=tail[1:]
                    if tail and tail[0]=='main':
                        target=repositories[repo]/'/'.join(tail[1:])
                        if not target.exists():
                            local_errors.append({'source':path.relative_to(root).as_posix(),'target':link})
                        if host=='raw.githubusercontent.com' and target.is_dir():
                            # A base URL concatenated with a resource path is not
                            # itself a downloadable file. The loader tests check
                            # the actual resource table and checksums.
                            continue
                    # Private links must never be sent to an unauthenticated probe.
                    if repo.endswith('-solutions'):
                        continue
                urls.add(link)
            elif not link.startswith(('#','mailto:')):
                relative=unquote(urlsplit(link).path)
                if relative and not (path.parent/relative).exists():
                    local_errors.append({'source':path.relative_to(root).as_posix(),'target':link})
    results=list(ThreadPoolExecutor(max_workers=6).map(probe,sorted(urls))) if args.online else [{'url':u,'state':'not-probed'} for u in sorted(urls)]
    report={'local_errors':local_errors,'web_links':results}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    missing=[r for r in results if r['state']=='missing']
    print(json.dumps({'local_errors':local_errors,'missing':missing,'web_links':len(results)},indent=2))
    raise SystemExit(bool(local_errors or missing))


if __name__=='__main__':
    main()
