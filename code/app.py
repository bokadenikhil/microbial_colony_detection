def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['Install',package])
import streamlit as st
from PIL import Image
import pandas as pd
install_and_import('opencv-python')
import cv2
import os
import time
#------------------#
input_path = r'C:\Users\Nikhil.Bokade\OneDrive - Tridiagonal Solutions\TSPL\Other\git\microbial colony detection\src\input'
output_path = r'C:\Users\Nikhil.Bokade\OneDrive - Tridiagonal Solutions\TSPL\Other\git\microbial colony detection\src\processed'
logo_path = r'C:\Users\Nikhil.Bokade\OneDrive - Tridiagonal Solutions\TSPL\Other\git\microbial colony detection\src\logo'
#---------------------------------#
st.markdown("<h1 style='text-align: center;color:yellow;'>Microbial Colony Detection</h1>", unsafe_allow_html=True)
# Starting part
os.chdir(input_path)
files = os.listdir()
try:
    with st.sidebar:
        #logo = Image.open(logo_path+'\logo.png')
        #st.image(logo,width=250)
        st.header('Microbial Colony Detection')
        uploaded_file = st.file_uploader("Choose a Image file", accept_multiple_files=False)
        if uploaded_file != None:
            im1 = Image.open(uploaded_file.name)
            im = cv2.imread(uploaded_file.name)
#------------------------------------------------------#
    _, _, _, col, _, _, _ = st.columns([1]*6+[1.18])
    clicked = col.button('start')
    col1,col2 = st.columns(2)
    if clicked:
        with col1:
            st.header('Input Image')
            st.image(im1)
            # convert to grayscale
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            # threshold
            thresh = cv2.threshold(gray,128,255,cv2.THRESH_BINARY)[1]
            # get contours
            boxes = []
            result = im.copy()
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            for cntr in contours:
                x,y,w,h = cv2.boundingRect(cntr)
                if h < 50:
                    if w>5:
                        cv2.rectangle(im, (x, y), (x + w, y + h), (255,0,0))
                        boxes.append([x,y,w,h])
            noOfColonies = len(boxes)
        with col2:
            st.header('Result')
            with st.spinner('Wait for it...'):
                time.sleep(5)
                st.success('Done!')
            if noOfColonies == 0:
                st.text('0 Colonies located')
            else:
                st.text(f'{noOfColonies} colonies located')
            
                
except Exception as e:
    st.text(e)
    #st.snow()
