import os
import json
import bottle
import datetime
import functools32

static_dir = os.path.join(os.path.dirname(__file__), 'static')
spycam_dir = os.path.join(os.path.dirname(__file__), 'pix')


@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='.')


@bottle.route('/dates.json')
def generate_dates():
    dates = []
    for file in os.listdir(spycam_dir):
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


@bottle.route('/picture/<filename>')
def get_original(filename):
    return bottle.static_file(filename, root=spycam_dir)

@functools32.lru_cache(maxsize=1024)
def create_thumbnail(filename):
    from PIL import Image
    from StringIO import StringIO
    print 'Creating thumbnail for {}'.format(filename)
    path = os.path.join(spycam_dir, filename)
    assert os.path.exists(path), 'No such file: {}'.format(path)
    io = StringIO()
    im = Image.open(path)
    im.thumbnail((128,128))
    im.save(io, 'JPEG')
    return io.getvalue()


@bottle.route('/thumb/<filename>')
def get_thumbnail(filename):
    bottle.response.content_type = 'image/jpeg'
    return create_thumbnail(filename)


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080, debug=True)
