Cloud Filer
===========

Cloud Filer is a cloud storage file management GUI client.  Cloud Filer allows you to upload and download files to cloud storage (e.g. Amazon S3) and can be used as part of a backup strategy.

Cloud Filer uses pre-internet encryption and file name obfuscation making access to your cloud data useless without the right password.

For more details see https://www.cloudfiler.org/


Installing on Linux
-------------------

On Linux you need to install the following packages:

apt install python-wxgtkX.Y python-wxtools wxX.Y-i18n python-pip

and then install Cloud Filer using pip:

pip install cloudfiler


Installing on Windows
---------------------

Install python 2.x from https://www.python.org

Install wxpython from https://wxpython.org

Install Microsoft Visual C++ Compiler for Python 2.7 from http://aka.ms/vcpython27

pip install cloudfiler


Running Cloud Filer
-------------------

python -m cloudfiler

