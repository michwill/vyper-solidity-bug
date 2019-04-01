import pytest
from eth_tester import EthereumTester, PyEVMBackend
from web3 import Web3
import os
import subprocess
import json
from os.path import dirname, join, realpath
from vyper import compile_code
from web3.contract import ConciseContract

CONTRACT_PATH = join(dirname(dirname(realpath(__file__))), 'contracts')


@pytest.fixture(scope='session')
def compile_sol():
    sol_bin_path = os.path.join(CONTRACT_PATH, 'bin')
    if not os.path.exists(sol_bin_path):
        os.mkdir(sol_bin_path)
    result = subprocess.call(['solc', '-o', sol_bin_path, '--bin', '--abi',
                              '--overwrite', join(CONTRACT_PATH, 'solcontract.sol')])
    assert result == 0

    with open(os.path.join(sol_bin_path, 'SolContract.bin'), 'r') as f:
        contract_bin = bytes.fromhex(f.read())

    with open(os.path.join(sol_bin_path, 'SolContract.abi'), 'rb') as f:
        contract_abi = json.load(f)

    return contract_bin, contract_abi


@pytest.fixture
def tester():
    return EthereumTester(backend=PyEVMBackend(), auto_mine_transactions=True)


@pytest.fixture
def w3(tester):
    w3 = Web3(Web3.EthereumTesterProvider(tester))
    w3.eth.setGasPriceStrategy(lambda web3, params: 0)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3


@pytest.fixture
def solcontract(w3, compile_sol):
    contract, abi = compile_sol
    deployer = w3.eth.contract(abi=abi, bytecode=contract)
    txhash = deployer.constructor().transact()
    receipt = w3.eth.getTransactionReceipt(txhash)
    assert receipt.contractAddress

    return ConciseContract(w3.eth.contract(
        address=receipt.contractAddress,
        abi=abi))


@pytest.fixture
def vycontract(w3, solcontract):
    with open(join(CONTRACT_PATH, 'vycontract.vy')) as f:
        source = f.read()
    code = compile_code(source, ['bytecode', 'abi'])
    deploy = w3.eth.contract(abi=code['abi'],
                             bytecode=code['bytecode'])
    tx_hash = deploy.constructor(solcontract.address).transact({'from': w3.eth.accounts[1]})
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return ConciseContract(w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=deploy.abi))
