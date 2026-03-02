import numpy as np
import time
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

""" Al dibujarse la rejilla se espera la condición inicial puedes ejecutar el proceso
pulsando el boton "Iniciar juego de la vida". Se puede agregar puntos durante el proceso.
El proceso se detendrá al pulsa "Detener juego de la vida". """


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

        else:
            self.img = img['img']
            self.matriz_juego = img['Matriz']


        ## dibujamos la imagen con rejilla y esperamos a que se dé una condición inicial
        st.button('Fill_random', on_click=self.fill_with_random)

        streamlit_image_coordinates(self.img, key='image', on_click=self.change_color)

        if run_game:
            self.juego_de_la_vida()
        else:
            st.button('Iniciar juego de la vida', on_click=self.run_game_now)

    def fill_with_random(self):
        random_matrix = np.random.randint(low=0, high=2, size=(self.matriz_juego.shape[0],
                                                               self.matriz_juego.shape[1]))
        self.matriz_juego = np.maximum(random_matrix, self.matriz_juego)

    
        indices_uno = np.argwhere(random_matrix == 1)
        indices_uno_orig = np.argwhere(random_matrix == 1)

        for index in indices_uno:
            x_initpx = index[0]*self.cuadrito
            x_finpx = x_initpx+self.cuadrito
            y_initpx = index[1]*self.cuadrito
            y_finpx = y_initpx+self.cuadrito
            self.img[y_initpx:y_finpx,x_initpx:x_finpx,:] = 0
            
        st.session_state["img_game"] = {'img': self.img, 
                        'Matriz':self.matriz_juego}

        st.write(f'Se encendieron {len(indices_uno) - len(indices_uno_orig)} celdas')
        

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
        st.button('Detener juego de la vida', on_click=self.quit_game)
        indices_cero = np.argwhere(self.matriz_juego == 0)
        indices_uno = np.argwhere(self.matriz_juego == 1)

        new_matrix = self.matriz_juego.copy()
        reviven = 0
        for index in indices_cero:
            if np.sum(self.matriz_juego[max(index[0]-1,0):index[0]+2, max(index[1]-1,0):index[1]+2])==3:
                new_matrix[index[0],index[1]] = 1
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
                new_matrix[index[0],index[1]] = 0
                x_initpx = index[0]*self.cuadrito
                x_finpx = x_initpx+self.cuadrito
                y_initpx = index[1]*self.cuadrito
                y_finpx = y_initpx+self.cuadrito
                self.img[y_initpx:y_finpx,x_initpx:x_finpx,:] = 255
                mueren+=1

        self.matriz_juego = new_matrix.copy()
        st.session_state["img_game"] = {'img': self.img, 
                        'Matriz':self.matriz_juego}

    
        st.write(f'reviven {reviven} \n mueren {mueren}')
        time.sleep(1/24)
        
        st.rerun()

######### función 

if "img_game" not in st.session_state:
    st.session_state["img_game"] = None
if 'run_game' not in st.session_state:
    st.session_state['run_game'] = False

juego_dela_vida('juego de la vida',  tam = 750, div = 100, img=st.session_state["img_game"], run_game=st.session_state['run_game'])


