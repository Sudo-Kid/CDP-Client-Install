#!/usr/bin/env python

import urllib
import platform
import subprocess
import os
import sys

class R1soft():

    osDistro = platform.dist()[0].lower()
    osVersion = platform.dist()[1]
    repoFile = ''
    repoDir = ''
    repo = ''

    def setOSVerables(self):
        if 'redhat' in self.osDistro or 'centos' in self.osDistro:
            self.repoFile = 'r1soft.repo'
            self.repoDir = '/etc/yum.repos.d/'
            self.repo = '{0}{1}{2}{3}{4}'.format('[r1soft]\n', 
                'name=R1Soft Repository Server\n', 
                'baseurl=http://repo.r1soft.com/yum/stable/\$basearch\n',
                'enabled=1\n',
                'gpgcheck=0')
        elif 'debian' in self.osDistro or 'ubuntu' in self.osDistro:
            self.repoFile = 'sources.list'
            self.repoDir = '/etc/apt/'
            self.repo = 'deb http://repo.r1soft.com/apt stable main'
        else:
            print('Your system is not supported')
            sys.exit()
        return

    def addRepo(self):
        # Adding repo for RedHat
        if 'redhat' in self.osDistro or 'centos' in self.osDistro:
            # If the file does not excites self will create it
            if not os.path.isfile(self.repoDir + self.repoFile):
                file = open(self.repoDir + self.repoFile, 'w')
                file.close()

            file = open(self.repoDir + self.repoFile, 'a+')

            if self.repo in file.read():
                print('The CDP repo has already been added')
            else:
                file.write(repo)
            file.close()
            return

        # Adding repo for Debian
        elif 'debian' in osDistro or 'centos' in osDistro:
            # If the file does not excites self will create it
            if not os.path.isfile(self.repoDir + self.repoFile):
                file = open(self.repoDir + self.repoFile, 'w')
                file.close()

            file = open(self.repoDir + self.repoFile, 'a+')

            if self.repo in file.read():
                print('The CDP repo has already been added!')
            else:
                file.write(self.repo)
            file.close()
        return

    def installPackage(self):
        if 'redhat' in self.osDistro or 'centos' in self.osDistro:
            subprocess.call(['yum', 'install', 'r1soft-cdp-enterprise-agent', '-y'])
        elif 'debian' in self.osDistro or 'centos' in self.osDistro:
            subprocess.call(['apt-get', 'install', 'r1soft-cdp-enterprise-agent', '-y'])
        return

    def getHeaders(self):
        kernelRelease = platform.release()

        if 'redhat' in self.osDistro or 'centos' in self.osDistro:
            if '7' in self.osVersion[0]:
                url = '{}{}{}'.format('http://repo.r1soft.com/modules/Centos_7_x64/hcpdriver-cki-', 
                    kernelRelease, '.ko')
                try:
                    urllib.urlretrieve(url, '/lib/modules/r1soft/hcpdriver.ko')
                except IOError:
                    print('We could not connect to the requested server please check' +
                        'your network connection and try again')
            elif '6' in osVersion[0] or '5' in osVersion[0]:
                subprocess.call(['yum', 'install', 'kernel-devel', 'kernel-headers', '-y'])
            elif '4' in osVersion[0]:
                subprocess.call(['up2date', 'install', 'glibc-kernheaders', 'kernel-devel', '-y'])
            else:
                subprocess.call(['yum', 'install', 'linux-headers' + kernelRelease, '-y'])
        elif 'debian' in osDistro:
            subprocess.call(['apt-get', 'install', 'linux-headers-' + kernelRelease, '-y'])

        subprocess.call(['r1soft-setup', '--get-module', '&&', '/etc/init.d/cdp-agent', 'restart'])
        return

cdp = R1soft()

cdp.setOSVerables()
cdp.addRepo()
cdp.installPackage()
cdp.getHeaders()
sys.exit()