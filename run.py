#!/usr/bin/env python
#-*- coding:utf8 -*-

import yaml
import os



def run():
    data = None
    with open('./mkdocs.yml', 'r') as fin:
        data = yaml.load(fin,Loader=yaml.FullLoader)
        fin.close()

    if not data:
        print("load mkdocs.yml error")
        return

    nav_item_list = []
    for nitem in data['nav']:
        for k,v in nitem.items():
            # k is show name , v is file name  ,{'Home': 'index.md'}
            nav_item_list.append(v)
            break
    docs_dir = data.get('docs_dir') or 'docs'
    site_dir = data.get('site_dir') or 'site'

    for item in os.listdir(docs_dir):
        abs_item = os.path.join(docs_dir, item)
        if os.path.isdir(abs_item):
            print("warning: found dir in document dir:{0}".format(docs_dir))
            continue
        if not abs_item.endswith('.md'):
            print("warning: found not support file type:{0}".format(item))
            continue
        if item in nav_item_list:
            continue
        file_name = item[:-3]  # not including .md
        nav_item = {file_name: item}
        data['nav'].append(nav_item)
        nav_item_list.append(item)

    with open('./mkdocs.yml', 'w') as fout:
        fout.write(yaml.dump(data))
        print(yaml.dump(data))
        fout.close()
    print("\nupdate mkdocs.yml done")

    cmd = 'mkdocs build'
    print(cmd)
    os.popen(cmd).readlines()
    print("mkdocs build done in dir:{0}".format(site_dir))

    cmd = 'git add --all . && git commit -m "update mkdocs site" && git push'
    print(cmd)
    r = os.popen(cmd).readlines()
    print(r)



    


if __name__ == '__main__':
    run()
