from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import pymongo
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
# contractAbi = [
# 	{
# 		"inputs": [],
# 		"name": "clearList",
# 		"outputs": [],
# 		"stateMutability": "nonpayable",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "string",
# 				"name": "eventt",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "timeStamp",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "dbName",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "clusterName",
# 				"type": "string"
# 			}
# 		],
# 		"name": "insertEntry",
# 		"outputs": [],
# 		"stateMutability": "payable",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "string",
# 				"name": "timeStamp",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "tHash",
# 				"type": "string"
# 			}
# 		],
# 		"name": "updateTransactionHash",
# 		"outputs": [],
# 		"stateMutability": "payable",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "address",
# 				"name": "userAddress",
# 				"type": "address"
# 			}
# 		],
# 		"name": "Sizee",
# 		"outputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "",
# 				"type": "uint256"
# 			}
# 		],
# 		"stateMutability": "view",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "address",
# 				"name": "",
# 				"type": "address"
# 			},
# 			{
# 				"internalType": "uint256",
# 				"name": "",
# 				"type": "uint256"
# 			}
# 		],
# 		"name": "transactionData",
# 		"outputs": [
# 			{
# 				"internalType": "string",
# 				"name": "timeStp",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "DBName",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "ClusName",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "operation",
# 				"type": "string"
# 			},
# 			{
# 				"internalType": "string",
# 				"name": "tranHash",
# 				"type": "string"
# 			}
# 		],
# 		"stateMutability": "view",
# 		"type": "function"
# 	}
# ]
# contractAbi = [
#     {
#         "inputs": [],
#         "name": "clearList",
#                 "outputs": [],
#                 "stateMutability": "nonpayable",
#                 "type": "function"
#     },
#     {
#         "inputs": [
#             {
#                 "internalType": "string",
#                 "name": "eventt",
#                                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "timeStamp",
#                                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "dbName",
#                                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "clusterName",
#                                 "type": "string"
#             }
#         ],
#         "name": "insertEntry",
#         "outputs": [],
#         "stateMutability": "payable",
#                 "type": "function"
#     },
#     {
#         "inputs": [
#             {
#                 "internalType": "string",
#                 "name": "timeStamp",
#                                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "tHash",
#                                 "type": "string"
#             }
#         ],
#         "name": "updateTransactionHash",
#         "outputs": [],
#         "stateMutability": "payable",
#                 "type": "function"
#     },
#     {
#         "inputs": [
#             {
#                 "internalType": "address",
#                 "name": "userAddress",
#                                 "type": "address"
#             }
#         ],
#         "name": "Sizee",
#         "outputs": [
#             {
#                 "internalType": "uint256",
#                 "name": "",
#                 "type": "uint256"
#             }
#         ],
#         "stateMutability": "view",
#         "type": "function"
#     },
#     {
#         "inputs": [
#             {
#                 "internalType": "address",
#                 "name": "",
#                                 "type": "address"
#             },
#             {
#                 "internalType": "uint256",
#                 "name": "",
#                                 "type": "uint256"
#             }
#         ],
#         "name": "transactionData",
#         "outputs": [
#             {
#                 "internalType": "string",
#                 "name": "timeStp",
#                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "DBName",
#                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "ClusName",
#                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "operation",
#                 "type": "string"
#             },
#             {
#                 "internalType": "string",
#                 "name": "tranHash",
#                 "type": "string"
#             }
#         ],
#         "stateMutability": "view",
#         "type": "function"
#     }
# ]
contractAbi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "dbid",
				"type": "string"
			}
		],
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
			},
			{
				"internalType": "string",
				"name": "dbid",
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
			},
			{
				"internalType": "string",
				"name": "dbid",
				"type": "string"
			}
		],
		"name": "updateTransactionHash",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "dbid",
				"type": "string"
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
				"internalType": "string",
				"name": "",
				"type": "string"
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
contractAddress = "0x855D59913DD3b699747Cc59799Dc327a34A9DCE8"
userAddress = "0xE0f5Ef3120ad5d012112eca9792a151230C8cEab"


