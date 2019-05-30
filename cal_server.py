from socket import *
import re

class cal_server:
    def run(self):
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(('', 10012))
        self.serverSock.listen(1)
        self.connectionSock, self.addr = self.serverSock.accept()
        print(f"클라이언트 접속 : {self.addr}")
        while 1:
            data = self.recieving_data()

            if data == "quit":
                break

            result = self.calc_expr(data)

            self.connectionSock.sendall(str(result).encode("UTF-8"))
            self.connectionSock.sendall(str("\n").encode("UTF-8"))
            
    def recieving_data(self):
        data = self.connectionSock.recv(1024).decode("UTF-8")
        data.replace("\r\n", "")
            
        print(f"받은 데이터 : {data}")
        return data.strip()

    def parse_expr(self, expStr):
        tokens = self.tokenize(expStr)
        OP = ("*", "/", "+", "-", "(", ")")
        P = {
            "*" : 50,
            "/" : 50,
            "+" : 40,
            "-" : 40,
            "(" : 0
        }
        output = []
        stack = []

        for item in tokens:
            if item not in OP:
                output.append(item)
            elif item == "(":
                stack.append(item)
            elif item == ")":
                while stack != [] and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack != [] and P[stack[-1]] >= P[item]:
                    output.append(stack.pop())
                stack.append(item)

        while stack:
            output.append(stack.pop())

        return output

    def calc_expr(self, expStr):
        tokens = self.parse_expr(expStr)
        OP = ("*", "/", "+", "-",)
        FUNC = {
            "*": lambda x, y: y * x,
            "/": lambda x, y: y / x,
            "+": lambda x, y: y + x,
            "-": lambda x, y: y - x,
        }
        stack = []

        for item in tokens:
            if item not in OP:
                if '.' in item:
                    stack.append(float(item))
                else:
                    stack.append(int(item))
            else:
                x = stack.pop()
                y = stack.pop()
                stack.append(FUNC[item](x, y))

        return stack.pop()

    def tokenize(self, expStr):
        RE = re.compile(r'(?:(?<=[^\d\.])(?=\d)|(?=[^\d\.]))', re.MULTILINE)
        return [x for x in re.sub(RE, " ", expStr).split(" ") if x]

    def __del__(self):
        self.serverSock.close() 

if __name__ == '__main__':
    serverObj = cal_server()
    serverObj.run()
