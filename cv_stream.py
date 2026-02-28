import cv2
import numpy as np
import time
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

""" Aut_Cell_2D(reglas) ejecutará el programa deseado
reglas = 'juego de la vida' para el juego de la vida
reglas = 'solidificación Neumann' Para ejecutar solidificación.

Al dibujarse la rejilla se espera la condición inicial y se da 'Enter' para
inicial el proceso. Se puede agregar puntos durante el proceso (no supe cómo quitarle)
El proceso se puede bloquear con 'Enter'"""


class juego_dela_vida:
    def __init__(self, regla, tam, div, img=None, run_game=False):
        self.regla = regla
        self.tam = tam
        self.div = div
        self.lines = np.arange(0, self.tam, step=int(self.tam/self.div), dtype=int)
        self.cuadrito = int(self.tam/self.div)

        if img is None:
            self.img = np.ones((self.tam,self.tam,3), np.uint8)*255 ## matriz de imagen en pantalla
            self.matriz_juego = np.zeros((len(self.lines)-1, len(self.lines)-1), dtype=int)
            self.img[self.lines, :, :] = 0 #dibujamos la rejilla
            self.img[:, self.lines, :] = 0 #dibujamos la rejilla
            st.write('NUEVAIMg')
        else:
            self.img = img['img']
            self.matriz_juego = img['Matriz']
            st.write('viega')

        ## dibujamos la imagen con rejilla y esperamos a que se dé una condición inicial
        # cv2.namedWindow('image') 
        # cv2.setMouseCallback('image', draw_rejilla)
        # esperamos la condición inicial e inicia con enter
        # while(1):
            # cv_im = cv2.imshow('image', self.img)


        
        streamlit_image_coordinates(self.img, key='image', on_click=self.change_color)

        if run_game:
            self.juego_de_la_vida()
        else:
            st.button('Iniciar juego de la vida', on_click=self.run_game_now)
            # k = cv2.waitKey(100) & 0xFF
            # if k == 13:
            #     break
            #     cv2.destroyAllWindows()
        ## inicia el dibujo
        # for i in range(0, 100):
        #     cv2.imshow('image', img)
        #     k = cv2.waitKey(100) & 0xFF
        #     if k == 13 or i==99:
        #         cv2.destroyAllWindows()
        #         break
        #     matriz_juego = aplicar_reglas(matriz_juego, regla)
        #     time.sleep(0.05)
    def run_game_now(self):
        st.session_state['run_game'] = True
        st.write('')
    def quit_game(self):
        st.session_state['run_game'] = False
        st.write('')

    def change_color(self):
        self.click = st.session_state['image']
        if self.click is not None:
            x_square = int(self.click['x']/self.cuadrito)
            y_square = int(self.click['y']/self.cuadrito)
        
            x_initpx = x_square*self.cuadrito
            x_finpx = x_initpx+self.cuadrito
            y_initpx = y_square*self.cuadrito
            y_finpx = y_initpx+self.cuadrito

            valor = self.matriz_juego[x_square,  y_square]
            if valor == 1:
                self.matriz_juego[x_square , y_square] = 0
                self.img[y_initpx:y_finpx,x_initpx:x_finpx,:] = 255
            elif valor == 0:
                self.matriz_juego[x_square , y_square] = 1
                self.img[y_initpx:y_finpx,x_initpx:x_finpx,:] = 0

            st.session_state["img_game"] = {'img': self.img, 
                                        'Matriz':self.matriz_juego}



    def juego_de_la_vida(self):
        st.button('Iniciar juego de la vida', on_click=self.quit_game)
        indices_cero = np.argwhere(self.matriz_juego == 0)
        indices_uno = np.argwhere(self.matriz_juego == 1)


        reviven = 0
        for index in indices_cero:
            if np.sum(self.matriz_juego[max(index[0]-1,0):index[0]+2, max(index[1]-1,0):index[1]+2])==3:
                self.matriz_juego[index[0],index[1]] = 1
                x_initpx = index[0]*self.cuadrito
                x_finpx = x_initpx+self.cuadrito
                y_initpx = index[1]*self.cuadrito
                y_finpx = y_initpx+self.cuadrito
                self.img[y_initpx:y_finpx,x_initpx:x_finpx,:] = 0
                reviven +=1

        mueren=0
        for index in indices_uno:
            vecinos = np.sum(self.matriz_juego[max(index[0]-1,0):index[0]+2, max(index[1]-1,0):index[1]+2]) - 1
            if vecinos<2 or vecinos>3:
                self.matriz_juego[index[0],index[1]] = 0
                x_initpx = index[0]*self.cuadrito
                x_finpx = x_initpx+self.cuadrito
                y_initpx = index[1]*self.cuadrito
                y_finpx = y_initpx+self.cuadrito
                self.img[y_initpx:y_finpx,x_initpx:x_finpx,:] = 255
                mueren+=1

        st.session_state["img_game"] = {'img': self.img, 
                        'Matriz':self.matriz_juego}

    
        st.write(f'reviven {reviven} \n mueren {mueren}')
        time.sleep(0.2)
        
        st.rerun()

