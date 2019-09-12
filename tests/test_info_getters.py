import requests

from tippecanews.info_getters import xml_urls


def test_valid_xml_urls():
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
            "HIGH:!DH:!aNULL"
        )
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

    for url in xml_urls:
        response = requests.get(url)
        assert response.status_code == 200
