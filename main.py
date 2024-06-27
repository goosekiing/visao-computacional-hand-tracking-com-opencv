"Hand Tracking with OpenCV"

import cv2 # cv2.__version__ 3.4.8
import mediapipe as mp #mp.__version__ 0.8.11
from typing import List, Tuple, Dict
import numpy as np
import os
from time import sleep
from pynput.keyboard import Controller, Key

BRANCO = (255, 255, 255)
PRETO = (0,0,0)
AZUL = (255,0,0)
VERDE = (0,255,0)
VERMELHO = (0,0,255)
AZUL_CLARO = (255,255,0)
CINZA_ESCURO = (64,64,64)

mp_maos = mp.solutions.hands
mp_desenhos = mp.solutions.drawing_utils

maos = mp_maos.Hands()

camera = cv2.VideoCapture(0)
resolucao_x = 1280
resolucao_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucao_y)

def main()-> None:
    """Main execution function."""
    clear_terminal()
    bloco_notas = False
    offset_x = 250
    offset_y = 30
    tamanho_tecla = 50
    teclas = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
              ['A','S','D','F','G','H','J','K','L'],
              ['Z','X','C','V','B','N','M', ',','.',' ']]
    contador = 0
    texto = "> "
    teclado = Controller()
    img_quadro = np.ones((resolucao_y, resolucao_x, 3), np.uint8)*255
    cor_pincel = [255,0,0]
    espessura_pincel = 7
    x_quadro, y_quadro = 0, 0

    while True:
        sucesso, img = camera.read()
        img = cv2.flip(img, 1)

        img, todas_maos = encontra_coordenadas_maos(img=img)

        if len(todas_maos) == 1:
            if todas_maos[0]["lado"] == "Left":
                info_dedos_mao1 = dedos_levantados(todas_maos[0])
                indicador_x, indicador_y, indicador_z = todas_maos[0]["coordenadas"][8]
                cv2.putText(img, f"Distancia camera: {indicador_z}", (850,50),cv2.FONT_HERSHEY_COMPLEX, 1, BRANCO, 2)
                for indice_linha, linha_teclado in enumerate(teclas):
                    for indice, letra in enumerate(linha_teclado):
                        if sum(info_dedos_mao1) <= 1:
                            letra = letra.lower()
                        img = imprime_botoes(img, (offset_x+indice*80, offset_y+indice_linha*80), letra, tamanho=tamanho_tecla)
                        if offset_x + indice*80 < indicador_x < (offset_x+tamanho_tecla)+indice*80 and offset_y+indice_linha*80 < indicador_y < (offset_y+tamanho_tecla)+indice_linha*80:
                            img = imprime_botoes(img, (offset_x+indice*80, offset_y+indice_linha*80), letra, tamanho=tamanho_tecla, espessura_borda_tecla=2, cor_letra=PRETO)
                            if indicador_z < -100:
                                contador = 1
                                escreve = letra
                                img = imprime_botoes(img, (offset_x+indice*80, offset_y+indice_linha*80), letra, tamanho=tamanho_tecla, cor_letra=VERMELHO, espessura_borda_tecla=2)
                if contador:
                    contador +=1
                    if contador == 3:
                        texto += escreve
                        contador = 0
                        teclado.press(escreve)

                if info_dedos_mao1 == [False, False, False, False, True] and len(texto) > 2:
                    texto = texto[:-1]
                    sleep(0.15)

                cv2.rectangle(img, (offset_x, 450), (830, 500), BRANCO, cv2.FILLED)
                cv2.rectangle(img, (offset_x, 450), (830, 500), PRETO, 1)
                cv2.putText(img, texto[-40:], (offset_x, 480),cv2.FONT_HERSHEY_COMPLEX, 1, PRETO, 2)
                cv2.circle(img, (indicador_x, indicador_y), 7, AZUL, cv2.FILLED)

            if todas_maos[0]["lado"] == "Right":
                info_dedos_mao1 = dedos_levantados(todas_maos[0])
                if info_dedos_mao1 == [False, True, False, False, False] and bloco_notas is False:
                    bloco_notas = True
                    os. startfile(r"C:\WINDOWS\system32\notepad.exe")
                if info_dedos_mao1 == [False, False, False, False, False] and bloco_notas is True:
                    bloco_notas = False
                    os.system("TASKKILL /IM notepad.exe")
                if info_dedos_mao1 == [False, False, True, False, False]:
                    break
        
        if len(todas_maos) == 2:
            info_dedos_mao1 = dedos_levantados(todas_maos[0])
            info_dedos_mao2 = dedos_levantados(todas_maos[1])

            indicador_x, indicador_y, indicador_z = todas_maos[0]["coordenadas"][8]

            if sum(info_dedos_mao2) == 1:
                cor_pincel = AZUL
            elif sum(info_dedos_mao2) == 2:
                cor_pincel = VERDE
            elif sum(info_dedos_mao2) == 3:
                cor_pincel = VERMELHO
            elif sum(info_dedos_mao2) == 4:
                cor_pincel = PRETO
            elif sum(info_dedos_mao2) == 5:
                cor_pincel = BRANCO
            else:
                img_quadro = np.ones((resolucao_y, resolucao_x, 3), np.uint8)*255

            espessura_pincel = int(abs(indicador_z))//10+3
            cv2.circle(img, (indicador_x, indicador_y), espessura_pincel, cor_pincel, cv2.FILLED)

            if info_dedos_mao1 == [False, True, False, False, False]:
                if x_quadro == 0 and y_quadro == 0:
                    x_quadro, y_quadro = indicador_x, indicador_y
                cv2.line(img_quadro, (x_quadro, y_quadro), (indicador_x, indicador_y), cor_pincel, espessura_pincel)
                x_quadro, y_quadro = indicador_x, indicador_y
            else:
                x_quadro, y_quadro = 0, 0

            img = cv2.addWeighted(img, 1, img_quadro, 0.2, 0)

        cv2.imshow("imagem", img)
        cv2.imshow("Quadro", img_quadro)
        tecla = cv2.waitKey(1)
        if tecla == 27:
            break

    with open("texto.txt", "w") as arquivo:
        arquivo.write(texto)

    cv2.imwrite("quadro.png", img_quadro)

