import os
from solc import compile_files
from web3 import Web3
from web3.utils.threads import (
    Timeout,
)


def compile_contracts(contract_name):
    """compiles a contract situated in blockchain/contracts/contracts with file name contract_name.sol
    returns the abi and bytecode"""
    path_to_contract_source_code = (os.path.join(os.path.dirname(__file__),
                                                 os.pardir,
                                                 "contracts",
                                                 contract_name + ".sol"))

    compiled_sol = compile_files([path_to_contract_source_code])
    contract_interface = compiled_sol[path_to_contract_source_code + ":" + contract_name]

    return contract_interface


def deploy_compiled_contract(contract_interface, web3, *args):
    contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    txhash = contract.constructor(*args).transact()
    receipt = check_successful_tx(web3, txhash)
    id_address = receipt["contractAddress"]
    return contract(id_address)


class TransactionFailed(Exception):
    pass


def wait_for_transaction_receipt(web3, txid, timeout=180):
    with Timeout(timeout) as time:
            while not web3.eth.getTransactionReceipt(txid):
                time.sleep(5)

    return web3.eth.getTransactionReceipt(txid)


def check_successful_tx(web3: Web3, txid: str, timeout=180) -> dict:
    """See if transaction went through (Solidity code did not throw).
    :return: Transaction receipt
    """
    receipt = wait_for_transaction_receipt(web3, txid, timeout=timeout)
    tx_info = web3.eth.getTransaction(txid)
    status = receipt.get("status", None)
    if receipt["gasUsed"] == tx_info["gas"] or status is False:
        raise TransactionFailed
    return receipt
