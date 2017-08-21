#/bin/bash
if [ `id` -eq  0 ]; then
   echo 'run as root'
   exit
fi
cd ~/
	wget --no-check-certificate https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
	tar xf Python-2.7.9.tar.xz
	cd Python-2.7.9
	./configure --prefix=/usr/local
	make && make install
	mv /usr/bin/python /usr/bin/python2.6.6
	ln -s /usr/local/bin/python2.7 /usr/bin/python
	sed -i 's#/usr/bin/python#/usr/bin/python2.6.6#'  /usr/bin/yum
cd ~/

	wget https://codeload.github.com/pypa/setuptools/zip/master -O setuptools-master.zip
	unzip setuptools-master.zip
	cd setuptools-master
	python bootstrap.py
	python setup.py  install

cd ~/

	wget https://codeload.github.com/pypa/pip/zip/master -O pip-master.zip
	unzip pip-master.zip
	cd pip-master
	python setup.py  install

cd ~
pip install fabric
