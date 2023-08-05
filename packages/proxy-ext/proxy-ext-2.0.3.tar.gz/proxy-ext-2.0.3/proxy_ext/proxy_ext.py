# coding:utf-8
import random
import list_ext
import file_ext
import xprint as xp
from ip_query import ip_query


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
        length = len(proxy_dict)
        if 5 <= length:
            return {
                'hostname': proxy_dict['host'],
                'port': proxy_dict['port'],
                'username': proxy_dict['username'],
                'password': proxy_dict['password'],
            }

        elif 3 <= length:
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


def random_pyrogram_dict_from_file(path_to_file: str,
                                   retries: int = 0,
                                   max_retries: int = 10,
                                   ):
    lines = file_ext.read_to_list(path_to_file)
    if lines:
        xp.getting('Random a proxy')

        line = random.choice(lines)
        proxy_dict = line2dict(line)

        if not proxy_dict:
            retries += 1
            if retries < max_retries:
                return random_pyrogram_dict_from_file(path_to_file=path_to_file,
                                                      retries=retries,
                                                      )
            xp.fx()
            xp.error('After {max_retries} retries, there are no available proxy.'.format(
                max_retries=max_retries,
            ))
            return None

        # host:port
        xp.wr('{host}:{port} '.format(host=proxy_dict['host'],
                                      port=proxy_dict['port'],
                                      ))
        xp.step(with_blanks=1)

        # try to get IP
        try:
            if ip_query(requests_proxies=dict2requests_proxies(proxy_dict)):
                return dict2pyrogram_dict(proxy_dict)

        except Exception as e:
            xp.error('Failed.')

            retries += 1
            if retries < max_retries:
                return random_pyrogram_dict_from_file(path_to_file=path_to_file,
                                                      retries=retries,
                                                      )

            xp.fx()
            xp.error('After {max_retries} retries, there are no available proxy.'.format(
                max_retries=max_retries,
            ))
            return None

    return None


def requests_proxies(protocol: str = 'socks5',
                     host: str = '127.0.0.1',
                     port: int = 1080,
                     username: str = None,
                     password: str = None,
                     ):
    if username and password:
        string = '{protocol}://{username}:{password}@{host}:{port}'.format(protocol=protocol,
                                                                           host=host,
                                                                           port=port,
                                                                           username=username,
                                                                           password=password,
                                                                           )
    else:
        string = '{protocol}://{host}:{port}'.format(protocol=protocol,
                                                     host=host,
                                                     port=port,
                                                     )

    return string2requests_proxies(string)
