# -*- coding: utf-8 -*-

import os
import csv
import time

bpath = os.getcwd()


def mergeExcel(qtype):
    qtype_path = os.path.join(bpath, r'TEM', r'WZJG', qtype)

    def file_name(file_dir):
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.csv':
                    L.append(os.path.join(root, file))
        return L

    a = open(os.path.join(qtype_path, f'0_{qtype}_A.csv'), 'a', encoding='utf-8', newline='')
    b = open(os.path.join(qtype_path, f'0_{qtype}_B.csv'), 'a', encoding='utf-8', newline='')
    c = open(os.path.join(qtype_path, f'0_{qtype}_C.csv'), 'a', encoding='utf-8', newline='')
    aw = csv.writer(a)
    bw = csv.writer(b)
    cw = csv.writer(c)
    aw.writerow(['昵称', '邮箱', '等级'])
    bw.writerow(['昵称', '邮箱', '等级'])
    cw.writerow(['昵称', '邮箱', '等级'])

    al = []
    bl = []
    cl = []
    for file in file_name(qtype_path):
        with open(file, 'r', encoding='utf-8', newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            # spamreader.__next__()
            next(spamreader, None)
            for row in spamreader:
                print(row)
                lc = row[2]
                if 'A' == lc:
                    al.append(row)
                elif 'B' == lc:
                    bl.append(row)
                elif 'C' == lc:
                    cl.append(row)
    aset = set()
    bset = set()
    cset = set()
    for row in al:
        email = row[1]
        if email not in aset:
            aset.add(email)
            aw.writerow(row)
        else:
            continue
    for row in bl:
        email = row[1]
        if email not in bset:
            bset.add(email)
            bw.writerow(row)
        else:
            continue
    for row in cl:
        email = row[1]
        if email not in cset:
            cset.add(email)
            cw.writerow(row)
        else:
            continue
    a.close()
    b.close()
    c.close()


if __name__ == '__main__':
    mergeExcel('company')
