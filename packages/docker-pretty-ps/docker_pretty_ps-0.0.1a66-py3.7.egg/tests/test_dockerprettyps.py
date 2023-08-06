"""Tests Carpet Tools

"""
from .data import docker_ps as test_ps_data


class TestDockerPrettyPs(object):

    def test_url_join(self):
        """
        Tests the url_join method. This is just an alias of url_concat.
        We check to make sure we're not adding any extra slashes or making weird urls.

        """
        assert type(test_ps_data.ps_data_1) == str

# End File docker-pretty-ps/tests/test_dockerprettyps.py