######### función 
def Aut_Cell_2D(regla):
    global tam, div, lines, img, matriz_juego
    tam = 750 #tamaño rejilla (cuadrada)
    div = 100 ## divisiones (si no es exacta la división, se redondeará)
    img = np.ones((tam,tam,3), np.uint8)*255 ## matriz de imagen en pantalla
    lines = np.arange(0, tam, step=int(tam/div), dtype=int) ## rejilla
    matriz_juego = np.zeros((len(lines)-1, len(lines)-1), dtype=int) ## matriz inicial del algoritmo

    img[lines, :, :] = 0 #dibujamos la rejilla
    img[:, lines, :] = 0 #dibujamos la rejilla
    
    ## dibujamos la imagen con rejilla y esperamos a que se dé una condición inicial
    cv2.namedWindow('image') 
    cv2.setMouseCallback('image', draw_rejilla)
    # esperamos la condición inicial e inicia con enter
    while(1):
        cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xFF
        if k == 13:
            break
            cv2.destroyAllWindows()
    ## inicia el dibujo
    for i in range(0, 100):
        cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xFF
        if k == 13 or i==99:
            cv2.destroyAllWindows()
            break
        matriz_juego = aplicar_reglas(matriz_juego, regla)
        time.sleep(0.05)



### reglas aplicadas
def reglas_neumann(celdas, index):
    global img
    vecinos_vivos = celdas.sum()
    if celdas[1, 1] == 0 and (vecinos_vivos == 1 or vecinos_vivos == 2):
        ## para encender
        celda_sal = 1 
        cambiar_color(lines[index[0]] + 1, lines[index[1]] + 1) #cambiamos el color de img
    else:
        # En cualquier otro caso, se mantiene la celda como está, ya sea viva o muerta
        celda_sal = celdas[1, 1]
    return celda_sal

def reglas_juego_de_la_vida(celdas, index):
    global img
    vecinos_vivos = celdas.sum()
    if celdas[1, 1] == 0 and vecinos_vivos == 3:
        # nacimiento :)
        celda_sal = 1
        cambiar_color(lines[index[0]] + 1, lines[index[1]] + 1) #cambiamos el color de img
    elif celdas[1, 1] == 1 and ((vecinos_vivos - 1) > 3 or (vecinos_vivos - 1) < 2):
        # muerte por sobrepoblación o por soledad :C
        celda_sal = 0
        cambiar_color(lines[index[0]]+1, lines[index[1]] + 1) #cambiamos el color de img
    else:
        # En cualquier otro caso, se mantiene la celda como está, ya sea viva o muerta
        celda_sal = celdas[1, 1]
    return celda_sal


def aplicar_reglas(matriz_entrada, regla):
    global img
    s = (np.size(matriz_entrada, 0), np.size(matriz_entrada, 1))
    # creamos una matriz pegando fronteras
    matriz_inicial = np.zeros((s[0]+2, s[1]+2))
    matriz_inicial[1:-1, 1:-1] = matriz_entrada
    matriz_inicial[1:-1,0] = matriz_entrada[:,-1]
    matriz_inicial[1:-1,-1] = matriz_entrada[:,1]
    matriz_inicial[0] = matriz_inicial[-2]                                
    matriz_inicial[-1] = matriz_inicial[1]     

    # matriz donde guardamos datos                          
    matriz_sal = np.zeros(s)

    ## para cada celda aplicamos las reglas, dependiendo qué regla
    for i in range(0, s[0]):
        for j in range(0, s[1]):
            if regla == 'juego de la vida':
                matriz_sal[i, j] = reglas_juego_de_la_vida(matriz_inicial[i :i + 3, j :j + 3], (i,j))
            elif regla == 'solidificación Neumann':
                matriz_sal[i, j] = reglas_neumann(matriz_inicial[i :i + 3, j :j + 3], (i, j))
    return matriz_sal


