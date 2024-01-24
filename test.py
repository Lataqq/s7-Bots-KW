from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def ControlSum(seqRaw, depCode):
    seqStr = str(seqRaw).zfill(8)
    code = depCode + seqStr
    decoded = []
    for i in range(12):
        decoded.append(decodeWeights[i] * decodeDict[code[i]])
    return sum(decoded)%10

# Things to calculate control sum
decodeDict = {
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
    "X": 10, "A": 11, "B": 12, "C": 13, "D": 14, "E": 15, "F": 16, "G": 17, "H": 18, "I": 19,
    "J": 20, "K": 21, "L": 22, "M": 23, "N": 24, "O": 25, "P": 26, "R": 27, "S": 28, "T": 29,
    "U": 30, "W": 31, "Y": 32, "Z": 33, "0": 0
}
decodeWeights = [1 ,3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]

# Set parameters of KW
departamentCode = "KR1C"
NumKW = 1
EndNumKw = 10



for i in range(EndNumKw):
    print(NumKW)

    NumKW =+ 1

    time.sleep(10)
    









