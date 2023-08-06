# -*- coding: utf-8 -*-
"""pyk8sver.app
"""
from __future__ import print_function
from github import Github

from pyk8sver import metadata
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Kubernetes():

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token
        self.g = Github(github_access_token)

    def fetch_releases(self):
        repo = self.g.get_repo("kubernetes/kubernetes")
        logging.info("repo {0}".format(repo))
        releases = repo.get_releases()
        logging.debug("releases {0}".format(releases))
        return releases
