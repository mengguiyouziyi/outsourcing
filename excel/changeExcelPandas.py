# -*- coding: UTF-8 -*-
# ***********************************************
# **  file：     changeExcelPandas.py
# **  purpose：  change excel with pandas
# **
# **  author:    mengguiyouziyi
# **  date:      2018/12/03
# ***********************************************

import pandas as pd
import pandas as np
from traceback import print_exc
import os

path_re = path_wr = r'.'
if not os.path.exists(path_wr):
    os.makedirs(path_wr)
for i, file in enumerate(os.listdir(path_re)):
    # if '.xlsx' not in file:
    #     continue
    print(i, '~' * 5, 'handle', file)
    if file.startswith('~') or file.startswith('change'):
        continue
    if (not file.endswith('.xls')) and (not file.endswith('.xlsx')):
        continue
    try:
        file_re = os.path.join(path_re, file)
        file_wr = os.path.join(path_wr, 'change-' + file)
        # file_wr = os.path.join(path_wr, 'change-' + str(i) + '-' + file)
        er = pd.ExcelFile(file_re)
        ew = pd.ExcelWriter(file_wr)
        sheets = er.sheet_names
        oks = [sheet for sheet in sheets if 'OK' in sheet]
        for ok in oks:
            # , names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
            sp = er.parse(ok, header=None)
            # sp.ix[1, 'B'] = sp.ix[1, 'K']
            # sp.ix[1, 'K'] = np.NaT
            # sp.ix[2, 'C'] = 2
            # sp.ix[4, 'D'] = np.NaT
            # sp.ix[1, 'F'] = sp.ix[2, 'F'] / sp.ix[3, 'F']
            print(sp.keys())
            sp.ix[1, 1] = sp.ix[1, 10]
            sp.ix[1, 10] = np.NaT
            sp.ix[2, 2] = 2
            sp.ix[4, 3] = np.NaT
            sp.ix[1, 5] = sp.ix[2, 5] / sp.ix[3, 5]
            sp.to_excel(ew, sheet_name=ok, header=False, index=False)
        ew.save()
        print()
    except:
        print_exc()
        print()
        continue
