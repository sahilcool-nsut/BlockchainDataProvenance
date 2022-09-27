from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json

# contractAbi = [
#     {
#         "inputs": [
#             {
#                 "internalType": "uint256",
#                 "name": "eventt",
#                 "type": "uint256"
#             }
#         ],
#         "name": "insertEntry",
#         "outputs": [],
#         "stateMutability": "payable",
#         "type": "function"
#     },
#     {
#         "inputs": [
#             {
#                 "internalType": "address",
#                 "name": "",
#                 "type": "address"
#             },
#             {
#                 "internalType": "uint256",
#                 "name": "",
#                 "type": "uint256"
#             }
#         ],
#         "name": "transcationData",
#         "outputs": [
#             {
#                 "internalType": "uint256",
#                 "name": "operation",
#                 "type": "uint256"
#             }
#         ],
#         "stateMutability": "view",
#         "type": "function"
#     }
# ]
# contractAddress = "0x66c3Aa6F43061fa81380940Fc4Bd05809E7Ba2BE"
contractAbi = [
	{
		"inputs": [],
		"name": "clearList",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "eventt",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "timeStamp",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "dbName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "clusterName",
				"type": "string"
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
				"internalType": "string",
				"name": "timeStamp",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "tHash",
				"type": "string"
			}
		],
		"name": "updateTransactionHash",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			}
		],
		"name": "Sizee",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
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
		"name": "transactionData",
		"outputs": [
			{
				"internalType": "string",
				"name": "timeStp",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "DBName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "ClusName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "operation",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "tranHash",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
contractAddress = "0x385cd8Fc9EFf56a027E4b0DBEe4E98278b9f63E1"
userAddress = "0xE0f5Ef3120ad5d012112eca9792a151230C8cEab"

class CustomWeb3:
    def __init__(self):
        self.webObject = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/b85e8248ce5548038da1ccb22100b77a"))
        self.webObject.middleware_onion.inject(geth_poa_middleware, layer=0)
        print("Web3 is connected? : " + str(self.webObject.isConnected()))
        self.provContract = self.webObject.eth.contract(address=contractAddress, abi=contractAbi)
        

    def insertEventInSmartContract(self,data):
    
        operationType = str(data["operationType"])
        timeStamp = str(data["clusterTime"]["$timestamp"]["t"])
        dbUsed = str(data["ns"]["db"])
        collectionUsed = str(data["ns"]["coll"])
        print(operationType)
        print(timeStamp)
        print(dbUsed)
        print(collectionUsed)
        privateKey = "60d5687eeb10f16d44d6c8c6510fd526a868ee10ff370458a31e9c6b39c28f39" 
        nonce = self.webObject.eth.getTransactionCount(userAddress)  #SC OWNER ADDR
        gasPrice = self.webObject.eth.gasPrice
        gasPriceHex = self.webObject.toHex(gasPrice)
        # gasLimitHex = self.webObject.toHex(3000000)
        # try:
        transaction = self.provContract.functions.insertEntry(operationType,timeStamp,dbUsed,collectionUsed).buildTransaction({
            "gasPrice": gasPriceHex,
            "from": userAddress,
            "nonce":nonce
        }) 
        print("created transaction object")
        signedTxn = self.webObject.eth.account.signTransaction(transaction, private_key=privateKey)
        print("signed transaction")
        transactionHash = self.webObject.eth.sendRawTransaction(signedTxn.rawTransaction)
        print("sent transaction1")
        print(type(transactionHash))
        print(transactionHash)
        print(self.webObject.toHex(transactionHash))
        print(str(self.webObject.toHex(transactionHash)))
        strTransactionHash = str(self.webObject.toHex(transactionHash))
        print(type(strTransactionHash))
        # Now create new transaction to store the transaction hash
        # First get the index from the timestamp->index mapping
        gasPrice2 = self.webObject.eth.gasPrice
        gasPriceHex2 = self.webObject.toHex(gasPrice2)
        nonce2 = self.webObject.eth.getTransactionCount(userAddress)  #SC OWNER ADDR
        transaction2 = self.provContract.functions.updateTransactionHash(timeStamp,"hello").buildTransaction({
            "gasPrice": gasPriceHex2,
            "from": userAddress,
            "nonce":nonce2
        }) 
        print("created transaction2 object")
        signedTxn2 = self.webObject.eth.account.signTransaction(transaction2, private_key=privateKey)
        print("signed transaction2")
        transactionHash2 = self.webObject.eth.sendRawTransaction(signedTxn2.rawTransaction)
        print("sent transaction2")
        print(self.webObject.toHex(transactionHash2))
        # except Exception as e:
        #     print(e)
        # one for address, second for entry
        

    def retrieveBlockChainData(self):
        finalList=[]
        listLength = self.provContract.functions.Sizee(userAddress).call()
        print(listLength)
        urlsList=[]
        for i in range(0,listLength):
            var = self.provContract.functions.transactionData(userAddress,i).call()
            txHash = var[len(var)-1]        #Last entry is the hash
            txLink = "https://rinkeby.etherscan.io/tx/" + txHash
            urlsList.append(txLink)    
            var.insert(0,i+1)
            print(var)
            finalList.append(var)
        print(urlsList)
        return finalList,urlsList

    def clearBlockChainData(self):
        privateKey = "60d5687eeb10f16d44d6c8c6510fd526a868ee10ff370458a31e9c6b39c28f39" 
        nonce = self.webObject.eth.getTransactionCount(userAddress)  #SC OWNER ADDR
        gasPrice = self.webObject.eth.gasPrice
        gasPriceHex = self.webObject.toHex(gasPrice)
        # gasLimitHex = self.webObject.toHex(3000000)
        try:
            transaction = self.provContract.functions.clearList().buildTransaction({
                "gasPrice": gasPriceHex,
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

