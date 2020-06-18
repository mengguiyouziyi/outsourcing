import os
import xlwt
import xlrd
import datetime


file_dir = os.path.join(os.getcwd(), 'files')
excel_dir = os.path.join(file_dir, 'excel')
pdf_dir = os.path.join(file_dir, 'pdf')
if not os.path.exists(file_dir):
    os.mkdir(file_dir)
if not os.path.exists(pdf_dir):
    os.mkdir(pdf_dir)
if not os.path.exists(excel_dir):
    os.mkdir(excel_dir)


def write_xls(xls_lst, kw, time_now):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet 1")
    for i, l in enumerate(xls_lst):
        for j, col in enumerate(l):
            sheet.write(i, j, col)
    xls_file = os.path.join(pdf_dir, '{}_{}.xls'.format(kw, time_now))
    book.save(xls_file)


def read_xls(file_str):
    file = xlrd.open_workbook(os.path.join(excel_dir, file_str))
    st = file.sheet_by_index(0)
    lines = [st.row_values(i) for i in range(st.nrows)]
    return lines


def deduplicate(lines):
    xls_lst = list()
    dedup = set()
    for i, line in enumerate(lines):
        if line[1] in dedup:
            continue
        else:
            dedup.add(line[1])
            if line[0].endswith('.pdf'):
                xls_lst.append(line)
                # print(' handle %d line' % (i + 1))
    return xls_lst


def main(file_str):
    kw = '_'.join(file_str.split('_')[:-1])
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    lines = read_xls(file_str)
    xls_lst = deduplicate(lines)
    write_xls(xls_lst, kw, time_now)


if __name__ == '__main__':
    for file_str in os.listdir(excel_dir):
        print('reading %s' % file_str)
        main(file_str)
