from brownie import Lottery, accounts, network, config
from web3 import Web3
import pytest
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)
from scripts.deploy_lottery import deploy_lottery


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(60)
    assert lottery.recentWinner == account
    assert lottery.balance() == 0


def test_get_entrace_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    print(f"Entrance fee is {lottery.getEntranceFee()}")
    print(f'Converted fee is {Web3.toWei(0.00000, "ether")}')
    # assert lottery.getEntranceFee() > Web3.toWei(0.00000, "ether")


def main():
    test_get_entrace_fee()
