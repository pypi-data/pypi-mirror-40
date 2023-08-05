# coding:utf-8
import list_ext
import xprint as xp


def line2dict(line: str, internal: bool = False):
    r = dict()
    tmp_list = list_ext.remove(line.split(' '))
    length = len(tmp_list)
    if 3 <= length:
        r['protocol'] = tmp_list[0]
        r['host'] = tmp_list[1]
        r['port'] = int(tmp_list[2])

    if 5 <= length:
        r['username'] = tmp_list[3]
        r['password'] = tmp_list[4]

    if not internal and not r:
        xp.error('Cannot parse a proxy from string: "{}"'.format(line))
        return None

    return r


def line2string(line: str, internal: bool = False):
    proxy = line2dict(line, internal=True)
    return dict2string(proxy, internal)


def line2requests_proxies(line: str):
    string = line2string(line, internal=True)
    return string2requests_proxies(string)


def line2pyro_socks_dict(line: str):
    proxy = line2dict(line, internal=True)
    return dict2pyro_socks_dict(proxy)


def dict2string(proxy: dict, internal: bool = False):
    length = len(proxy)
    if 5 <= length:
        return '{protocol}://{username}:{password}@{host}:{port}'.format(
            protocol=proxy['protocol'],
            username=proxy['username'],
            password=proxy['password'],
            host=proxy['host'],
            port=proxy['port'],
        )

    elif 3 <= length:
        return '{protocol}://{host}:{port}'.format(
            protocol=proxy['protocol'],
            host=proxy['host'],
            port=proxy['port'],
        )

    if not internal:
        xp.error('Cannot parse a proxy from dict: {}'.format(proxy))

    return None


def dict2requests_proxies(proxy: dict):
    string = dict2string(proxy, internal=True)
    return string2requests_proxies(string)


def dict2pyro_socks_dict(proxy: dict, internal: bool = False):
    if proxy['protocol'] == 'socks5':
        return {
            'hostname': proxy['host'],
            'port': proxy['port'],
        }

    if not internal:
        xp.error('Cannot parse a proxy from dict: {}'.format(proxy))

    return None


def string2requests_proxies(string: str):
    return {
        'http': format(string),
        'https': format(string),
    }
