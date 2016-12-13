#!/usr/bin/env bash
#encoding=utf8
lintpath=$(cd "$(dirname "$0")"; pwd)
backuppath=$lintpath"/backup"

function lintUpdate () {
cd $lintpath
echo "Start LINT Update from Github"
git pull
git submodule update --init --recursive
git submodule foreach git pull origin master
source bin/activate
echo "Start Dependency Install or Upgrade"
pip install -r requirements.txt --upgrade
pip install -r requirements.txt
}

function SExtractorInstall () {
echo "Start SExtractor Install."
wget http://www.astromatic.net/download/sextractor/sextractor-2.19.5.tar.gz
fi
tar -xf sextractor-2.19.5.tar.gz
cd sextractor-2.19.5/
./configure
make
make install
cd ..
rm -rf sextractor-2.19.5.tar.gz
}

function lintInstall () {
cd $lintpath
if [ "$(uname -s)" == "Darwin" ]
then
echo "You are on Mac OS"
brew update
brew install --devel protobuf
elif [ $(uname -s) == CYGWIN* ]
then
echo "You are on Cygwin"
if [ !-x "$(command -v apt-cyg)" ]
then
wget http://apt-cyg.googlecode.com/svn/trunk/apt-cyg
chmod +x apt-cyg
mv apt-cyg /usr/local/bin/
fi
apt-cyg install gcc-core make
easy_install pip
elif [ -x "$(command -v apt-get)" ]
then
echo "You are on Debian/Ubuntu"
sudo apt-get update
sudo apt-get -y install python python-pip python-dev gcc make git
elif [ -x "$(command -v yum)" ]
then
echo "You are on CentOS/RedHat"
sudo yum -y install epel-release gcc make
sudo yum -y install python-pip python-devel
elif [ -x "$(command -v pacman)" ]
then
echo "You are on Arch Linux"
sudo pacman -Sy python2 python2-pip gcc make
elif [ -x "$(command -v dnf)" ]
then
echo "You are on Fedora/RHEL"
sudo dnf update
sudo dnf -y install python-pip python-devel gcc make
elif [ -x "$(command -v zypper)" ]
then
echo "You are on Open SUSE"
sudo zypper update
sudo zypper -y install python-pip python-devel gcc make
else
echo "Please check if you have  python pip gcc make  installed on your device."
echo "Wait 5 seconds to continue or Use ctrl+c to interrupt this shell."
sleep 5
fi
lintUpdate
SExtractorInstall
echo "Install complete."
}

function lintHelp () {
echo "usage:"
echo "	-i,--install.		Install LINT."
echo "	-b,--backup.		Backup config files."
echo "	-u,--update.		Command git pull to update."
}

case $* in
--install|-i)
lintInstall
;;
--update|-u)
lintUpdate
;;
--backup|-b)
mkdir -p $backuppath
cp -f $lintpath/*.config $backuppath/
cp -f $lintpath/*.txt $backuppath/
echo "Backup complete."
;;
--help|-h)
lintHelp
;;
*)
lintHelp
;;
esac
exit 0
