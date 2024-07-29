from Crypto.Util import number
import PySimpleGUI as sg
import random
from workWithInput import wwi
from BBS import bbs

#------------------------------------------------------------------------------
# вспомогательные таблицы
Sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]

InvSbox = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]

Rcon = [
        [0x00, 0x00, 0x00, 0x00],
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1b, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00]
    ]

#------------------------------------------------------------------------------
# смена формата полученного ответа
def changeEnc(text):
    
    res = ""
    
    for i in range(len(text)):
        
        a = bin(text[i])[2:]
        
        while (len(a)<8):
            a = '0' + a
        
        res = res + a
    
    return(res)

#------------------------------------------------------------------------------
# получаем массив State из input
def getState(M, Nb):
    
    state = [[""] * Nb for i in range(4)]
    
    for r in range(4):
        for c in range(Nb):
            state[r][c] = int(M[r+4*c], 2)
    
    return state

#------------------------------------------------------------------------------
# получаем массив output из state
def getOutput(M, Nb):
    
    output = ["" for i in range(4*Nb)]
    
    for r in range(4):
        for c in range(Nb):
            output[r+4*c] = M[r][c]
    
    return output


#------------------------------------------------------------------------------
# замена байтов в столбце wi на элементы таблицы Sbox
def SubWord(wi):
    
    for i in range(4):
            wi[i] = Sbox[wi[i]]

#------------------------------------------------------------------------------
# циклический сдвиг столбца на один элемент
def RotWord(wi):
    
    b = wi[0]
    for i in range(3):
            wi[i] = wi[i+1]
    wi[3] = b

