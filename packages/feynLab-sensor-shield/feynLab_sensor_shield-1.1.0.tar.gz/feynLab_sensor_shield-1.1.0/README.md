Installing : 

sudo apt install python-smbus

sudo apt-get install i2c-tools

sudo pip install requests


//python setup.py sdist bdist_wheel
//twine upload --repository-url https://test.pypi.org/legacy/ dist/*
//twine upload --repository-url https://pypi.org/legacy/ dist/*
