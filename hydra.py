import iop_python as iop
import requests
import json
import os





# ---------------------------------------MileStone 2-----------------------------------------------------
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# -------------------------------------------------------------------------------------------------------


class HydraChain:

    home_directory = os.path.expanduser("~")
    file_path = home_directory+"/.hydra_wallet"
    
    def __init__() -> None:
        pass
    
    def generate_wallet(password):
        phrase = iop.generate_phrase()
        public_key = iop.get_public_key(phrase, password)
        vault = {
            "phrase": phrase,
            "password": password,
            "public_key": public_key
        }
        vault = json.dumps(vault)
        home_directory = os.path.expanduser("~")
        f1 = os.open (home_directory+"/.hydra_wallet", os.O_CREAT, 0o777)
        os.close (f1)
        with open(home_directory+'/.hydra_wallet', 'w') as file:
            file.write(vault+"\n")
        file.close()

    @classmethod
    def generate_did(cls):
        with open(cls.file_path, 'r') as file:
            file_content = file.read()
        vault = json.loads(file_content)
        phrase, password = vault['phrase'],vault['password']
        _did = iop.generate_did_by_secp_key_id(phrase, password)
        did = iop.generate_did_by_morpheus(phrase, password)
        return(did)

    @classmethod
    def sign_witness_statements(cls,data):
        with open(cls.file_path, 'r') as file:
            file_content = file.read()
        vault = json.loads(file_content)
        phrase, password = vault['phrase'],vault['password']
        data = json.dumps(data)
        iop.sign_witness_statement(phrase, password, data)







class HydraWallet:

    def __init__(self,phrase,password):
        self.phrase = phrase
        self.password = password
   
    
    def get_wallet_address(self):
        addr = iop.get_wallet(self.phrase,self.password)
        return addr
    
    async def send_tx(phrase, receiver, amount, nonce, password):
        response = await iop.send_transaction_with_python(phrase,receiver,amount,nonce,password)
        return response
    
    def get_nonce(self):
        addr = self.get_wallet_address()
        url = f"https://test.explorer.hydraledger.io:4705/api/v2/wallets/{addr}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            nonce = int(data['data']['nonce'])
            return nonce
        else:
            print("Failed to fetch data. Status code:", response.status_code)   

    def sign_transaction(self,receiver,amount):
        nonce = self.get_nonce()
        response = iop.generate_transaction(self.phrase,receiver,amount,nonce,self.password)
        signed_txs = json.loads(response)
        return signed_txs    

    #this function assumes that the wallet has made a transaction before
    def send_transaction(self,receiver,amount):
        # Send a GET request to the URL
        signed_txs = self.sign_transaction(receiver,amount)
        url = "https://test.explorer.hydraledger.io:4705/api/v2/transactions"
        res = requests.post(url, json=signed_txs)
        response = res.json()
        return response


    def check_transaction(self,txhash):
        url = f"https://test.explorer.hydraledger.io:4705/api/v2/transactions/{txhash}"
        res = requests.get(url)
        response = res.json()
        txid = response['data']['id']
        blockId = response['data']['blockId']
        fee = response['data']['fee']
        confirmations = response['data']['confirmations']
        time = response['data']['timestamp']['human']          
        return f"Transaction with id {txid} was sent successfully at {time} with a fee of {fee} Hyd and has {confirmations} confirmations"

        
    def display_address_balance(self):
        addr = self.get_wallet_address()
        response = requests.get(f"https://test.explorer.hydraledger.io:4705/api/v2/wallets/{addr}")
        if response.status_code == 200:
            data = response.json()
            balance = data['data']['balance']
            return balance
        else:
            print("Failed to fetch data. Status code:", response.status_code)  



 

    
   






















