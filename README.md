https://github.com/bitbankinc/python-bitbankcc

pip3 install pybitflyer

sudo apt install python3-venv

python -m venv --without-pip .venv
source .venv/bin/activate

pipenv install git+https://github.com/bitbankinc/python-bitbankcc.git#egg=python-bitbankcc
pipenv install requests
pip install requests
pip install pybitflyer

## restore from pipfile

pipenv install


## Start

pipenv run start