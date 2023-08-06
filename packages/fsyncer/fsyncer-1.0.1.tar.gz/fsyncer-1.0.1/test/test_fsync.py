import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from pyfakefs.fake_filesystem_unittest import TestCase, Patcher
from fsyncer import fsyncer


class TestFsyncer(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    @patch('fsyncer.fsyncer.Github.get_user')
    def test_get_repo_list(self, get_user):
        os.environ['FSYNC_GITHUB_TOKEN'] = 'dummy token'
        mock_repo = MagicMock()
        mock_repo.fork.return_value = True
        mock_repo.owner.name = 'skarlso'

        mock_user = MagicMock()
        mock_user.get_repos.return_value = [mock_repo]
        mock_user.name = 'skarlso'

        get_user.return_value = mock_user
        repos = fsyncer.get_repo_list()
        get_user.assert_called()
        assert 1 == len(repos)

    @patch("fsyncer.fsyncer.sync_list")
    @patch('fsyncer.fsyncer.get_repo_list')
    def test_main_with_config_file(self, mock_repo_list, mock_sync_list):
        os.environ['FSYNC_GITHUB_TOKEN'] = 'dummy token'
        mock_repo1 = MagicMock()
        mock_repo1.fork.return_value = True
        mock_repo1.owner.name = 'skarlso'
        mock_repo1.name = 'mock_repo1'
        mock_repo2 = MagicMock()
        mock_repo2.fork.return_value = True
        mock_repo2.owner.name = 'skarlso'
        mock_repo2.name = 'mock_repo2'
        mock_repo_list.return_value = [mock_repo1, mock_repo2]
        config = Path(os.path.join(Path.home(), '.config', 'fsyncer', '.repo_list'))
        self.fs.create_file(config, contents='mock_repo1\n')
        fsyncer.main()
        mock_sync_list.assert_called_with([mock_repo1])

    @patch('fsyncer.fsyncer.run')
    @patch('fsyncer.fsyncer.get_repo_list')
    def test_main_without_config_file(self, mock_repo_list, mock_call):
        os.environ['FSYNC_GITHUB_TOKEN'] = 'dummy token'
        mock_repo = MagicMock()
        mock_repo.fork.return_value = True
        mock_repo.owner.name = 'skarlso'
        mock_repo.name = 'mock_repo'
        mock_repo_list.return_value = [mock_repo]
        fsyncer.main()
        mock_call.assert_called_with(['rm', '-fr', 'mock_repo'])

