import socket


host = '192.168.50.10' #Problems with this
port = 5560

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    command = input("Enter command: ")
    if command == 'EXIT': # Dùng break để thoát khỏi vòng lặp
        s.send(str.encode(command))
        break
    elif command == 'KILL': # Gõ KILL để thoát khỏi vòng lặp
        s.send(str.encode(command))
        break 
    s.send(str.encode(command))
    reply = s.recv(1024)
    print(reply.decode('utf-8')) # Dùng decode để hiển thị dữ liệu trả về

s.close()