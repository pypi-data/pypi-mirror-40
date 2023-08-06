import os
import itertools
import hashlib
import urllib
import urllib.error
import json
import feedparser


def blank():
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, 'blank.png')


def get_cache_fn(uri):
    uri_hash = hashlib.md5(bytes(uri, 'utf-8')).hexdigest()

    home = os.environ['HOME']
    cache_dir = os.environ.get('XDG_CACHE_DIR') or '{}/.cache'.format(home)

    return '{}/mopidy/images/{}'.format(cache_dir, uri_hash)


def open_image_url(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
    return data


def spotify_art(uri):
    api_url = 'http://embed.spotify.com/oembed/?url={}'.format(uri)
    with urllib.request.urlopen(api_url) as api_response:
        data = api_response.read()
    js = json.loads(data)
    thumb_url = js['thumbnail_url']
    return open_image_url(thumb_url)


def podcast_art(uri):
    try:
        fp = feedparser.parse(uri[8:])
        image_url = fp['feed']['image']['url']
        return open_image_url(image_url)
    except urllib.error.HTTPError:
        return None


def get_local_fn(uri, root=None):
    song_fn = urllib.parse.unquote(uri.rsplit(':', 1)[1])
    if root:
        song_fn = os.path.join(root, song_fn)
    d = os.path.dirname(song_fn)

    def cap_perms(*t):
        return [i for s in t for i in (s, s.upper(), s.capitalize())]

    hidden = ['', '.']
    fn = cap_perms('folder', 'cover', 'front')
    ext = cap_perms('jpg', 'png', 'gif', 'bmp')

    perms = itertools.product(hidden, fn, ext)
    for perm in perms:
        search_fn = '{}{}.{}'.format(*perm)
        search_path = os.path.join(d, search_fn)
        if os.path.exists(search_path):
            return search_path

    return blank()


def get_fn(uri, root=None):
    if not uri:
        return blank()
    elif uri.startswith('file'):
        return get_local_fn(uri)
    elif uri.startswith('local'):
        return get_local_fn(uri, root)
    else:
        return get_cache_fn(uri)


def get_image(uri=None, art_url=None):
    if art_url:
        return open_image_url(art_url)
    elif uri.startswith('spotify'):
        return spotify_art(uri)
    elif uri.startswith('podcast'):
        return podcast_art(uri)
    else:
        return None
