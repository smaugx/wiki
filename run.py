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

    print(data)
    nav_item_list = []
    data['nav'] = []  # clear old nav items
    docs_dir = data.get('docs_dir') or 'docs'
    site_dir = data.get('site_dir') or 'site'

    first_index = False
    last_other = False
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
        if item == 'index.md':
            first_index = True
        elif item == 'other.md':
            last_other = True
        else:
            nav_item_list.append(item)

    for item in nav_item_list:
        file_name = item[:-3]  # not including .md
        nav_item = {file_name: item}
        data['nav'].append(nav_item)

    if first_index:
        data['nav'].insert(0, {'Home': 'index.md'})
    if last_other:
        data['nav'].append({u'其他': 'other.md'})

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
    cmd = 'ls'
    print(cmd)
    r = os.popen(cmd).readlines()
    for ritem in r:
        print(ritem),


    


if __name__ == '__main__':
    run()
