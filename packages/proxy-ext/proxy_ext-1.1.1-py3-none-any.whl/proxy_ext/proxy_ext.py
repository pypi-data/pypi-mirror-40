# coding:utf-8
import list_ext
import xprint as xp


def line2dict(line: str, internal: bool = False):
    proxy_dict = dict()
    tmp_list = list_ext.remove(line.split(' '))
    length = len(tmp_list)
    if 3 <= length:
        proxy_dict['protocol'] = tmp_list[0]
        proxy_dict['host'] = tmp_list[1]
        proxy_dict['port'] = int(tmp_list[2])

    if 5 <= length:
        proxy_dict['username'] = tmp_list[3]
        proxy_dict['password'] = tmp_list[4]

    if not internal and not proxy_dict:
        xp.error('Cannot parse a proxy from string: "{}"'.format(line))
        return None

    return proxy_dict


def line2string(line: str, internal: bool = False):
    proxy = line2dict(line, internal=True)
    return dict2string(proxy, internal)


def line2requests_proxies(line: str):
    string = line2string(line, internal=True)
    return string2requests_proxies(string)


def line2pyrogram_dict(line: str):
    proxy = line2dict(line, internal=True)
    return dict2pyrogram_dict(proxy)


def dict2string(proxy_dict: dict, internal: bool = False):
    length = len(proxy_dict)
    if 5 <= length:
        return '{protocol}://{username}:{password}@{host}:{port}'.format(
            protocol=proxy_dict['protocol'],
            username=proxy_dict['username'],
            password=proxy_dict['password'],
            host=proxy_dict['host'],
            port=proxy_dict['port'],
        )

    elif 3 <= length:
        return '{protocol}://{host}:{port}'.format(
            protocol=proxy_dict['protocol'],
            host=proxy_dict['host'],
            port=proxy_dict['port'],
        )

    if not internal:
        xp.error('Cannot parse a proxy from dict: {}'.format(proxy_dict))

    return None


def dict2requests_proxies(proxy_dict: dict):
    string = dict2string(proxy_dict, internal=True)
    return string2requests_proxies(string)


def dict2pyrogram_dict(proxy_dict: dict, internal: bool = False):
    if proxy_dict['protocol'] == 'socks5':
        return {
            'hostname': proxy_dict['host'],
            'port': proxy_dict['port'],
        }

    if not internal:
        xp.error('Cannot parse a proxy from dict: {}'.format(proxy_dict))

    return None


def string2requests_proxies(string: str):
    return {
        'http': format(string),
        'https': format(string),
    }