class CustomWeb3:
    def __init__(self):
        self.webObject = Web3(Web3.HTTPProvider(
            "https://goerli.infura.io/v3/b85e8248ce5548038da1ccb22100b77a"))
        self.webObject.middleware_onion.inject(geth_poa_middleware, layer=0)
        print("Web3 is connected? : " + str(self.webObject.isConnected()))
        self.provContract = self.webObject.eth.contract(
            address=contractAddress, abi=contractAbi)

    def insertEventInSmartContract(self, data):
        try:
            dbID = str(data['DBID'])
            operationType = str(data['changeEvent']["operationType"])
            timeStamp = str(data['changeEvent']["clusterTime"]["$timestamp"]["t"])
            dbUsed = str(data['changeEvent']["ns"]["db"])
            collectionUsed = str(data['changeEvent']["ns"]["coll"])
            print(operationType)
            print(timeStamp)
            print(dbUsed)
            print(collectionUsed)
            privateKey = "60d5687eeb10f16d44d6c8c6510fd526a868ee10ff370458a31e9c6b39c28f39"
            nonce = self.webObject.eth.getTransactionCount(
                userAddress)  # SC OWNER ADDR
            gasPrice = self.webObject.eth.gasPrice
            gasPriceHex = self.webObject.toHex(gasPrice)
            # gasLimitHex = self.webObject.toHex(3000000)
            try:
                transaction = self.provContract.functions.insertEntry(operationType, timeStamp, dbUsed, collectionUsed,dbID).buildTransaction({
                    "gasPrice": gasPriceHex,
                    "from": userAddress,
                    "nonce": nonce
                })
                print("created transaction object")
                signedTxn = self.webObject.eth.account.signTransaction(
                    transaction, private_key=privateKey)
                print("signed transaction")
                transactionHash = self.webObject.eth.sendRawTransaction(
                    signedTxn.rawTransaction)
                print("sent transaction1")
                print(type(transactionHash))
                print(transactionHash)
                print(self.webObject.toHex(transactionHash))
                print(str(self.webObject.toHex(transactionHash)))
                strTransactionHash = str(self.webObject.toHex(transactionHash))
                print(type(strTransactionHash))
                # Now create new transaction to store the transaction hash
                # First get the index from the timestamp->index mapping
                tx_receipt = self.webObject.eth.waitForTransactionReceipt(
                    transactionHash, timeout=120, poll_latency=0.1)
                gas_price = self.webObject.eth.getTransaction(transactionHash).gasPrice
                gas_used = self.webObject.eth.getTransactionReceipt(transactionHash).gasUsed
                transactionCost = gas_price * gas_used
                print(transactionCost)
                self.updateHash(timeStamp, strTransactionHash,dbID,transactionCost)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    def updateHash(self, timeStamp, strTransactionHash,dbID,transactionCost):
        print(transactionCost)
        print("inside UPDATE HASH2")
        gasPrice = self.webObject.eth.gasPrice
        gasPriceHex = self.webObject.toHex(gasPrice)
        nonce2 = self.webObject.eth.getTransactionCount(
            userAddress)  # SC OWNER ADDR
        transaction2 = self.provContract.functions.updateTransactionHash(timeStamp, strTransactionHash,dbID).buildTransaction({
            "gasPrice": gasPriceHex,
            "from": userAddress,
            "nonce": nonce2
        })
        privateKey = "60d5687eeb10f16d44d6c8c6510fd526a868ee10ff370458a31e9c6b39c28f39"
        print("created transaction2 object")
        signedTxn2 = self.webObject.eth.account.signTransaction(
            transaction2, private_key=privateKey)
        print("signed transaction2")
        transactionHash2 = self.webObject.eth.sendRawTransaction(
            signedTxn2.rawTransaction)
        print("sent transaction2")
        print(self.webObject.toHex(transactionHash2))
        tx_receipt = self.webObject.eth.waitForTransactionReceipt(
            transactionHash2, timeout=120, poll_latency=0.1)
        gas_price = self.webObject.eth.getTransaction(transactionHash2).gasPrice
        gas_used = self.webObject.eth.getTransactionReceipt(transactionHash2).gasUsed
        transactionCost += gas_price * gas_used
        print("CONNECTING BACKEND MONGO")
        backendClient = pymongo.MongoClient("mongodb+srv://dbUser:test@blockchaintry.uyultsy.mongodb.net/?retryWrites=true&w=majority")
        db = backendClient.get_database('backendDB')
        print(transactionCost)
        print(dbID)
        currentEntry = db.databasesLinked.find_one_and_update({"databaseID":dbID},{"$inc":{"balance":transactionCost}})
        print(currentEntry)
        print("CURRENT ENTRY")

    def retrieveBlockChainData(self,dbID):
        finalList = []
        print(dbID)
        listLength = self.provContract.functions.Sizee(str(dbID)).call()
        print(listLength)
        urlsList = []
        for i in range(0, listLength):
            var = self.provContract.functions.transactionData(
                dbID, i).call()
            txHash = var[len(var)-1]  # Last entry is the hash
            txLink = "https://goerli.etherscan.io/tx/" + txHash
            urlsList.append(txLink)
            var.insert(0, i+1)
            print(var)
            finalList.append(var)
        print(urlsList)
        return finalList, urlsList

    def clearBlockChainData(self):
        privateKey = "60d5687eeb10f16d44d6c8c6510fd526a868ee10ff370458a31e9c6b39c28f39"
        nonce = self.webObject.eth.getTransactionCount(
            userAddress)  # SC OWNER ADDR
        gasPrice = self.webObject.eth.gasPrice
        gasPriceHex = self.webObject.toHex(gasPrice)
        # gasLimitHex = self.webObject.toHex(3000000)
        try:
            transaction = self.provContract.functions.clearList().buildTransaction({
                "gasPrice": gasPriceHex,
                "from": userAddress,
                "nonce": nonce
            })
            print("created transaction object")
            signedTxn = self.webObject.eth.account.signTransaction(
                transaction, private_key=privateKey)
            print("signed transaction")
            transactionHash = self.webObject.eth.sendRawTransaction(
                signedTxn.rawTransaction)
            print("sent transaction")
            print(self.webObject.toHex(transactionHash))
            tx_receipt = self.webObject.eth.waitForTransactionReceipt(
                transactionHash, timeout=120, poll_latency=0.1)
        except Exception as e:
            print(e)
