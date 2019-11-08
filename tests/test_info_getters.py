import requests

from tippecanews.utils.info_getters import get_pngs, xml_urls


def test_valid_xml_urls():
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
            "HIGH:!DH:!aNULL"
        )
    except AttributeError:
        pass

    for url in xml_urls:
        response = requests.get(url)
        assert response.status_code == 200


def test_get_pngs():
    assert len(get_pngs()) >= 0
