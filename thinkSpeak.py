import random
import urllib.request
import threading
import time



def thingspeak():
    #data= random.randint(10,11);
    #data = int(input())
    #print("data: ", data)
    threading.Timer(30, thingspeak).start()
    start_time = time.time()
    #val1 = 0
    #if data == 11:
    val1 = random.randint(0,10)
        
    print("val1: ",val1)
        
    val2 = random.randint(0, 10)
    print("val2: ",val2)
    URL='http://api.thingspeak.com/update?api_key='
    KEY = '7Z982VO9JNGFQCD3'
    HEADER ='&field1={}&field2={}'.format(val1,val2)
    new_URL = URL+KEY+HEADER
    v = urllib.request.urlopen(new_URL)
    print(v)
    print("--- %s seconds ---" % (time.time() - start_time))
if __name__ == '__main__':
    thingspeak()