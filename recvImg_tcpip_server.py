#!/usr/bin/python
import socket
import cv2
import numpy

# socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: returen None
        buf += nuewbuf
        count -= len(newbuf)
    print(buf)
    return buf

# 수신에 사용될 server ip와 server port번호
TCP_IP = '220.69.208.241'
TCP_PORT = 8888

# tcp 소켓 열고 수신 대기
s = socekt.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
print("연결 대기 중")
conn, addr = s.accept()
print("연결 성공")

# 편의를 위해 이미지의 길이를 16으로 지정하고 데이터를 수신하는 것
# str 형의 이미지를 수신받아서 이미지로 변환하고 화면에 출력
length = recvall(conn, 16)
print(length)

stringData = recvall(conn, int(length))
print(stringData)
data = numpy.fromstring(stringData,dtype='uint8')
print(data)

s.close()
decimg = cv2.imdecode(data,1)
#decimg = data.reshape(480,640,3)
cv2.imshow('SERVER',decimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
