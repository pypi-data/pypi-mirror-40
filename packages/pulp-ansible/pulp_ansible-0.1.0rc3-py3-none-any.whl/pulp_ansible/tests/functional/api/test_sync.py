# coding=utf-8
"""Tests that sync ansible plugin repositories."""
import unittest

from pulp_smash import api, config, exceptions
from pulp_smash.pulp3.constants import REPO_PATH
from pulp_smash.pulp3.utils import (
    gen_repo,
    get_content_summary,
    get_added_content,
    sync,
)

from pulp_ansible.tests.functional.constants import (
    ANSIBLE_REMOTE_PATH,
    ANSIBLE_FIXTURE_CONTENT_SUMMARY,
    ANSIBLE_FIXTURE_COUNT,
)
from pulp_ansible.tests.functional.utils import gen_ansible_remote
from pulp_ansible.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class BasicSyncTestCase(unittest.TestCase):
    """Sync repositories with the ansible plugin."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()

    def test_sync(self):
        """Sync repositories with the ansible plugin.

        In order to sync a repository a remote has to be associated within
        this repository. When a repository is created this version field is set
        as None. After a sync the repository version is updated.

        Do the following:

        1. Create a repository, and a remote.
        2. Assert that repository version is None.
        3. Sync the remote.
        4. Assert that repository version is not None.
        5. Assert that the correct number of units were added and are present in the repo.
        6. Sync the remote one more time.
        7. Assert that repository version is different from the previous one.
        8. Assert that the same number of are present and that no units were added.
        """
        client = api.Client(self.cfg, api.json_handler)

        repo = client.post(REPO_PATH, gen_repo())
        self.addCleanup(client.delete, repo['_href'])

        body = gen_ansible_remote()
        remote = client.post(ANSIBLE_REMOTE_PATH, body)
        self.addCleanup(client.delete, remote['_href'])

        # Sync the repository.
        self.assertIsNone(repo['_latest_version_href'])
        sync(self.cfg, remote, repo)
        repo = client.get(repo['_href'])

        self.assertIsNotNone(repo['_latest_version_href'])
        self.assertDictEqual(get_content_summary(repo), ANSIBLE_FIXTURE_CONTENT_SUMMARY)
        self.assertEqual(len(get_added_content(repo)), ANSIBLE_FIXTURE_COUNT)

        # Sync the repository again.
        latest_version_href = repo['_latest_version_href']
        sync(self.cfg, remote, repo)
        repo = client.get(repo['_href'])

        self.assertNotEqual(latest_version_href, repo['_latest_version_href'])
        self.assertDictEqual(get_content_summary(repo), ANSIBLE_FIXTURE_CONTENT_SUMMARY)
        self.assertEqual(len(get_added_content(repo)), 0)


class SyncInvalidURLTestCase(unittest.TestCase):
    """Sync a repository with an invalid url on the Remote."""

    def test_all(self):
        """
        Sync a repository using a Remote url that does not exist.

        Test that we get a task failure.

        """
        cfg = config.get_config()
        client = api.Client(cfg, api.json_handler)

        repo = client.post(REPO_PATH, gen_repo())
        self.addCleanup(client.delete, repo['_href'])

        body = gen_ansible_remote(url="http://i-am-an-invalid-url.com/invalid/")
        remote = client.post(ANSIBLE_REMOTE_PATH, body)
        self.addCleanup(client.delete, remote['_href'])

        with self.assertRaises(exceptions.TaskReportError):
            sync(cfg, remote, repo)
