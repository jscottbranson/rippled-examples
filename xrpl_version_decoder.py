'''
Convert a version integer returned by servers on the XRP Ledger
into a human readable version number.

This is basically a Python3 translation of the XRPScan XRPL-Server-Version
repo: https://github.com/xrpscan/xrpl-server-version/blob/main/index.js
'''

IMPLEMENTATIONS = {
    '183b': 'rippled',
}

RELEASE_TYPES = {
    '10': 'RC',
    '01': 'beta',
}

def decode_version(version):
    '''
    Decode XRP Ledger version numbers.

    :param int version: Version integer from a XRP Ledger server

    :param returns: Human readable version information
    :param rtype: dict
    '''
    decoded_version = {}

    # Convert from integer to a string binary with 0 padding on the left
    version_bin = format(int(version), '064b')

    # Decode Implementation ID
    imp_bin = version_bin[0:16]
    imp_hex = format(int(imp_bin, 2), 'x')

    if imp_hex in IMPLEMENTATIONS:
        decoded_version['implementation'] = IMPLEMENTATIONS[imp_hex]
    else:
        decoded_version['implementation'] = 'unknown'

    # Decode Major Version
    decoded_version['major'] = int(version_bin[16:24], 2)

    # Decode Minor Version
    decoded_version['minor'] = int(version_bin[24:32], 2)

    # Decoded Patch Version
    decoded_version['patch'] = int(version_bin[32:40], 2)

    # Decode Release Type and number (if not a major release)
    release_type_bin = version_bin[40:42]
    if release_type_bin in RELEASE_TYPES:
        decoded_version['release_type'] = RELEASE_TYPES[release_type_bin]
        decoded_version['release_number'] = int(version_bin[42:48], 2)
    else:
        decoded_version['release_type'] = ''
        decoded_version['release_number'] = ''

    # Put it all together
    version_number = \
            f"{decoded_version.get('implementation')} " \
            + f"{decoded_version.get('major')}." \
            + f"{decoded_version.get('minor')}." \
            + f"{decoded_version.get('patch')}"
    decoded_version['version_number'] = version_number.strip()

    version_final = \
            f"{decoded_version.get('version_number')} " \
            + f"{decoded_version.get('release_type')} " \
            + f"{decoded_version.get('release_number')}"
    decoded_version['version'] = version_final.strip()

    return decoded_version


if __name__ == '__main__':
    VERSION = 1745990418782224384
    decoded = decode_version(VERSION)
    print(decoded)
