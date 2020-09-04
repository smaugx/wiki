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
        print("{0} begin dump mkdocs.yml {1}".format("#" * 15, "#" * 15))
        print(yaml.dump(data))
        fout.close()
    print("{0} update mkdocs.yml done {1}\n".format("#" * 15, "#" * 15))

    cmd = 'mkdocs build'
    print("{0} begin {1} {2}".format("#" * 15, cmd, "#" * 15))
    os.popen(cmd).readlines()
    print("{0} mkdocs build done in dir:{1} {2}\n".format("#" * 15, site_dir, "#" * 15))

    cmd = 'git add --all . && git commit -m "update mkdocs site" && git push'
    print("{0} begin git push:{1} {2}".format("#" * 15, cmd, "#" * 15))
    r = os.popen(cmd).readlines()
    for ritem in r:
        print(ritem),
    print("{0} git push done {1}\n".format("#" * 15, "#" * 15))


    


if __name__ == '__main__':
    run()
