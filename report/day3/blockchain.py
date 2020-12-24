from datetime import datetime
from hashlib import sha256

class Block:
    def __init__(self, data, prevhash, nonce = 0):
        # self.timestamp = datetime.now()
        self.data = data
        self.prevhash = prevhash
        self.nonce = nonce
        self.hash = self.generate_hash()
    
    # Block에 대한 정보를 출력
    def print_block(self):
        print('nonce: ', self.nonce)
        print('data: ', self.data)
        print('prevhash: ', self.prevhash)
        print('hash: ', self.hash)
        print()

    # hash를 생성하는 함수
    def generate_hash(self):
        if self.data == 'Genesis Block':
            block_contents = str(self.data) + str(self.prevhash) + str(self.nonce)
            block_hash = sha256(block_contents.encode())
            return block_hash.hexdigest()

        Flag = True
        while Flag:  
            block_contents = str(self.data) + str(self.prevhash) + str(self.nonce)
            block_hash = sha256(block_contents.encode())

            # 해쉬 값이 앞에 '0'이 5개인 경우 while문 종료 후 hash값 반환
            if block_hash.hexdigest()[0:5] == '00000':
                Flag = False
            
            # 아니라면 nonce를 1 증가시키고 다시 while문 실행해서 hash값 생성
            else:
                self.nonce += 1

        return block_hash.hexdigest()

# 객체 생성 및 할당
B1 = Block('Genesis Block', ' ', 0)
B2 = Block('2nd', B1.hash, 0)
B3 = Block('3rd', B2.hash, 0)

# 출력
B1.print_block()
B2.print_block()
B3.print_block()

