from bip_utils import (
    Bip39SeedGenerator, Bip84, Bip84Coins, 
    Bip39WordsNum, Bip39EntropyGenerator, Bip39MnemonicGenerator, Bip44Changes
)
import os

WALLET_FILE = "wallet.txt"
INFOBASE_FILE = "infobase.txt"

def generate_mnemonic():
    entropy_bytes = Bip39EntropyGenerator(256).Generate()
    return Bip39MnemonicGenerator().FromEntropy(entropy_bytes)

def generate_wallet(mnemonic):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip84_mst_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    bip84_acc_ctx = bip84_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    return {
        "mnemonic": mnemonic,
        "address": bip84_acc_ctx.PublicKey().ToAddress(),
        "private_key": bip84_acc_ctx.PrivateKey().Raw().ToHex(),
        "public_key": bip84_acc_ctx.PublicKey().RawCompressed().ToHex()
    }

def wallet_exists(address):
    if not os.path.exists(WALLET_FILE):
        return False
    with open(WALLET_FILE, "r") as f:
        for line in f:
            if address in line.split():
                return True
    return False

def get_wallet_info(address):
    if not os.path.exists(WALLET_FILE):
        return None
    with open(WALLET_FILE, "r") as f:
        for line in f:
            if address in line.split():
                return line.strip()
    return None

def save_to_infobase(info):
    with open(INFOBASE_FILE, "a") as f:
        f.write(info + "\n")

def main():
    num_wallets = int(input("Введите количество кошельков для генерации: "))
    
    for i in range(num_wallets):
        mnemonic = generate_mnemonic()
        wallet = generate_wallet(mnemonic)
        
        address = wallet["address"]
        
        if wallet_exists(address):
            print(f"Кошелек с адресом {address} уже существует. Пропуск.")
            wallet_info = get_wallet_info(address)
            if wallet_info:
                save_to_infobase(wallet_info)
        else:
            print(f"Кошелек {i+1}:")
            print(f"Мнемоническая фраза: {wallet['mnemonic']}")
            print(f"Приватный ключ: {wallet['private_key']}")
            print(f"Публичный ключ: {wallet['public_key']}")
            print(f"Биткоин-адрес: {wallet['address']}")
            print("-" * 30)

if __name__ == "__main__":
    main()

