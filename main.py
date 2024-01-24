from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
import io

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
trAndIndex = [[[8, 2], [7, 3]], [[23, 4], [22, 5]], [[38, 6], [37, 7]], [[53, 8], [52, 9]], [[68, 10], [67, 11]], [[83, 12], [82, 13]], [[98, 14], [97, 15]], [[113, 16], [112, 17]], [[128, 18], [127, 19]], [[143, 20], [142, 21]]]

# Set parameters of KW
departamentCode = "KR1C"
NumKW = 3000
amountOfKw = 10

# Database
conn = sqlite3.connect('D:\GIT\s7-Bots\KW\dbKW.db')
c = conn.cursor()

for i in range(amountOfKw):
    print(NumKW)
    tstart = time.perf_counter()
    services = Service(executable_path="D:\GIT\s7-Bots\KW\chromedriver.exe")
    driver = webdriver.Chrome(service=services)
    driver.get("https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW?komunikaty=true&kontakt=true&okienkoSerwisowe=false")
    WebDriverWait(driver, 360).until(
        EC.presence_of_element_located((By.ID, "msLogo"))
    )
    numControlSum = ControlSum(NumKW, departamentCode)
    driver.find_element(By.ID, "kodWydzialuInput").send_keys(departamentCode)
    driver.find_element(By.ID, "numerKsiegiWieczystej").send_keys(NumKW)
    driver.find_element(By.ID, "cyfraKontrolna").send_keys(numControlSum)
    driver.find_element(By.ID, "wyszukaj").click()
    
    WebDriverWait(driver, 360).until(
        EC.presence_of_element_located((By.ID, "msLogo"))
    )
    isPresent = bool(driver.find_elements(By.ID, "przyciskWydrukDotychczasowy"))
    if isPresent:
        record = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        kw = departamentCode + "/" + str(NumKW).zfill(8) + "/" + str(numControlSum)
        record[0] = kw
        driver.find_element(By.ID, "przyciskWydrukDotychczasowy").click()
        driver.find_element(By.XPATH, "/html/body/table[1]/tbody/tr/td[2]/form/input[7]").click()
        isPresent = bool(driver.find_elements(By.XPATH, "/html/body/div/table[4]/tbody/tr[9]/td[3]"))
        if isPresent:
            city = driver.find_element(By.XPATH, "/html/body/div/table[4]/tbody/tr[9]/td[3]").text
            record[1] = city

            for j in range(10):
                trNr = trAndIndex[j][0][0]
                xpath = f"/html/body/div/table[5]/tbody/tr[{trNr}]/td[3]"
                isPresent = bool(driver.find_elements(By.XPATH, xpath))
                if isPresent:
                    ParcelNr = driver.find_element(By.XPATH, xpath).text
                    record[trAndIndex[j][0][1]] = ParcelNr

                trNr = trAndIndex[j][1][0]
                xpath = f"/html/body/div/table[5]/tbody/tr[{trNr}]/td[4]/a"
                isPresent = bool(driver.find_elements(By.XPATH, xpath))
                if isPresent:
                    ParcelID = driver.find_element(By.XPATH, xpath).text
                    record[trAndIndex[j][1][1]] = ParcelID

            print(record)
            c.execute("INSERT INTO KsiegiWieczyste VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11],
                        record[12], record[13], record[14], record[15], record[16], record[17], record[18], record[19], record[20], record[21]))
            conn.commit()

    NumKW += 1
    driver.close()
    tstop = time.perf_counter()
    print(tstop - tstart)


    







