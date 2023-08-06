#Test
##Test

sudo python setup.py install
python3 -m pip install --user --upgrade setuptools wheel
sudo python3 setup.py sdist bdist_wheel

Install to to upload to pypi:
python3 -m pip install --user -upgrade twine
twine upload --repository-url https://test.pypi.org/legacy dist/*  
or
python3 -m twine upload --repository-url https://test.pypi.org/legacy dist/*  

