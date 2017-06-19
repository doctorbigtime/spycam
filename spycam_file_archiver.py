import os
import datetime as dt

def scan_spycam():
    now = dt.datetime.now()
    directory = '/export/spycam'
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if not os.path.isfile(path):
            continue
        ctime = dt.datetime.fromtimestamp(os.stat(path).st_ctime)
        if((now - ctime) > dt.timedelta(hours=1)):
            archive_path = os.path.join(directory, '{}-{:02}'.format(ctime.year, ctime.month)
                                        , '{:02}'.format(ctime.day)
                                        , '{:02}'.format(ctime.hour))
            if not os.path.exists(archive_path):
                os.makedirs(archive_path)
            new_path = os.path.join(archive_path, entry)
            print '{} => {}'.format(entry, new_path)
            os.rename(path, new_path)


if __name__ == '__main__':
    scan_spycam()
