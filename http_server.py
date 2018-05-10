import os
import sys
import json
import bottle
import datetime
import functools32

#static_dir = os.path.join(os.path.dirname(__file__), 'static')
#spycam_dir = os.path.join(os.path.dirname(__file__), 'pix')
spycam_dir = '/export/spycam/'
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    spycam_dir = sys.argv[1]


@bottle.route('/')
def home():
    subdirs = [x for x in os.listdir(spycam_dir) if os.path.isdir(os.path.join(spycam_dir, x))]
    return bottle.template('index', curr_dir='', subdirs=subdirs)


@functools32.lru_cache(maxsize=128)
def get_subdirs(path):
    print 'path: "{}"'.format(path)
    d = os.path.join(spycam_dir, path)
    print 'd: "{}"'.format(d)
    return sorted([x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))])


@bottle.route('/index/<path:path>')
def index(path):
    subdirs = get_subdirs(path)
    if subdirs:
        return bottle.template('index', curr_dir=path, subdirs=subdirs)
    else:
        return bottle.template('timeline', curr_dir=path)


@bottle.route('/<path:path>/dates.json')
@functools32.lru_cache(maxsize=1024)
def generate_dates(path):
    print 'generate dates - path: "{}"'.format(path)
    dates = []
    for file in os.listdir(os.path.join(spycam_dir, path)):
        try:
            date_split = file.split('-')
            dt = datetime.datetime.strptime(date_split[0], '%Y%m%d%H%M%S')
            if date_split[1].startswith('01'):
                dt = dt.replace(microsecond=500000)
            dates.append(str(dt))
        except ValueError:
            print 'I don\'t know what to do with {}'.format(file)
            continue
    return json.dumps({'dates':sorted(dates)}, indent=4)


@bottle.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root=static_dir)


@bottle.route('/picture/<path:path>/<filename>')
def get_original(path, filename):
    return bottle.static_file(os.path.join(path, filename), root=spycam_dir)


@functools32.lru_cache(maxsize=1024)
def create_thumbnail(path, filename):
    from PIL import Image
    from StringIO import StringIO
    print 'Creating thumbnail for {}'.format(filename)
    path = os.path.join(spycam_dir, path, filename)
    assert os.path.exists(path), 'No such file: {}'.format(path)
    io = StringIO()
    im = Image.open(path)
    im.thumbnail((128,128))
    im.save(io, 'JPEG')
    return io.getvalue()


@bottle.route('/thumb/<path:path>/<filename>')
def get_thumbnail(path, filename):
    bottle.response.content_type = 'image/jpeg'
    return create_thumbnail(path, filename)


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080, debug=True)
