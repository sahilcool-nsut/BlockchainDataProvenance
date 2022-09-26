from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json

contractAbi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "eventt",
                "type": "uint256"
            }
        ],
        "name": "insertEntry",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "transcationData",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "operation",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
contractAddress = "0x66c3Aa6F43061fa81380940Fc4Bd05809E7Ba2BE"

userAddress = "0xE0f5Ef3120ad5d012112eca9792a151230C8cEab"

class CustomWeb3:
    def __init__(self):
        self.webObject = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/b85e8248ce5548038da1ccb22100b77a"))
        self.webObject.middleware_onion.inject(geth_poa_middleware, layer=0)
        print("Web3 is connected? : " + str(self.webObject.isConnected()))
        self.provContract = self.webObject.eth.contract(address=contractAddress, abi=contractAbi)
        

    def insertEventInSmartContract(self,):
    
        privateKey = "60d5687eeb10f16d44d6c8c6510fd526a868ee10ff370458a31e9c6b39c28f39" 
        nonce = self.webObject.eth.getTransactionCount(userAddress)  #SC OWNER ADDR
        gasPrice = self.webObject.eth.gasPrice
        gasPriceHex = self.webObject.toHex(gasPrice)
        # gasLimitHex = self.webObject.toHex(3000000)
        try:
            transaction = self.provContract.functions.insertEntry(12).buildTransaction({
                # "gas": ??????
                "gasPrice": gasPriceHex,
                # "gasLimit": gasLimitHex,          error dera
                "from": userAddress,
                "nonce":nonce
            }) 
            print("created transaction object")
            signedTxn = self.webObject.eth.account.signTransaction(transaction, private_key=privateKey)
            print("signed transaction")
            transactionHash = self.webObject.eth.sendRawTransaction(signedTxn.rawTransaction)
            print("sent transaction")
            print(self.webObject.toHex(transactionHash))
        except Exception as e:
            print(e)
        # one for address, second for entry
        

    def retrieveBlockChainData(self):
        finalList=[]
        for i in range(0,6):
            var = self.provContract.functions.transcationData(userAddress,i).call()
            finalList.append(var)
        print("after finallist")
        print(type(finalList))
        print(finalList)
        return finalList



