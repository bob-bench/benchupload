import os
import copy
import unittest
from benchupload import cidetect

class TestCIDetect(unittest.TestCase):
    def setUp(self):
        self.env = copy.deepcopy(os.environ)
        self.cleanEnv()

    def tearDown(self):
        os.environ = self.env

    def cleanEnv(self):
        """Remove all non supported environments"""
        valid_keys = ['_', 'TERM', 'Apple_PubSub_Socket_Render', 'SHLVL', 'SSH_AUTH_SOCK', 'SECURITYSESSIONID', 'TERM_SESSION_ID', 'TERM_PROGRAM_VERSION', 'LC_CTYPE', '__CF_USER_TEXT_ENCODING', 'PWD', 'SHELL', 'LOGNAME', 'USER', 'XPC_SERVICE_NAME', 'HOME', 'PATH', 'XPC_FLAGS', 'DISPLAY', 'TMPDIR', 'TERM_PROGRAM']
        for key in copy.deepcopy(os.environ.keys()):
            if not key in valid_keys:
                del os.environ[key]

    def testDetectTravisCI(self):
        os.environ['CI'] = 'true'
        os.environ['TRAVIS'] = 'true'
        os.environ['TRAVIS_REPO_SLUG'] = 'bobbench/citool'
        os.environ['TRAVIS_COMMIT'] = '1234abcdef'
        os.environ['TRAVIS_COMMIT_RANGE'] = '???'
        os.environ['TRAVIS_TAG'] = ''
        os.environ['TRAVIS_BRANCH'] = 'branchname'
        os.environ['TRAVIS_JOB_NUMBER'] = '4.1'
        os.environ['TRAVIS_OS_NAME'] = 'linux'
        os.environ['TRAVIS_JOB_ID'] = '231232133'
        os.environ['TRAVIS_PULL_REQUEST'] = 'false'

        res = cidetect.detect()
        self.assertIsNotNone(res)
        self.assertEquals(res.system_name(), "travis-ci")
        self.assertTrue(res.is_github)
        self.assertEquals(res.commit, '1234abcdef')
        self.assertEquals(res.commit_range, '???')
        self.assertEquals(res.repo_url, 'https://github.com/bobbench/citool')
        self.assertEquals(res.tag, '')
        self.assertEquals(res.branch, 'branchname')
        self.assertEquals(res.build_nr, '4.1')
        self.assertEquals(res.prev_build_nr, None)
        self.assertEquals(res.os_name, 'linux')
        self.assertEquals(res.job_id, '231232133')
        self.assertEquals(res.is_pull_request, False)

        os.environ['TRAVIS_PULL_REQUEST'] = '33.4'
        res = cidetect.detect()
        self.assertIsNotNone(res)
        self.assertEquals(res.is_pull_request, True)
        self.assertEquals(res.pull_request, '33.4')

    def testDetectCircleci(self):
        os.environ['CIRCLECI'] = 'true'
        os.environ['CI'] = 'true'
        os.environ['CI_PULL_REQUEST'] = 'https://blabla.com/pullrequest/1'
        os.environ['CIRCLE_ARTIFACTS'] = '/tmp/bla/'
        os.environ['CIRCLE_BRANCH'] = 'branchname'
        os.environ['CIRCLE_BUILD_IMAGE'] = '????'
        os.environ['CIRCLE_BUILD_NUM'] = 'circleci.com/gh/foo/bar/123'
        os.environ['CIRCLE_BUILD_URL'] = 'https://circleci.com/gh/circleci/frontend/933'
        os.environ['CIRCLE_COMPARE_URL'] = 'https://github.com/bla/foo/comparestuff'
        os.environ['CIRCLE_NODE_INDEX'] = '0'
        os.environ['CIRCLE_NODE_TOTAL'] = '1'
        os.environ['CIRCLE_PREVIOUS_BUILD_NUM'] = 'circleci.com/gh/foo/bar/122'
        os.environ['CIRCLE_PROJECT_REPONAME'] = 'bar'
        os.environ['CIRCLE_PROJECT_USERNAME'] = 'foo'
        os.environ['CIRCLE_REPOSITORY_URL'] = 'https://github.com/circleci/frontend'
        os.environ['CIRCLE_SHA1'] = '1234abcdef'
        os.environ['CIRCLE_TEST_REPORTS'] = '/tmp/bla/out'
        os.environ['CIRCLE_USERNAME'] = 'foo'
        os.environ['CIRCLE_TAG'] = 'release-v1.5.4'

        res = cidetect.detect()
        self.assertIsNotNone(res)
        self.assertEquals(res.system_name(), "circleci")
        self.assertTrue(res.is_github)
        self.assertEquals(res.commit, '1234abcdef')
        self.assertEquals(res.commit_range, '1234abcdef')
        self.assertEquals(res.repo_url, 'https://github.com/circleci/frontend')
        self.assertEquals(res.tag, 'release-v1.5.4')
        self.assertEquals(res.branch, 'branchname')
        self.assertEquals(res.build_nr, 'circleci.com/gh/foo/bar/123')
        self.assertEquals(res.prev_build_nr, 'circleci.com/gh/foo/bar/122')
        self.assertEquals(res.os_name, 'linux')
        self.assertEquals(res.job_id, 'https://circleci.com/gh/circleci/frontend/933')
