### Install python 
yum -y install centos-release-openstack-packstack-queens
> Centos
```
sudo -i
yum groupinstall -y "Development Tools"
yum install -y zlib-devel
cd /usr/src
wget https://python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
tar xf Python-3.7.3.tar.xz
cd Python-3.7.3
./configure --enable-optimizations --with-ensurepip=install
make altinstall
exit

```
> Ubuntu

```
sudo -i
apt update -y
apt install -y \
  wget \
  build-essential \
  libffi-dev \
  libgdbm-dev \
  libc6-dev \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  libncurses5-dev \
  libncursesw5-dev \
  xz-utils \
  tk-dev

cd /usr/src
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
tar xf Python-3.7.3.tar.xz
cd Python-3.7.3.tar.xz
./configure --enable-optimizations --with-ensurepip=install
make altinstall
exit

```

> Other

```
Ensure Python 3 Works with sudo
Make sure secure_path in the /etc/sudoers file includes /usr/local/bin. The line should look something like this:

Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin
Upgrade Pip
Note: This is not always necessary.

The version of pip we have might be up to date, but it's a good practice to try to update it after installation. Because we are working with Python 3, we need to use the pip3.7 executable, and we will use sudo so we can write files under the /usr/local directory.

sudo pip3.7 install --upgrade pip

```