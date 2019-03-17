from cpc.cpc import *
import time
import board
from digitalio import DigitalInOut, Direction, Pull

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.radioCS)
gdo0 = DigitalInOut(board.WAKE)
bytelength = 4
bitlength = bytelength*8
rx = CC1101(spi, cs, gdo0, 50000, 434423000, "30B6")
tx = CC1101(spi, cs, gdo0, 50000, 434423000, "30B6")
starthz = 434300000
range = 100000
step = 1000
# sweep = CC1101(spi, cs, gdo0, 50000, starthz, "0000")
# SPI object, Chip Select Pin, baudrate, frequency in Hz, Syncword

def byte(numstr):
	if len(numstr) > bitlength:
		return numstr[len(numstr)-bitlength,len(numstr)-1]
	if len(numstr) == bitlength:
		return numstr
	if numstr[0] == "0":
		return (bitlength-len(numstr))*"0" + numstr
	return (bitlength-len(numstr))*"1" + numstr

#text = open("test.txt","w")
def invert(string,index):
	if string[index] == "1":
		return "0"
	else:
		return "1"

def replace(str,index,char):
	return str[0:index] + char + str[index+1:-1]
def bitpp(bit):
	temp = bit2int(bit)
	return int2bits(temp + 1)
def twocomp(bit):
	onecomp = ""
	for i in range(0,len(bit)):
		onecomp += invert(bit,i)
	return bitpp(onecomp)
def bit2int(bit):
	neg = 1
	if bit[0] == "1":
		bit = twocomp(bit)
		neg = -1
	out = 0
	exp = 0
	for i in range(len(bit) - 1, 0, -1):
		if bit[i] == "1":
			out += int(2 ** exp)
		exp += 1
	return out*neg
def int2bits(num):
	out = ""
	for i in range(bitlength):
		if int(2**i) & num == 0:
			out = "0" + out
		else:
			out = "1" + out
	return out

# Built in LEDs
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = 0
timeout = 5000
def send(data):
	tx.setupTX()
	tx.setupCheck()
	tx.sendData(data, "30B6")
def get(obj):
	obj.setupRX()
	obj.setupCheck()
	data = obj.receiveData(bytelength,timeout)
	return data
data = byte("01")
while True:
	try:
		data = get(rx)
		data = bitpp(data)
		print("count = " + str(bit2int(data)))
	except ZeroDivisionError:
		print("Timeout, try again")
	send(data)
# Sweep frequency

# while True:
# 	for freq in range(starthz+step,starthz+range,step):
# 		try:
# 			data = get(sweep)
# 			print("count = " + str(bit2int(data)))
# 		except ZeroDivisionError:
# 			print("Timeout, try again")
#
# 		sweep.setFrequency(freq,0)