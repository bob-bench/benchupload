"""
Copyright (C) 2016-2017 by Strong Leaf Consultant Ltd.

GNU AGPL v3+

Bob-Bench CI detection
"""

import os

class CISystem(object):
    """
    I represent one CI system. My subclasses can be classes
    like TravisCI, Jenkins or many more. My subclasses are
    instantiated by calling the static detect method.
    """
    def __init__(self, github_slug=None, commit=None, commit_range=None, tag=None, branch=None, build_nr=None, os_name=None, job_id=None, repo_url=None):
        self.commit = commit
        self.commit_range = commit_range
        self.tag = tag
        self.branch = branch
        self.build_nr = build_nr
        self.os_name = os_name
        self.job_id = job_id

        # specific github, bitbucket, custom?
        if repo_url:
            self.repo_url = repo_url
            self.is_github = self.looks_like_github(repo_url)
        else:
            self.repo_url = self.build_url(github_slug)
            self.is_github = github_slug != None

    def looks_like_github(self, repo_url):
        """See if this url looks like github. Assume https for now"""
        return "https://github.com/" in repo_url

    def build_url(self, github_slug):
        """In the future I will know about bitbucket, etc"""
        return "https://github.com/" + github_slug

    @staticmethod
    def detect():
        raise Exception("Should be implemented")

class TravisCI(CISystem):
    """
    I represent the TravisCI system. It only works with the
    github hosting service. The environment variables for it
    are documented here:

      https://docs.travis-ci.com/user/environment-variables
    """

    def system_name(self):
        return "travis-ci"

    @staticmethod
    def detect():
        if os.getenv('CI') != 'true' or os.getenv('TRAVIS') != 'true' or os.getenv('SHIPPABLE') == 'true':
            return None

        return TravisCI(
                github_slug=os.getenv('TRAVIS_REPO_SLUG'),
                commit=os.getenv('TRAVIS_COMMIT'),
                commit_range=os.getenv('TRAVIS_COMMIT_RANGE'),
                tag=os.getenv('TRAVIS_TAG'),
                branch=os.getenv('TRAVIS_BRANCH'),
                build_nr=os.getenv('TRAVIS_JOB_NUMBER'),
                os_name=os.getenv('TRAVIS_OS_NAME'),
                job_id=os.getenv('TRAVIS_JOB_ID'))

class CircleCI(CISystem):
    """
    I was created in Hanoi and get detect CircleCI as CI
    system. The environment are documented and also found
    by other people:

      https://circleci.com/docs/environment-variables/
      https://gist.github.com/steinnes/248a144861547c719f89b55bcda297b5
    """

    def system_name(self):
        return "circleci"

    @staticmethod
    def detect():
        if os.getenv('CI') != 'true' or os.getenv('CIRCLECI') != 'true':
            return None

        return CircleCI(
                repo_url=os.getenv('CIRCLE_REPOSITORY_URL'),
                commit=os.getenv('CIRCLE_SHA1'),
                commit_range=os.getenv('CIRCLE_SHA1'),
                tag=os.getenv('CIRCLE_TAG'),
                branch=os.getenv('CIRCLE_BRANCH'),
                build_nr=os.getenv('CIRCLE_BUILD_NUM'),
                os_name='linux',
                job_id=os.getenv('CIRCLE_BUILD_URL'))


def detect():
    for ci in CISystem.__subclasses__():
        res = ci.detect()
        if res:
            return res
    return None
