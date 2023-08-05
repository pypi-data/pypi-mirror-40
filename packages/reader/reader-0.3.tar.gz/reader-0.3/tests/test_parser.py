from urllib.parse import urlparse
import warnings
import subprocess

import pytest
import feedparser

from server import run_httpd

from reader import Feed
from reader.parser import RequestsParser
from reader.exceptions import ParseError, NotModified


@pytest.fixture
def parse():
    parse = RequestsParser()
    parse._verify = False
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield parse


@pytest.fixture
def make_relative_path_url(**_):
    yield lambda feed_path: feed_path.basename

@pytest.fixture
def make_absolute_path_url(**_):
    yield lambda feed_path: str(feed_path)

@pytest.fixture
def make_http_url(requests_mock, **_):
    def make_url(feed_path):
        url = 'http://example.com/' + feed_path.basename
        headers = {}
        if feed_path.ext == '.rss':
            headers['Content-Type'] = 'application/x-rss+xml'
        elif feed_path.ext == '.atom':
            headers['Content-Type'] = 'application/atom+xml'
        requests_mock.get(url, text=feed_path.read(), headers=headers)
        return url
    yield make_url

@pytest.fixture
def make_https_url(requests_mock, **_):
    def make_url(feed_path):
        url = 'http://example.com/' + feed_path.basename
        headers = {}
        if feed_path.ext == '.rss':
            headers['Content-Type'] = 'application/x-rss+xml'
        elif feed_path.ext == '.atom':
            headers['Content-Type'] = 'application/atom+xml'
        requests_mock.get(url, text=feed_path.read(), headers=headers)
        return url
    yield make_url

@pytest.fixture
def make_http_gzip_url(requests_mock, **_):
    def make_url(feed_path):
        url = 'http://example.com/' + feed_path.basename
        headers = {}
        if feed_path.ext == '.rss':
            headers['Content-Type'] = 'application/x-rss+xml'
        elif feed_path.ext == '.atom':
            headers['Content-Type'] = 'application/atom+xml'
        headers['Content-Encoding'] = 'gzip'

        import io, gzip
        compressed_file = io.BytesIO()
        gz = gzip.GzipFile(fileobj=compressed_file, mode='wb')
        gz.write(feed_path.read_binary())
        gz.close()

        requests_mock.get(url, content=compressed_file.getvalue(), headers=headers)
        return url
    yield make_url

@pytest.fixture(params=[
    make_relative_path_url,
    make_absolute_path_url,
    make_http_url,
    make_https_url,
    make_http_gzip_url,
])
def make_url(request, requests_mock):
    yield from request.param(requests_mock=requests_mock)


@pytest.fixture(params=[
    make_relative_path_url,
    pytest.param(make_http_url, marks=pytest.mark.slow),
])
def make_url_local_remote(request, requests_mock):
    yield from request.param(requests_mock=requests_mock)


@pytest.mark.parametrize('feed_type', ['rss', 'atom'])
def test_parse(monkeypatch, feed_type, parse, make_url, data_dir):
    monkeypatch.chdir(data_dir)

    feed_filename = 'full.{}'.format(feed_type)
    feed_url = make_url(data_dir.join(feed_filename))

    expected = {}
    exec(data_dir.join(feed_filename + '.py').read(), expected)

    feed, entries, _, _ = parse(feed_url)
    entries = list(entries)

    assert feed == expected['feed']._replace(url=feed_url)
    assert entries == expected['entries']


@pytest.mark.parametrize('feed_type', ['rss', 'atom'])
def test_parse_empty(monkeypatch, feed_type, parse, make_relative_path_url, data_dir):
    make_url = make_relative_path_url
    monkeypatch.chdir(data_dir)

    feed_filename = 'empty.{}'.format(feed_type)
    feed_url = make_url(data_dir.join(feed_filename))

    expected = {}
    exec(data_dir.join(feed_filename + '.py').read(), expected)

    feed, entries, _, _ = parse(feed_url)
    entries = list(entries)

    assert feed == expected['feed']._replace(url=feed_url)
    assert entries == expected['entries']


@pytest.mark.xfail
def test_parse_returns_etag_last_modified():
    # TODO: write this
    assert False


@pytest.mark.parametrize('feed_type', ['rss', 'atom'])
def test_parse_relative_links(monkeypatch, feed_type, parse, make_url_local_remote, data_dir):
    make_url = make_url_local_remote
    monkeypatch.chdir(data_dir)

    feed_filename = 'relative.{}'.format(feed_type)
    feed_url = make_url(data_dir.join(feed_filename))

    expected = {}
    exec(data_dir.join(feed_filename + '.py').read(), expected)

    parsed_feed, _, _, _ = parse(feed_url)
    assert parsed_feed.link == urlparse(feed_url)._replace(path=expected['feed'].link).geturl()


