import socket
import json
import tensorflow as tf
import json
from urllib.request import urlopen
import pandas as pd
import numpy as np
from datetime import date


# 예 측

date=str(date.today().year)+str(date.today().month)+str(date.today().day)
start_date=str(int(date)-100)
key='U8U9S9MEHH8NU1X1BRBV'
nara=['0000001','0000002','0000003','0000053']   # 나라 코드(0000001:us, 0000002:jp, 0000003:eu, 0000053:cn)
url=["http://ecos.bok.or.kr/api/StatisticSearch/"+key+"/json/kr/1/100000/036Y001/DD/20180401/date/0000001/?/?/"]

s_data=pd.DataFrame()
time=[]
us=[]
jp=[]
eu=[]
cn=[]

for i in range(len(nara)):
    data=json.loads(urlopen(url[0][:-12]+nara[i]+url[0][-5:]).read())
    data2=data['StatisticSearch']['row']
    for k in range(len(data2)):
        if nara[i]==nara[0]:
            us.append(float(data2[k]['DATA_VALUE']))
            time.append(int(data2[k]['TIME']))
        elif nara[i]==nara[1]:
            jp.append(float(data2[k]['DATA_VALUE']))
        elif nara[i]==nara[2]:
            eu.append(float(data2[k]['DATA_VALUE']))
        else :
            cn.append(float(data2[k]['DATA_VALUE']))

s_data['time']=time
s_data['us']=us
s_data['jp']=jp
s_data['eu']=eu
s_data['cn']=cn
s_data['time']=pd.to_datetime(s_data.time.apply(lambda x: str(x)))
print(s_data)


model=tf.keras.models.load_model('C:/Users/icear/usd_model.h5')
model2=tf.keras.models.load_model('C:/Users/icear/jpy_model.h5')
model3=tf.keras.models.load_model('C:/Users/icear/cny_model.h5')

from sklearn.preprocessing import MinMaxScaler

# usd

lstm_predictions_scaled = list()

scaler = MinMaxScaler()
scaler.fit(s_data[['us']])
scaled_train_data = scaler.transform(s_data[['us']])

n_input = 1
n_features= 1

batch = scaled_train_data[-n_input:]
current_batch = batch.reshape((1, n_input, n_features))

for i in range(365):
    lstm_pred = model.predict(current_batch)[0]
    lstm_predictions_scaled.append(lstm_pred)
    current_batch = np.append(current_batch[:,1:,:],[[lstm_pred]],axis=1)

lstm_predictions = scaler.inverse_transform(lstm_predictions_scaled)
usd=pd.DataFrame(lstm_predictions)



# jpy

lstm_predictions_scaled = list()

scaler = MinMaxScaler()
scaler.fit(s_data[['jp']])
scaled_train_data = scaler.transform(s_data[['jp']])

n_input = 1
n_features= 1

batch = scaled_train_data[-n_input:]
current_batch = batch.reshape((1, n_input, n_features))

for i in range(365):
    lstm_pred = model2.predict(current_batch)[0]
    lstm_predictions_scaled.append(lstm_pred)
    current_batch = np.append(current_batch[:,1:,:],[[lstm_pred]],axis=1)

lstm_predictions = scaler.inverse_transform(lstm_predictions_scaled)
jpy=pd.DataFrame(lstm_predictions)


# cny

lstm_predictions_scaled = list()

scaler = MinMaxScaler()
scaler.fit(s_data[['cn']])
scaled_train_data = scaler.transform(s_data[['cn']])

n_input = 1
n_features= 1

batch = scaled_train_data[-n_input:]
current_batch = batch.reshape((1, n_input, n_features))

for i in range(365):
    lstm_pred = model3.predict(current_batch)[0]
    lstm_predictions_scaled.append(lstm_pred)
    current_batch = np.append(current_batch[:,1:,:],[[lstm_pred]],axis=1)

lstm_predictions = scaler.inverse_transform(lstm_predictions_scaled)
cny=pd.DataFrame(lstm_predictions)






# json 함수

def to_json(nation, jugi):
    pre_usd = dict()
    pre_jpy = dict()
    pre_cny = dict()
    if jugi == '일주일':
        if nation == 'usd':
            for i in range(0, 5):
                pre_usd['H{}'.format(i + 1)] = usd[0][i]
                json_usd = json.dumps(pre_usd, separators=(';', ':'))
            return json_usd

        elif nation == 'jpy':
            for i in range(0, 5):
                pre_jpy['H{}'.format(i + 1)] = jpy[0][i]
                json_jpy = json.dumps(pre_jpy, separators=(';', ':'))
            return json_jpy

        elif nation == 'cny':
            for i in range(0, 5):
                pre_cny['H{}'.format(i + 1)] = cny[0][i]
                json_cny = json.dumps(pre_cny, separators=(';', ':'))
            return json_cny

    if jugi == '한달':
        if nation == 'usd':
            for i in range(0, 31):
                pre_usd['H{}'.format(i + 1)] = usd[0][i]
                json_usd = json.dumps(pre_usd, separators=(';', ':'))
            return json_usd

        elif nation == 'jpy':
            for i in range(0, 31):
                pre_jpy['H{}'.format(i + 1)] = jpy[0][i]
                json_jpy = json.dumps(pre_jpy, separators=(';', ':'))
            return json_jpy

        elif nation == 'cny':
            for i in range(0, 31):
                pre_cny['H{}'.format(i + 1)] = cny[0][i]
                json_cny = json.dumps(pre_cny, separators=(';', ':'))
            return json_cny

    if jugi == '일년':
        if nation == 'usd':
            for i in range(0, 365):
                pre_usd['H{}'.format(i + 1)] = usd[0][i]
                json_usd = json.dumps(pre_usd, separators=(';', ':'))
            return json_usd

        elif nation == 'jpy':
            for i in range(0, 365):
                pre_jpy['H{}'.format(i + 1)] = jpy[0][i]
                json_jpy = json.dumps(pre_jpy, separators=(';', ':'))
            return json_jpy

        elif nation == 'cny':
            for i in range(0, 365):
                pre_cny['H{}'.format(i + 1)] = cny[0][i]
                json_cny = json.dumps(pre_cny, separators=(';', ':'))
            return json_cny






# socket


# 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다.
HOST = '127.0.0.1'

# 클라이언트 접속을 대기하는 포트 번호입니다.
PORT = 9999



# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 포트 사용중이라 연결할 수 없다는
# WinError 10048 에러 해결를 위해 필요합니다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
server_socket.bind((HOST, PORT))

# 서버가 클라이언트의 접속을 허용하도록 합니다.
server_socket.listen()

# accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
client_socket, addr = server_socket.accept()

# 접속한 클라이언트의 주소입니다.
print('Connected by', addr)



# 무한루프를 돌면서
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다.
    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다.
    if not data:
        break


    # 수신받은 문자열을 출력합니다.
    print('Received from', addr, data.decode())
    json_data = json.loads(data)
    print(json_data)
    receve_data=to_json(json_data['nation'],json_data['jugi'])



    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코)
    client_socket.sendall(data)


# 소켓을 닫습니다.
client_socket.close()
server_socket.close()