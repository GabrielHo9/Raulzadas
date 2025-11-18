# Importa o módulo socket
from socket import *
import sys  # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverPort = 6789  # Escolha a porta que deseja usar
serverSocket.bind(('0.0.0.0', serverPort))  # Bind do socket ao endereço e porta
serverSocket.listen(1)  # Escuta apenas uma conexão por vez

print(f"Servidor web rodando na porta {serverPort}...")
print('Prontinho')
while True:
    # Estabelece a conexão
    
    connectionSocket, addr = serverSocket.accept()  # Aceita conexão do cliente
    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()  # Recebe até 1024 bytes
        filename = message.split()[1]  # Extrai o nome do arquivo requisitado

        # Abre o arquivo requisitado
        f = open(filename[1:])  # Remove a barra inicial "/"
        outputdata = f.read()
        f.close()

        # Envia a linha de status do cabeçalho HTTP
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        print(f"200 OK")
        # Envia o conteúdo do arquivo ao cliente
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Fecha a conexão com o cliente
        connectionSocket.close()

    except IOError:
        # Envia mensagem de erro 404 se o arquivo não for encontrado
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        print(f"404 Not Found({filename})\n")
        # Fecha o socket do cliente
        connectionSocket.close()

# Fecha o socket do servidor (nunca será alcançado neste loop infinito)
serverSocket.close()
sys.exit()  # Encerra o programa
