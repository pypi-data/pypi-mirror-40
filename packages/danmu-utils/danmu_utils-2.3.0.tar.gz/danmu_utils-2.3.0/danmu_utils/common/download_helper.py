import os
import time


__all__ = ['download_line', 'download_file', 'download_dir']


def download_line(line, tool, add_file_timestamp=False):
    line_res = tool.download(line)
    for item in line_res:
        filename = item['filename']
        if add_file_timestamp:
            tmp_1 = os.path.splitext(filename)
            timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
            filename = tmp_1[0] + '_' + timestamp + tmp_1[1]
        with open(filename, 'wb') as f:
            f.write(item['data'])


def download_file(filename, tool, add_dir_timestamp=False, add_file_timestamp=False):
    print('Start process list file: "%s".' % filename)
    tmp_1 = os.path.splitext(filename)
    if tmp_1[1] == '.' + tool.DANMU_LIST_EXTNAME:
        out_dir = tmp_1[0]
    else:
        out_dir = filename
    if add_dir_timestamp:
        timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        out_dir = out_dir + '_' + timestamp
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    curdir = os.path.abspath(os.curdir)
    try:
        with open(filename, encoding='utf8') as f:
            os.chdir(out_dir)
            for line in f:
                download_line(line, tool, add_file_timestamp=add_file_timestamp)
    except Exception as e:
        print(e)
        return
    os.chdir(curdir)
    print('Success generate dir: "%s" for list file.' % out_dir)


def download_dir(dirname, tool, add_dir_timestamp=False, add_file_timestamp=False):
    print('Start process dir: "%s".' % dirname)
    for filename in os.listdir(dirname):
        filename = os.path.join(dirname, filename)
        if not os.path.isfile(filename):
            continue
        if os.path.splitext(filename)[1] != '.' + tool.DANMU_LIST_EXTNAME:
            continue
        download_file(filename, tool, add_dir_timestamp=add_dir_timestamp, add_file_timestamp=add_file_timestamp)
    print('Success process dir: "%s".' % dirname)