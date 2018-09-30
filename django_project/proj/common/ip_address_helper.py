#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import socket


# http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
def is_valid_ipv4_address(address):
    """
    Validate an IPv4 IP address.
    :param address: IPv4 address with no netmask.
    :return: True if valid IPv4 IP address.
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    """
    Validate an IPv6 IP address.
    :param address: IPv6 address with no netmask.
    :return: True if valid IPv6 IP address.
    """
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def normalize_ip_address(addr):
    """
    Use sockets to normalize IP addresses
    :param addr: IPv4 or IPv6 address string
    :return: Normalized IP address string
    """

    af_type = None

    if not addr:
        return None

    if is_valid_ipv4_address(addr):
        af_type = socket.AF_INET

    if is_valid_ipv6_address(addr):
        af_type = socket.AF_INET6

    if not af_type:
        return None

    try:
        # Get a cleanly formatted IPv6 address string
        b_addr = socket.inet_pton(af_type, addr)
        s_addr = socket.inet_ntop(af_type, b_addr)

        return s_addr

    except socket.error as e:
        pass

    return None