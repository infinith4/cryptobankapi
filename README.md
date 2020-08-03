sudo apt update
sudo apt install -y python3.8


https://github.com/bitbankinc/python-bitbankcc

pipenv install git+https://github.com/bitbankinc/python-bitbankcc.git#egg=python-bitbankcc
pipenv install requests
pipenv install yaml
pipenv install cryptocom-exchange

## restore from pipfile

pipenv install

## To activate this project's virtualenv run

pipenv shell

## Start

pipenv run start

## deactivate

exit