#------------------------------------------------------------------------------
# алгоритм генерации раундовых ключей из исходного ключа
def KeyExpansion(key, Nb, Nr, Nk):
    
    KeySchedule = [[""] * Nb*(Nr + 1) for i in range(4)]

    # первые четыре столбца заполняем значением исходного ключа
    for r in range(4):
        for c in range(Nk):
            KeySchedule[r][c] = int(key[r+4*c], 2)
    
    i = Nk
    
    while i < Nb * (Nr+1):
        
        # берём очередной столбец, с которым будем работать
        temp = []
        for j in range(4):
            temp.append(KeySchedule[j][i-1])
        
        # если добавляемый столбец кратен 4
        if i % Nk == 0:
            
            RotWord(temp)
            SubWord(temp)
            
            for j in range(4):
                temp[j] = temp[j]^Rcon[i//Nk][j]
        else:
            if Nk > 6 and i % Nk == 4:
                temp = SubWord(temp)
                
        for j in range(4):
            KeySchedule[j][i] = temp[j] ^ KeySchedule[j][i-Nk]
        
        i = i+1
    
    return KeySchedule
    
    
#------------------------------------------------------------------------------
# добавление к матрице состояния раундового ключа с помощью XOR
def AddRoundKey(state, w, Nb):
    
    for r in range(4):
        for c in range(Nb):
            state[r][c] = state[r][c]^w[r][c]
    
#------------------------------------------------------------------------------
# замена байтов state на элементы таблицы Sbox
def SubBytes(state, Nb):
    
    for r in range(4):
        for c in range(Nb):
            state[r][c] = Sbox[state[r][c]]

#------------------------------------------------------------------------------
# замена байтов state на элементы таблицы InvSbox
def InvSubBytes(state, Nb):
    
    for r in range(4):
        for c in range(Nb):
            state[r][c] = InvSbox[state[r][c]]
        

#------------------------------------------------------------------------------
# циклический сдвиг строк влево
def ShiftRows(state, Nb):
    
    for r in range(4):
        for i in range(r):
            b = state[r][0]
            for c in range(Nb-1):
                state[r][c] = state[r][c+1]
            state[r][Nb-1] = b
    
#------------------------------------------------------------------------------
# циклический сдвиг строк вправо
def InvShiftRows(state, Nb):
    
    for r in range(4):
        for i in range(r):
            b = state[r][Nb-1]
            for c in range(Nb-1,0,-1):
                state[r][c] = state[r][c-1]
            state[r][0] = b


#------------------------------------------------------------------------------
# умножение в поле Галуа на полином {02}
def GF02(b):
    
    if b < 0x80:
        res =  (b << 1)
    else:
        res =  (b << 1)^0x1b

    return res % 0x100

#------------------------------------------------------------------------------
# умножение в поле Галуа на полином {03}
def GF03(b):
    return b^GF02(b)

#------------------------------------------------------------------------------
# умножение в поле Галуа на полином {09}
def GF09(b):
    return GF02(GF02(GF02(b)))^b

#------------------------------------------------------------------------------
# умножение в поле Галуа на полином {0b}
def GF0b(b):
    return GF02(GF02(GF02(b)))^GF02(b)^b

#------------------------------------------------------------------------------
# умножение в поле Галуа на полином {0d}
def GF0d(b):
    return GF02(GF02(GF02(b)))^GF02(GF02(b))^b

#------------------------------------------------------------------------------
# умножение в поле Галуа на полином {0e}
def GF0e(b):
    return GF02(GF02(GF02(b)))^GF02(GF02(b))^GF02(b)

#------------------------------------------------------------------------------
# умножение столбцов в поле Галуа (шифрование)
def MixColumns(state, Nb):
    
    
    for i in range(Nb):
        
        s0 = GF02(state[0][i])^GF03(state[1][i])^state[2][i]^state[3][i]
        s1 = state[0][i]^GF02(state[1][i])^GF03(state[2][i])^state[3][i]
        s2 = state[0][i]^state[1][i]^GF02(state[2][i])^GF03(state[3][i])
        s3 = GF03(state[0][i])^state[1][i]^state[2][i]^GF02(state[3][i])

        state[0][i] = s0
        state[1][i] = s1
        state[2][i] = s2
        state[3][i] = s3


#------------------------------------------------------------------------------
# умножение столбцов в поле Галуа (дешифрование)
def InvMixColumns(state, Nb):
    
    for i in range(Nb):

        
        s0 = GF0e(state[0][i])^GF0b(state[1][i])^GF0d(state[2][i])^GF09(state[3][i])
        s1 = GF09(state[0][i])^GF0e(state[1][i])^GF0b(state[2][i])^GF0d(state[3][i])
        s2 = GF0d(state[0][i])^GF09(state[1][i])^GF0e(state[2][i])^GF0b(state[3][i])
        s3 = GF0b(state[0][i])^GF0d(state[1][i])^GF09(state[2][i])^GF0e(state[3][i])

        state[0][i] = s0
        state[1][i] = s1
        state[2][i] = s2
        state[3][i] = s3


#------------------------------------------------------------------------------
# разбиваем раундовые ключи на блоки
def getKeyBlock(keys, Nr, Nb):
    
    w = [[[1] * Nb for i in range(4)] for i in range (Nr+1)]
    
    for i in range(Nr+1):
        for r in range(4):
            for c in range(Nb):
                w[i][r][c] = keys[r][c+Nb*i]
    
    return w   


#------------------------------------------------------------------------------
# алгоритм AES    
def encryptAES(text, key, Nb, Nr, Nk):
    
    state = getState(text, Nb)
    
    w = getKeyBlock(KeyExpansion(key, Nb, Nr, Nk),Nr,Nb)
    
    AddRoundKey(state, w[0], Nb)
    
    for i in range(1,Nr):
        SubBytes(state, Nb)
        ShiftRows(state, Nb)
        MixColumns(state, Nb)
        AddRoundKey(state, w[i], Nb)
    
    SubBytes(state, Nb)
    ShiftRows(state, Nb)
    AddRoundKey(state, w[Nr], Nb)
    
    output = getOutput(state, Nb)
    return changeEnc(output)

#------------------------------------------------------------------------------
# алгоритм AES    
def decryptAES(text, key, Nb, Nr, Nk):
    
    
    state = getState(text, Nb)
    w = getKeyBlock(KeyExpansion(key, Nb, Nr, Nk),Nr,Nb)
    
    AddRoundKey(state, w[Nr], Nb)
    
    for i in range(Nr-1,0,-1):
        InvShiftRows(state, Nb)
        InvSubBytes(state, Nb)
        AddRoundKey(state, w[i], Nb)
        InvMixColumns(state, Nb)
    
    InvShiftRows(state, Nb)
    InvSubBytes(state, Nb)
    AddRoundKey(state, w[0], Nb)

    output = getOutput(state, Nb)
    
    return changeEnc(output)

# -----------------------------------------------------------------------------
# интерфейс
def main():
    
    sg.theme('DefaultNoMoreNagging')


    one = [
                    [sg.Text('________________________________________________________________________________________________________________')],
                    [sg.Text('Сообщение (M)'), sg.Button('Сгенерировать', key ='ok6')],
                    [sg.Text('Формат сообщения'), sg.Radio("2-ичный", "type2", key='2M', default=True), sg.Radio("16-ричный", "type2", key='16M'), sg.Radio("символьный", "type2", key='symbolM')],
                    [sg.Multiline(size=(110, 5), key="M")],
                    [sg.Text('Ключ (Key) '), sg.Button('Сгенерировать', key ='ok1')],
                    [sg.Text('Формат ключа'), sg.Radio("2-ичный", "type1", key='2K', default=True), sg.Radio("16-ричный", "type1", key='16K'), sg.Radio("символьный", "type1", key='symbolK')],
                    [sg.Multiline(size=(110, 5), key="Key")],
                    [sg.Text('Результат шифрования'), sg.Button('Получить', key ='ok2')],
                    [sg.Text('Формат шифротекста'), sg.Radio("2-ичный", "type9", key='2C3', default=True), sg.Radio("16-ричный", "type9", key='16C3'), sg.Radio("символьный", "type9", key='symbolC3')],
                    [sg.Output(size=(110, 5),key='result1')],
                    [sg.Text('________________________________________________________________________________________________________________')]
                ]
    
    two = [
                    [sg.Text('________________________________________________________________________________________________________________')],
                    [sg.Text('Зашифрованный текст (C)'), sg.Button('Сгенерировать', key ='ok7')],
                    [sg.Text('Формат сообщения'), sg.Radio("2-ичный", "type3", key='2C', default=True), sg.Radio("16-ричный", "type3", key='16C'), sg.Radio("символьный", "type3", key='symbolC')],
                    [sg.Multiline(size=(110, 5), key="C")],
                    [sg.Text('Ключ (Key) '), sg.Button('Сгенерировать', key ='ok3')],
                    [sg.Text('Формат ключа'), sg.Radio("2-ичный", "type", key='2', default=True), sg.Radio("16-ричный", "type", key='16'), sg.Radio("символьный", "type", key='symbol')],
                    [sg.Multiline(size=(110, 5), key="Key2")],
                    [sg.Text('Результат дешифрования'), sg.Button('Получить', key ='ok4')],
                    [sg.Text('Формат расшифрованного текста:'), sg.Radio("2-ичный", "type10", key='2C4', default=True), sg.Radio("16-ричный", "type10", key='16C4'), sg.Radio("символьный", "type10", key='symbolC4')],
                    [sg.Output(size=(110, 5),key='result2')],
                    [sg.Text('________________________________________________________________________________________________________________')]
                ]
    
    three = [
                    [sg.Text('________________________________________________________________________________________________________________')],
                    [sg.Text('Исходный текст')],
                    [sg.Text('Формат текста'), sg.Radio("2-ичный", "type6", key='2C1', default=True), sg.Radio("16-ричный", "type6", key='16C1'), sg.Radio("символьный", "type6", key='symbolC1')],
                    [sg.Multiline(size=(110, 5), key="text")],
                    [sg.Text('Текст в другом формате'), sg.Button('Сгенерировать', key ='ok5')],
                    [sg.Text('Перевод в:'), sg.Radio("2-ичный", "type7", key='2C2', default=True), sg.Radio("16-ричный", "type7", key='16C2'), sg.Radio("символьный", "type7", key='symbolC2')],
                    [sg.Output(size=(110, 5),key='result3')],
                    [sg.Text('________________________________________________________________________________________________________________')]
                ]
    
    tab_group_layout = [[sg.TabGroup([[sg.Tab('Шифрование', one, key='-TAB1-'), sg.Tab('Дешифрование', two, key='-TAB2-'),sg.Tab('Изменение формата', three, key='-TAB3-')]])]]
    
    window = sg.Window('Лабораторная 3', tab_group_layout)
    
    
    while True:
        
        event, values = window.read()
        
        if event in (None, 'Exit'):
            break
     
# -----------------------------------------------------------------------------
        # генерация ключа (шифрование)
        elif  event == 'ok1':
            
            key = "" # значение ключа
            fKey = 0 # формат ключа
            
            if values['2K'] == True:
                fKey = 1 # 2-ичное представление
            elif values['16K'] == True:
                fKey = 2 # 16-ричное представление
            elif values['symbolK'] == True:
                fKey = 3 # символьное представление
            
            key = wI.newRepresent(bbs.BBS(128))
                
            # переводим ключ в нужный формат
            if fKey == 2:
                key = wI.from2To16(key)
            elif fKey == 3:
                key = wI.from2ToSymbol(key)
                        
            if fKey == 1 or fKey == 2:
                window['Key'].update(' '.join(key))
            else:
                window['Key'].update(key)

# -----------------------------------------------------------------------------
        # шифрование
        elif event == 'ok2':
            
            M = values['M'] # текст шифруемого сообщения
            C = "" # результат шифрования
            key = values['Key'] # значение ключа
            lenM = 0 # длина сообщения
            fM = 0 # формат сообщения
            fKey = 0 # формат ключа
            fC = 0 # формат шифротекста
            textError = "" # текст ошибки
            flag = True # вспомогательная переменная
                
            if values['2M'] == True:
                fM = 1 # 2-ичное представление
            elif values['16M'] == True:
                fM = 2 # 16-ричное представление
            elif values['symbolM'] == True:
                fM = 3 # символьное представление
                
            if values['2K'] == True:
                fKey = 1 # 2-ичное представление
            elif values['16K'] == True:
                fKey = 2 # 16-ричное представление
            elif values['symbolK'] == True:
                fKey = 3 # символьное представление
            
            if values['2C3'] == True:
                fC = 1 # 2-ичное представление
            elif values['16C3'] == True:
                fC = 2 # 16-ричное представление
            elif values['symbolC3'] == True:
                fC = 3 # символьное представление
            
            
            
            # ----------------------------------- проверка шифруемого сообщения
            if M == "":
                sg.popup_ok("Сначала введите сообщение, которое необходимо зашифровать")
            else:
                # проверяем, в нужном ли формате задано сообщение
                if fM == 1:
                    flag, textError = wI.check2(M)
                elif fM == 2:
                    flag, textError = wI.check16(M)
                elif fM ==3:
                    flag, textError = wI.checkSymbol(M)
                
                if flag == False:
                    sg.popup_ok(textError)
                else:
                    
                    Mnew = [] # сообщение, разбитое на символы (необходимо, если формат не символьный)
                    
                    # определяем длину сообщения
                    if fM != 3:
                        Mnew = M.split()
                        lenM = len(Mnew)
                    else:
                        Mnew = M
                        lenM = len(M)
                    
                    # текст должен разбиваться на блоки по 128 битов
                    if lenM % 16 != 0:
                        sg.popup_ok("Количество символов должно быть кратно 16 (у вас " + str(lenM) + ")")
                    else:
                    
                        # ------------------------------------------ проверка ключа
                        if key == "":
                            sg.popup_ok("Введите или сгенирируйте ключ")
                        else:
                            
                            # проверяем, в нужном ли формате задан ключ
                            if fKey == 1:
                                flag, textError = wI.check2(key)
                                textError = textError + " (речь о ключе)"
                            elif fKey == 2:
                                flag, textError = wI.check16(key)
                                textError = textError + " (речь о ключе)"
                            
                            if flag == False:
                                sg.popup_ok(textError)
                                
                            else:
                                
                                keyNew = []
                                
                                # определяем длину ключа
                                if fKey != 3:
                                    keyNew = key.split()
                                    lenKey = len(keyNew)
                                else:
                                    keyNew = key
                                    lenKey = len(key)
                                
                                
                                # проверяем длину ключа
                                if lenKey != 16:
                                    
                                    sg.popup_ok("Длина ключа должна быть 16 байт")
                                
                                else:
                                    
                                    # ----------------------- генерируем шифротекст
                                    
                                    # изменяем тип шифруемого сообщения
                                    if fM == 2:
                                        Mnew = wI.from16To2(Mnew)
                                    elif fM == 3:
                                        Mnew = wI.fromSymbolTo2(Mnew)
                                    
                                    # изменяем тип ключа
                                    if fKey == 2:
                                        keyNew = wI.from16To2(keyNew)
                                    elif fKey  == 3:
                                        keyNew = wI.fromSymbolTo2(keyNew)
                                    
                                    # вычисляем шифротекст
                                    C = []
                                    for i in range(int(lenM/16)):
                                        C = C + wI.newRepresent(encryptAES(Mnew[i*16:(i+1)*16], keyNew, Nb, Nr, Nk))
                                    
                                    if fC == 2:
                                        window['result1'].update(' '.join(wI.from2To16(C)))
                                    elif fC == 3:
                                        window['result1'].update(wI.from2ToSymbol(C))
                                    else:
                                        window['result1'].update(' '.join(C))
                                
                                    
                               
# -----------------------------------------------------------------------------
        # генерация ключа (дешифрование)
        elif  event == 'ok3':
            
            key = "" # значение ключа
            fKey = 0 # формат ключа
            
            if values['2'] == True:
                fKey = 1 # 2-ичное представление
            elif values['16'] == True:
                fKey = 2 # 16-ричное представление
            elif values['symbol'] == True:
                fKey = 3 # символьное представление
            
            key = wI.newRepresent(bbs.BBS(128))
                
            # переводим ключ в нужный формат
            if fKey == 2:
                key = wI.from2To16(key)
            elif fKey == 3:
                key = wI.from2ToSymbol(key)
                        
            if fKey == 1 or fKey == 2:
                window['Key2'].update(' '.join(key))
            else:
                window['Key2'].update(key)

                               
# -----------------------------------------------------------------------------
        # дешифрование
        elif event == 'ok4':
            
            C = values['C'] # дешифруемое сообщение
            M = "" # результат шифрования
            key = values['Key2'] # значение ключа
            lenC = 0 # длина сообщения
            fM = 0 # формат сообщения
            fKey = 0 # формат ключа
            fC = 0 # формат шифротекста
            textError = "" # текст ошибки
            flag = True # вспомогательная переменная
                
            if values['2C4'] == True:
                fM = 1 # 2-ичное представление
            elif values['16C4'] == True:
                fM = 2 # 16-ричное представление
            elif values['symbolC4'] == True:
                fM = 3 # символьное представление
                
            if values['2'] == True:
                fKey = 1 # 2-ичное представление
            elif values['16'] == True:
                fKey = 2 # 16-ричное представление
            elif values['symbol'] == True:
                fKey = 3 # символьное представление
            
            if values['2C'] == True:
                fC = 1 # 2-ичное представление
            elif values['16C'] == True:
                fC = 2 # 16-ричное представление
            elif values['symbolC'] == True:
                fC = 3 # символьное представление
            
            
            
            # ----------------------------------- проверка шифруемого сообщения
            if C == "":
                sg.popup_ok("Сначала введите сообщение, которое необходимо дешифровать")
            else:
                # проверяем, в нужном ли формате задано сообщение
                if fC == 1:
                    flag, textError = wI.check2(C)
                elif fC == 2:
                    flag, textError = wI.check16(C)
                elif fC ==3:
                    flag, textError = wI.checkSymbol(C)
                
                if flag == False:
                    sg.popup_ok(textError)
                else:
                    
                    Cnew = [] # сообщение, разбитое на символы (необходимо, если формат не символьный)
                    
                    # определяем длину сообщения
                    if fC != 3:
                        Cnew = C.split()
                        lenC = len(Cnew)
                    else:
                        Cnew = C
                        lenC = len(C)
                    
                    # текст должен разбиваться на блоки по 64 бита
                    if lenC % 16 != 0:
                        sg.popup_ok("Количество символов шифротекста должно быть кратно 8 (у вас " + str(lenC) + ")")
                    else:
                    
                        # ------------------------------------------ проверка ключа
                        if key == "":
                            sg.popup_ok("Введите или сгенирируйте ключ")
                        else:
                            
                            # проверяем, в нужном ли формате задан ключ
                            if fKey == 1:
                                flag, textError = wI.check2(key)
                                textError = textError + " (речь о ключе)"
                            elif fKey == 2:
                                flag, textError = wI.check16(key)
                                textError = textError + " (речь о ключе)"
                            
                            if flag == False:
                                sg.popup_ok(textError)
                                
                            else:
                                
                                keyNew = []
                                
                                # определяем длину ключа
                                if fKey != 3:
                                    keyNew = key.split()
                                    lenKey = len(keyNew)
                                else:
                                    keyNew = key
                                    lenKey = len(key)
                                
                                
                                # проверяем длину ключа
                                if lenKey != 16:
                                    sg.popup_ok("Длина ключа должна быть 16 байт")
                                else:
                                    
                                    # ----------------------- генерируем шифротекст
                                    
                                    # изменяем тип шифруемого сообщения
                                    if fC == 2:
                                        Cnew = wI.from16To2(Cnew)
                                    elif fC == 3:
                                        Cnew = wI.fromSymbolTo2(Cnew)
                                    
                                    # изменяем тип ключа
                                    if fKey == 2:
                                        keyNew = wI.from16To2(keyNew)
                                    elif fKey  == 3:
                                        keyNew = wI.fromSymbolTo2(keyNew)
                                    
                                    # вычисляем шифротекст
                                    M = []
                                    for i in range(int(lenM/16)):
                                        M = M + wI.newRepresent(decryptAES(Cnew[i*16:(i+1)*16], keyNew, Nb, Nr, Nk))
                                    
                                    if fM == 2:
                                        window['result2'].update(' '.join(wI.from2To16(M)))
                                    elif fM == 3:
                                        window['result2'].update(wI.from2ToSymbol(M))
                                    else:
                                        window['result2'].update(' '.join(M))
                                
                                
# -----------------------------------------------------------------------------
        # смена формата
        elif event == 'ok5':
            
            M = values['text'] # текст, для которого меняем формат
            fM = 0 # формат изменяемого текста
            resText = "" # текст с изменённым форматом
            fT = 0 # желаемый формат
            flag = True # вспомогательная переменная
            
            
            
            if values['2C1'] == True:
                fM = 1 # 2-ичное представление
            elif values['16C1'] == True:
                fM = 2 # 16-ричное представление
            elif values['symbolC1'] == True:
                fM = 3 # символьное представление
                
            
            if values['2C2'] == True:
                fT = 1 # 2-ичное представление
            elif values['16C2'] == True:
                fT = 2 # 16-ричное представление
            elif values['symbolC2'] == True:
                fT = 3 # символьное представление
            
            
            # ----------------------------------- проверка изменяемого сообщения
            if M == "":
                sg.popup_ok("Сначала введите текст, для которого меняется формат")
            else:
                # проверяем, в нужном ли формате задано сообщение
                if fM == 1:
                    flag, textError = wI.check2(M)
                elif fM == 2:
                    flag, textError = wI.check16(M)
                elif fM ==3:
                    flag, textError = wI.checkSymbol(M)
                
                if flag == False:
                    sg.popup_ok(textError)
                else:
                # ----------------------------------- изменение формата
                    
                    Mnew = [] # сообщение, разбитое на символы (необходимо, если формат не символьный)
                    
                    if fM != 3:
                        Mnew = M.split()
                    else:
                        Mnew = M
                    
                    if fM == 2:
                        resText = wI.from16To2(Mnew)
                    elif fM == 3:
                        resText = wI.fromSymbolTo2(Mnew)
                    else:
                        resText = Mnew
                    
                    if fT == 2:
                        window['result3'].update(' '.join(wI.from2To16(resText)))
                    elif fT == 3:
                        window['result3'].update(wI.from2ToSymbol(resText))
                    else:
                        window['result3'].update(' '.join(resText))
                    

# -----------------------------------------------------------------------------
        # генерация блока текста M (шифрование)
        elif event == 'ok6':
            
            M = "" # значение сообщения
            fM = 0 # формат ключа
            
            if values['2M'] == True:
                fM = 1 # 2-ичное представление
            elif values['16M'] == True:
                fM = 2 # 16-ричное представление
            elif values['symbolM'] == True:
                fM = 3 # символьное представление
            
            M = wI.newRepresent(bbs.BBS(128))
                
            # переводим ключ в нужный формат
            if fM == 2:
                M = wI.from2To16(M)
            elif fM == 3:
                M = wI.from2ToSymbol(M)
                        
            if fM == 1 or fM == 2:
                window['M'].update(' '.join(M))
            else:
                window['M'].update(M)

# -----------------------------------------------------------------------------
        # генерация блока текста C (дешифрование)
        elif event == 'ok7':
            
            C = "" # значение сообщения
            fC = 0 # формат ключа
            
            if values['2C'] == True:
                fC = 1 # 2-ичное представление
            elif values['16C'] == True:
                fC = 2 # 16-ричное представление
            elif values['symbolC'] == True:
                fC = 3 # символьное представление
            
            C = wI.newRepresent(bbs.BBS(128))
                
            # переводим ключ в нужный формат
            if fC == 2:
                C = wI.from2To16(C)
            elif fC == 3:
                C = wI.from2ToSymbol(C)
                        
            if fC == 1 or fC == 2:
                window['C'].update(' '.join(C))
            else:
                window['C'].update(C)
                            

Nb = 4
Nr = 10
Nk = 4 # длина ключа
bbs = bbs()
wI = wwi()

main()