def test_parse_error(monkeypatch, parse, data_dir):
    """parse() should reraise most feedparser exceptions."""

    feedparser_exception = Exception("whatever")
    old_feedparser_parse = feedparser.parse
    def feedparser_parse(*args, **kwargs):
        rv = old_feedparser_parse(*args, **kwargs)
        rv['bozo'] = 1
        rv['bozo_exception'] = feedparser_exception
        return rv

    monkeypatch.setattr('feedparser.parse', feedparser_parse)

    with pytest.raises(ParseError) as excinfo:
        parse(str(data_dir.join('full.atom')))

    assert excinfo.value.__cause__ is feedparser_exception


def test_parse_character_encoding_override(monkeypatch, parse, data_dir):
    """parse() should not reraise feedparser.CharacterEncodingOverride."""

    old_feedparser_parse = feedparser.parse
    def feedparser_parse(*args, **kwargs):
        rv = old_feedparser_parse(*args, **kwargs)
        rv['bozo'] = 1
        rv['bozo_exception'] = feedparser.CharacterEncodingOverride("whatever")
        return rv

    monkeypatch.setattr('feedparser.parse', feedparser_parse)

    # shouldn't raise an exception
    parse(str(data_dir.join('full.atom')))


@pytest.fixture
def make_http_url_304(requests_mock):
    def make_url(feed_path):
        url = 'http://example.com/' + feed_path.basename
        requests_mock.get(url, status_code=304)
        return url
    yield make_url

def test_parse_not_modified(monkeypatch, parse, make_http_url_304, data_dir):
    """parse() should raise NotModified for unchanged feeds."""

    monkeypatch.chdir(data_dir)

    feed_url = make_http_url_304(data_dir.join('full.atom'))

    with pytest.raises(NotModified):
        parse(feed_url)


@pytest.fixture
def make_http_get_headers_url(requests_mock):
    def make_url(feed_path):
        url = 'http://example.com/' + feed_path.basename
        headers = {}
        if feed_path.ext == '.rss':
            headers['Content-Type'] = 'application/x-rss+xml'
        elif feed_path.ext == '.atom':
            headers['Content-Type'] = 'application/atom+xml'
        def callback(request, context):
            make_url.request_headers = request.headers
            return feed_path.read()
        requests_mock.get(url, text=callback, headers=headers)
        return url
    yield make_url

def test_parse_sends_etag_last_modified(monkeypatch, parse, make_http_get_headers_url, data_dir):
    monkeypatch.chdir(data_dir)

    feed_url = make_http_get_headers_url(data_dir.join('full.atom'))
    parse(feed_url, 'etag', 'last_modified')

    headers = make_http_get_headers_url.request_headers

    assert headers.get('If-None-Match') == 'etag'
    assert headers.get('If-Modified-Since') == 'last_modified'


@pytest.mark.parametrize('tz', ['UTC', 'Europe/Helsinki'])
def test_parse_local_timezone(monkeypatch, request, parse, tz, data_dir):
    """parse() return the correct dates regardless of the local timezone."""

    feed_path = data_dir.join('full.atom')

    expected = {}
    exec(feed_path.new(ext='.atom.py').read(), expected)

    import time
    request.addfinalizer(time.tzset)
    monkeypatch.setenv('TZ', tz)
    time.tzset()
    feed = parse(str(feed_path))[0]
    assert feed.updated == expected['feed'].updated


def test_parse_response_plugins(monkeypatch, tmpdir, make_http_url, data_dir):
    monkeypatch.chdir(data_dir)

    feed_url = make_http_url(data_dir.join('empty.atom'))
    make_http_url(data_dir.join('full.atom'))

    import requests

    def do_nothing_plugin(session, response, request):
        do_nothing_plugin.called = True
        assert isinstance(session, requests.Session)
        assert isinstance(response, requests.Response)
        assert isinstance(request, requests.Request)
        assert request.url == feed_url
        return None

    def rewrite_to_empty_plugin(session, response, request):
        rewrite_to_empty_plugin.called = True
        request.url = request.url.replace('empty', 'full')
        return request

    parse = RequestsParser()
    parse.response_plugins.append(do_nothing_plugin)
    parse.response_plugins.append(rewrite_to_empty_plugin)

    feed, _, _, _ = parse(feed_url)
    assert do_nothing_plugin.called
    assert rewrite_to_empty_plugin.called
    assert feed.link is not None
    print('---', feed)


def test_parse_requests_exception(monkeypatch, parse):
    exc = Exception('exc')
    def raise_exc():
        raise exc

    import requests
    monkeypatch.setattr(requests, 'Session', raise_exc)

    with pytest.raises(ParseError) as excinfo:
        parse('http://example.com')

    assert excinfo.value.__cause__ is exc

