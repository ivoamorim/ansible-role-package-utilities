import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('distro, package', [
    ('centos', 'yum-plugin-versionlock'),
    ('centos', 'epel-release'),
    ('debian,ubuntu', 'apt-utils'),
])
def test_packages_are_installed(host, distro, package):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    assert host.package(package).is_installed


@pytest.mark.parametrize('distro, file', [
    ('centos', '/etc/yum.repos.d/epel.repo'),
])
def test_configuration_files_exist(host, distro, file):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    file = host.file(file)
    assert file.exists


def test_BaseRepos_priority_is_highest(host):
    if host.system_info.distribution != 'centos':
        pytest.skip("skipping unmatch distribution")
    repo = '/etc/yum.repos.d/CentOS-Base.repo'
    cmd = "grep -A 8 '\[base\]' " + repo + " | grep 'priority=1'"
    result = host.run(cmd)
    assert result.rc == 0


def test_EPEL_is_enabled(host):
    if host.system_info.distribution != 'centos':
        pytest.skip("skipping unmatch distribution")
    file = '/etc/yum.repos.d/epel.repo'
    cmd = "grep 'enabled=1' " + file
    result = host.run(cmd)
    assert result.rc == 0


def test_EPELRepos_priority_is_second_highest(host):
    if host.system_info.distribution != 'centos':
        pytest.skip("skipping unmatch distribution")
    file = '/etc/yum.repos.d/epel.repo'
    cmd = "grep -A 8 '\[epel\]' " + file + " | grep 'priority=2'"
    result = host.run(cmd)
    assert result.rc == 0
