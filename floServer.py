import socket

host = ''
port = 65534


stored_data = "Yo, whats up?"

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete")
    return s


def setupConnection():
    s.listen(1) # Allows 1 connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def GET():
    reply = stored_data
    return reply

def REPEAT(dataMessage):
    reply = dataMessage[1]
    return reply

def dataTransfer(conn):
    # Receives the data
    while True:
        data = conn.recv(1024) # Receives the data
        data = data.decode('utf-8')
        #print(dataMessage) split the data into the command and the message
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'GET':
            reply = GET()
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)
        elif command == 'EXIT':
            print("Closing connection")
            break
        elif command == 'KILL':
            print("Closing server")
            s.close()
            break
        else:
            reply = "Unknown Command"
        # Sends the reply back to the client
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
    conn.close()
        
s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        break





        def readData():
    ser = serial.Serial(
        port = '/dev/ttyACM0',
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1)
    s = ser.readline()
    data_sensor = s.decode()			# decode s
    stored_data= str(data_sensor.rstrip())
    return stored_data