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

    return r


def line2string(line: str, internal: bool = False):
    """
    :param line:        socks5 127.0.0.1 1080 user pass
    :param internal:    call from internal
    :return:            socks5://user:pass@127.0.0.1:1008
    """
    proxy = line2dict(line, internal=True)
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


def line2requests_proxies(line: str):
    string = line2string(line)
    return {
        'http': string,
        'https': string,
    }


def line2pyro_socks_dict(line: str, internal: bool = False):
    proxy = line2dict(line, internal=True)
    if proxy['protocol'] == 'socks5':
        return {
            'hostname': proxy['host'],
            'port': proxy['port'],
        }

    if not internal:
        xp.error('Cannot parse a proxy from string: "{}"'.format(line))

    return None


def string2requests_proxies(string: str):
    return {
        'http': 'http://{}'.format(string),
        'https': 'https://{}'.format(string),
    }
