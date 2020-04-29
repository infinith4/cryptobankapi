https://github.com/bitbankinc/python-bitbankcc

python -m venv --without-pip .venv
source .venv/bin/activate

pip3 install pybitflyer

sudo apt install python3-venv

pipenv install git+https://github.com/bitbankinc/python-bitbankcc.git#egg=python-bitbankcc
pipenv install requests
pip install requests
pip install pybitflyer

## restore from pipfile

pipenv install


## Start

pipenv run start