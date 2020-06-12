from twisted.internet import defer
from twisted.internet import reactor
from twisted.python import log

from buildbot import config as bbconfig
from buildbot.interfaces import WorkerTooOldError
from buildbot.process import buildstep
from buildbot.steps.worker import CompositeStepMixin
from buildbot.util.git import GitStepMixin

class GitPull(buildstep.BuildStep, GitStepMixin, CompositeStepMixin):
    description = None
    descriptionDone = None
    descriptionSuffix = None

    name = 'gitpull'
    renderables = ['repourl', 'branch', 'subtree']

    def __init__(self, workdir=None, repourl=None, branch=None, subtree=None, force=False,
                 env=None, timeout=20 * 60, logEnviron=True,
                 sshPrivateKey=None, sshHostKey=None, sshKnownHosts=None,
                 config=None, **kwargs):

        self.workdir = workdir
        self.repourl = repourl
        self.branch = branch
        self.force = force
        self.env = env
        self.timeout = timeout
        self.logEnviron = logEnviron
        self.sshPrivateKey = sshPrivateKey
        self.sshHostKey = sshHostKey
        self.sshKnownHosts = sshKnownHosts
        self.config = config
        self.subtree = subtree

        super().__init__(**kwargs)

        self.setupGitStep()

        if not self.branch:
            bbconfig.error('GitPull: must provide branch')

    def _getSshDataWorkDir(self):
        return self.workdir
    
    def _isSshPrivateKeyNeededForGitCommand(self):
        return True

    @defer.inlineCallbacks
    def run(self):
        self.stdio_log = yield self.addLog("stdio")
        try:
            gitInstalled = yield self.checkFeatureSupport()

            if not gitInstalled:
                raise WorkerTooOldError("git is not installed on worker")

            yield self._downloadSshPrivateKeyIfNeeded()
            ret = yield self._doPull()
            yield self._removeSshPrivateKeyIfNeeded()
            return ret

        except Exception as e:
            yield self._removeSshPrivateKeyIfNeeded()
            raise e

    @defer.inlineCallbacks
    def _doPull(self):
        cmd = []
        if self.subtree is not None:
            cmd += ["subtree", 'pull', '--prefix', self.subtree]
        else:
            cmd += ['pull']
        cmd += [self.repourl, self.branch]

        ret = yield self._dovccmd(cmd)
        return ret