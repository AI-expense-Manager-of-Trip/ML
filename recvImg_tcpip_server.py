#!/usr/bin/python
import socket
import cv2
import numpy

# socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock):
    buf = b''
    flag = True
    while flag:
        newbuf = sock.recv(count)
        if not newbuf:
            flag = False
            continue

        buf += newbuf

    return buf

# 수신에 사용될 server ip와 server port번호
TCP_IP = '192.168.0.0'
TCP_PORT = 8888

# tcp 소켓 열고 수신 대기
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
print("연결 대기 중")
conn, addr = s.accept()
print("연결 성공")

# str 형의 이미지를 수신받아서 이미지로 변환하고 화면에 출력
recvbytes = recvall(conn)
print(len(recvbytes))

nparr = numpy.fromstring(recvbytes, numpy.uint8)

#for _ in nparr:
#    print(_,end=' ')

s.close()

decimg = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

cv2.imshow('SERVER',decimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
