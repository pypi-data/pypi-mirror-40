import ConfigParser
import tempfile
import git
import logging
import os
import shutil
import subprocess
import re
import sys
import argparse

mswindows = (sys.platform == "win32")

logger = logging.getLogger('AUTOBUILD')
logging.basicConfig(level=logging.INFO)

TEMPDIR = os.path.join(tempfile.gettempdir(), "autobuild")
os.makedirs(TEMPDIR) if not os.path.exists(TEMPDIR) else 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_CONF = "config.ini"


def read_subprocess(sp):
    while True:
        log = sp.stdout.readline()
        logger.info(log)
        if sp.poll() is not None:
            break

def read_error_subprocess(sp):
    while True:
        log = sp.stdout.readline()
        logger.info(log)
        if sp.poll() is not None:
            break

def setvalue(conf, section, obj):
    options = conf.options(section)
    for op in options:
        setattr(obj, op, conf.get(section, op))


def setarg(myparser, obj):
    if myparser.sha:
        obj.sha = myparser.sha
    if myparser.branch:
        obj.branch = myparser.branch


def mymakedir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def copydir(sourceDir, targetDir):
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(sourceF):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetF) or (
                    os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                open(targetF, "wb").write(open(sourceF, "rb").read())
        if os.path.isdir(sourceF):
            copydir(sourceF, targetF)


def copyfile(sourcefile, targetfile):
    shutil.copy(sourcefile, targetfile)


def remove_file(path):
    shutil.rmtree(path, True)
    if os.path.exists(path):
        if mswindows:
            os.system('rd/s/q %s' % path)
        else:
            os.system('rm -rf %s' % path)


class Project(object):
    def __init__(self):
        self.projectdir = ""
        self.name = ""
        self.url = ""
        self.command = "build.bat qa"
        self.branch = ""
        self.package = ""
        self.sha = ""
        self.packages = []
        self.files = []
        self.basedir = BASE_DIR

    def init(self):
        if type(self.packages) is str:
            self.packages = str(self.packages).split(',')
        if type(self.files) is str:
            self.files = str(self.files).split(',')
        if self.projectdir == "":
            self.projectdir = os.path.join(TEMPDIR, self.name)
        else:
            self.projectdir = os.path.join(self.projectdir, self.name)
        # self.url = self.set_url()
        if hasattr(self, 'targetpath'):
            self.basedir = os.path.abspath(self.targetpath)
        print self.url

    def remove(self):
        if os.path.exists(self.projectdir):
            shutil.rmtree(self.projectdir)

    def set_url(self):
        if hasattr(self, 'username'):
            url = "https://%s:%s@%s" % (self.username, self.password, self.url.split("//")[-1])
            return url
        else:
            return self.url

    def git_clone(self):
        try:
            logger.info('git clone project:%s' % self.projectdir)
            if os.path.exists(self.projectdir):
                self.git_checkout_branch()
            else:
                self.git_config_ssl()
                git.Repo.clone_from(self.url, self.projectdir)
                self.git_checkout_branch()
            return True
        except Exception, e:
            logger.error(e)
            return self.re_clone()

    def re_clone(self):
        try:
            remove_file(self.projectdir)
            self.git_config_ssl()
            git.Repo.clone_from(self.url, self.projectdir)
            self.git_checkout_branch()
            return True
        except Exception, e:
            logger.error("re_clone error:%s" % e)
            return False

    def git_config_ssl(self):
        g = git.Git(TEMPDIR)
        g.execute(["git", "config", "--global", "http.sslVerify", "false"])

    def git_checkout_branch(self):
        g = git.Git(self.projectdir)
        logger.info('git pull project:%s' % self.name)
        if self.sha != "":
            logger.info('git checkout %s' % self.sha)
            g.execute(["git", "checkout", self.sha])
        else:
            g.execute(["git", "checkout", self.branch])
            g.pull()
            logger.info('git checkout %s' % self.branch)
            g.execute(["git", "config", "core.longpaths", "true"])
            g.clean('-xdf')
            g.execute(["git", "reset", "--hard"])
            if self.branch != "":
                g.checkout(self.branch)

    def build(self):
        logger.info('package project:%s' % self.name)
        os.chdir(self.projectdir)
        logger.info(self.command)
        sp = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        read_subprocess(sp)

    def movetoloacal(self):
        for p in self.packages:
            warpath = p.split(':')[0]
            war_unzip_name = p.split(':')[-1]
            srcpath = os.path.join(self.projectdir, warpath)
            srcpath_dir = os.path.dirname(srcpath)
            srcpath_file_war = os.path.basename(srcpath)
            if '$d' in srcpath_file_war:
                srcpath_file_war = srcpath_file_war.replace("$d", "\d.*")
                for i in os.listdir(srcpath_dir):
                    if os.path.isfile(os.path.join(srcpath_dir, i)):
                        p = re.compile(srcpath_file_war)
                        rs = p.findall(i)
                        if rs:
                            srcpath_file_war = rs[0]
                            break
            srcpath = os.path.join(srcpath_dir, srcpath_file_war)
            if not os.path.exists(srcpath):
                logger.error("File is not exists:%s" % srcpath)
                return False
            targetpath = os.path.join(self.basedir, war_unzip_name)
            mymakedir(targetpath)
            os.chdir(targetpath)
            command = 'jar -xvf %s' % srcpath
            logger.info(command)
            os.popen(command)
        for f in self.files:
            sourcefile = f.split(':')[0]
            filename = f.split(':')[-1]
            srcpath = os.path.join(self.projectdir, sourcefile)
            targetpath = os.path.join(self.basedir, filename)
            if os.path.isdir(srcpath):
                copydir(srcpath, targetpath)
            elif os.path.isfile(srcpath):
                copyfile(srcpath, targetpath)

myparser = None

def main():
    conf = ConfigParser.ConfigParser()
    conf.read(os.path.join(BASE_DIR, PROJECT_CONF))
    sections = conf.sections()
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="git commit sha code", dest='sha', default=None)
    parser.add_argument("-b", help="git branch", dest='branch', default=None)
    parser.add_argument("run", help="run script")
    myparser = parser.parse_args()
    for section in sections:
        p = Project()
        setvalue(conf, section, p)
        setarg(myparser, p)
        p.init()
        if p.git_clone():
            p.build()
        p.movetoloacal()

if __name__ == '__main__':
    main()
    logger.info('done')