def encontra_coordenadas_maos(img: np.ndarray):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    resultado = maos.process(img_rgb)

    todas_maos: List[Dict] = []
    if resultado.multi_hand_landmarks:
        for lado_mao, marcacoes_maos in zip(resultado.multi_handedness, resultado.multi_hand_landmarks):
            info_mao: Dict = {}
            coordenadas:List[Tuple[int, int, int]] = []
            for marcacao in marcacoes_maos.landmark:
                coord_x, coord_y, coord_z = int(marcacao.x * resolucao_x), int(marcacao.y * resolucao_y), int(marcacao.z * resolucao_x)
                coordenadas.append((coord_x, coord_y, coord_z))

            info_mao["coordenadas"] = coordenadas
            info_mao["lado"] = lado_mao.classification[0].label
            todas_maos.append(info_mao)
            mp_desenhos.draw_landmarks(img, marcacoes_maos, mp_maos.HAND_CONNECTIONS)
    
    return img, todas_maos

def dedos_levantados(mao):
    dedos:List = []
    if mao['lado'] == 'Right': 
        if mao['coordenadas'][4][0] < mao['coordenadas'][3][0]:
            dedos.append(True)
        else:
            dedos.append(False)
    else:
        if mao['coordenadas'][4][0] > mao['coordenadas'][3][0]:
            dedos.append(True)
        else:
            dedos.append(False)
    for ponta_dedo in [8,12,16,20]:
        if mao["coordenadas"][ponta_dedo][1] < mao["coordenadas"][ponta_dedo-2][1]:
            dedos.append(True)
        else:
            dedos.append(False)
    return dedos

def imprime_botoes(img, posicao, letra, tamanho=50, cor_preenchimento_retangulo=BRANCO, cor_borda_retangulo=PRETO, espessura_borda_tecla=1, cor_letra=CINZA_ESCURO):
    cv2.rectangle(img, posicao, (posicao[0]+tamanho, posicao[1]+tamanho), cor_preenchimento_retangulo, cv2.FILLED)
    cv2.rectangle(img, posicao, (posicao[0]+tamanho, posicao[1]+tamanho), cor_borda_retangulo, espessura_borda_tecla)
    cv2.putText(img, letra, (posicao[0]+15, posicao[1]+35), cv2.FONT_HERSHEY_COMPLEX, 1, cor_letra, 2)
    return img

def clear_terminal() -> None:
    """Clears the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n-------|-----|-------\nExecução Interrompida\n-------|-----|-------\n")