########## para dibujar el plot
def buscar_coord(x): 
    #dando click en la coordenada x, buscamos a cuál corresponde 
    #en los indices de la matriz del gráfico y el pixel inicial de esa región
    for l in range(0, len(lines)-1):
        if x >= lines[l] and x <= lines[l+1]:
            coord = lines[l] #pixel inicial
            ind = l # indice en la matriz 
            break
    return [coord, ind]

def cambiar_color(x, y, cond_ini=False):
    # (x,y) = posición del pixel donde se dio click (o el que se indique)
    global img, matriz_juego
    [coord_img_x, coord_matr_x] = buscar_coord(x) # busca x en la matriz de imagen & matriz del algoritmo
    [coord_img_y, coord_matr_y] = buscar_coord(y) # busca y en la matriz de imagen & matriz del algoritmo
    #cambiaremos el cuadro desde start_p hasta end_p
    start_p = (coord_img_x + 1, coord_img_y + 1) 
    end_p = ((start_p[0] + tam // div) - 1, (start_p[1] + tam // div) - 1) 
    # cambiamos color de negro a blanco y si es blanco, cambiamos a negro
    # notemos que solo cambiamos lo que previamente se iba a cambiar no importa el color
    if np.ndarray.tolist(img[start_p[1], start_p[0] + 1, :]) == [0, 0, 0]:
        color = (255, 255, 255)
        if cond_ini: #cambiamos la matriz inicial
            matriz_juego[coord_matr_x, coord_matr_y] = 0
    else:
        color = (0, 0, 0)
        if cond_ini: #cambiamos la matriz inicial
            matriz_juego[coord_matr_x, coord_matr_y] = 1
    # se cambia el color en la imagen
    img[start_p[1]: end_p[1], start_p[0]: end_p[0]] = color

## esta funcion registra el click y qué hacer al detectarlo
def draw_rejilla(event,x,y,flags,param):
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        cambiar_color(x, y, cond_ini=True)

######### función 
def Aut_Cell_2D(regla):
    global tam, div, lines, img, matriz_juego
    tam = 750 #tamaño rejilla (cuadrada)
    div = 100 ## divisiones (si no es exacta la división, se redondeará)
    img = np.ones((tam,tam,3), np.uint8)*255 ## matriz de imagen en pantalla
    lines = np.arange(0, tam, step=int(tam/div), dtype=int) ## rejilla
    matriz_juego = np.zeros((len(lines)-1, len(lines)-1), dtype=int) ## matriz inicial del algoritmo

    img[lines, :, :] = 0 #dibujamos la rejilla
    img[:, lines, :] = 0 #dibujamos la rejilla
    
    ## dibujamos la imagen con rejilla y esperamos a que se dé una condición inicial
    cv2.namedWindow('image') 
    cv2.setMouseCallback('image', draw_rejilla)
    # esperamos la condición inicial e inicia con enter
    while(1):
        cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xFF
        if k == 13:
            break
            cv2.destroyAllWindows()
    ## inicia el dibujo
    for i in range(0, 100):
        cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xFF
        if k == 13 or i==99:
            cv2.destroyAllWindows()
            break
        matriz_juego = aplicar_reglas(matriz_juego, regla)
        time.sleep(0.05)

if "img_game" not in st.session_state:
    st.session_state["img_game"] = None
if 'run_game' not in st.session_state:
    st.session_state['run_game'] = False

juego_dela_vida('juego de la vida',  tam = 750, div = 100, img=st.session_state["img_game"], run_game=st.session_state['run_game'])


# import streamlit as st
# from PIL import Image, ImageDraw
# from streamlit_image_coordinates import streamlit_image_coordinates

# # Initialize/update points in session state
# if "points" not in st.session_state:
#     st.session_state["points"] = []

# def add_point():
#     """Callback to add click coordinates to session state and trigger rerun."""
#     raw_value = st.session_state["pil_image"] 
#     if raw_value is not None:
#         point = (raw_value["x"], raw_value["y"])
#         if point not in st.session_state["points"]:
#             st.session_state["points"].append(point)
#             st.rerun() #

# # Load and update image with drawn points
# img = Image.open(r"C:\Users\aleja\Pictures\peluche_math.png") 
# draw = ImageDraw.Draw(img)
# for point in st.session_state["points"]:
#     radius = 5
#     draw.ellipse((point[0]-radius, point[1]-radius, point[0]+radius, point[1]+radius), fill="red")

# # Display and capture clicks
# streamlit_image_coordinates(img, key="pil_image", on_click=add_point)
# st.write("Clicked points:", st.session_state["points"])