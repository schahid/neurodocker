"""Tests for neurodocker.interfaces.Miniconda"""
# Author: Jakub Kaczmarzyk <jakubk@mit.edu>
from __future__ import absolute_import, division, print_function

import pytest

from neurodocker.interfaces import Miniconda
from neurodocker.interfaces.tests import utils

class TestMiniconda(object):
    """Tests for Miniconda class."""

    #@pytest.mark.skip(reason="running container in background does not find correct Python")
    def test_build_image_miniconda_latest_shellscript_centos7(self):
        """Install latest version of Miniconda via ContinuumIO's installer
        script on CentOS 7.
        """
        specs = {'pkg_manager': 'yum',
                 'check_urls': True,
                 'instructions': [
                    ('base', 'centos:7'),
                    ('user', 'neuro'),
                    ('miniconda', {
                        'env_name': 'default',
                        'python_version': '3.5.1',
                        'conda_install': ['traits'],
                        'pip_install': ['https://github.com/nipy/nipype/archive/master.tar.gz']
                    }),
                    ('user', 'neuro'),
                 ]}
        container = utils.get_container_from_specs(specs)
        output = container.exec_run('python -V')
        assert "3.5.1" in output, "incorrect Python version"
        output = container.exec_run('python -c "import nipype"')
        assert "ImportError" not in output, "nipype not installed"
        utils.test_cleanup(container)
