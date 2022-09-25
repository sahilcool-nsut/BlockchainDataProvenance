from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json
lotteryAbi = [
    { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" },
    {
        "inputs": [],
        "name": "enter",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getBalance",
        "outputs": [{ "internalType": "uint256"," name": "", "type": "uint256" }],
        "tateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getPlayers",
        "outputs": [
        { "internalType": "address payable[]", "name": "", "type": "address[]" },
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getRandomNumber",
        "outputs": [{ "internalType": "bytes32", "name": "requestId", "type": "bytes32" }],
        "stateMutability": "nonpayable",
        'type': "function",
    },
    {
        "inputs": [{ "internalType": "uint256", "name": "lottery", "type": "uint256" }],
        "name": "getWinnerByLottery",
        "outputs": [{ "internalType": "address payable", "name": "", "type": "address" }],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
        "name": "lotteryHistory",
        "outputs": [{ "internalType": "address payable", "name": "", "type": "address" }],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "lotteryId",
        "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{ "internalType": "address", "name": "", "type": "address" }],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "payWinner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "pickWinner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
        "name": "players",
        "outputs": [{ "internalType": "address payable", "name": "", "type": "address" }],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "randomResult",
        "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
        { "internalType": "bytes32", "name": "requestId", "type": "bytes32" },
        { "internalType": "uint256", "name": "randomness", "type": "uint256" },
        ],
        "name": "rawFulfillRandomness",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
lotteryAddress="0xaB9858163DeC63663bEb6C5Fc697ca12e97Be26e"
def interactWithSmartContract ():
    print("inside interactWithSmartContract function")
    web3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/b85e8248ce5548038da1ccb22100b77a"))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(web3.isConnected())
    # print("Completed")
    # balance = web3.eth.get_balance("0xE0f5Ef3120ad5d012112eca9792a151230C8cEab")
    lotteryContract = web3.eth.contract(address=lotteryAddress, abi=lotteryAbi)
    print(lotteryContract)
    lotteryId = lotteryContract.functions.lotteryId().call()
    print("ID: " + str(lotteryId))
    history = lotteryContract.functions.lotteryHistory(lotteryId).call()
    print(history)
    potAmount = lotteryContract.functions.getBalance().call()
    print(potAmount)
    players =lotteryContract.functions.getPlayers().call()
    print(players)