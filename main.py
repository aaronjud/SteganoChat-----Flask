 from PIL import Image
import numpy as np
from numpy import array
import sys 
from sub_main import AESCipher 
import os
binary_image = [] 
plain_text=[] 
binary_result = [] 
image_result = [] 





def get_text(text):
    text= text.encode("UTF-8")
    text=list(text)
    for i in range(0,len(text)):
        text[i] = list(format(text[i], '08b'))

    for i in range(0,len(text)):
        for j in range(0,8):
            text[i][j] = int(text[i][j]) 
            plain_text.append(int(text[i][j])) 

    
    return plain_text


def process_image(img,plain_text,filename):
    pixel_info=[] #
    row=[] #
    final_image=[] #
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            binary_image.append(img.getpixel((y,x))[0])
            binary_image.append(img.getpixel((y,x))[1])
            binary_image.append(img.getpixel((y,x))[2])
            binary_image.append(img.getpixel((y,x))[3])
    
    for i in range(0, len(binary_image)):
        binary_result.append( plain_text[i]^binary_image[i])
    
    for i in range(0,len(binary_result)):
        pixel_info.append(binary_result[i])
        if i % 4 == 3:
            image_result.append(pixel_info)
            pixel_info=[]
    for i in range(0, len(image_result)):
        row.append(image_result[i])
        if i % 64 == 63:
            final_image.append(row)
            row=[]
    im=Image.fromarray(array(final_image,dtype=np.uint8),mode="RGBA")
    im.save(filename)
    pixel_info.clear()
    row.clear()
    final_image.clear()
    return im


def generate_random(w,h,filename):
    pixel_data=np.random.randint(low=0,high=255,size=(w,h,4),dtype=np.uint8)
    image=Image.fromarray(pixel_data)
    image.save(filename)
    return image


def fill_message(text):
    message_size=len(text)
    if message_size<=2048:
        text=("{: <2048}".format(text))
        return text


def decode_image(stg,key):
    
    stg_image=[]
    for x in range(stg.size[0]):
        for y in range(stg.size[1]):
            stg_image.append(stg.getpixel((y,x))[0])
            stg_image.append(stg.getpixel((y,x))[1])
            stg_image.append(stg.getpixel((y,x))[2])
            stg_image.append(stg.getpixel((y,x))[3])
    key_image=[]
    for x in range(key.size[0]):
        for y in range(key.size[1]):
            key_image.append(key.getpixel((y,x))[0])
            key_image.append(key.getpixel((y,x))[1])
            key_image.append(key.getpixel((y,x))[2])
            key_image.append(key.getpixel((y,x))[3])
    decoded_text=[]
    for i in range(0,len(key_image)):
        decoded_text.append(stg_image[i]^key_image[i])
    byte=[]
    words=[]
    for i in range(0,len(decoded_text)):
        byte.append(str(decoded_text[i]))
        if i % 8 == 7:
            words.append(chr(int(''.join(byte),2)))
            byte=[]
    result = ''.join(words)
    stg_image.clear
    return result 

def encrypt_message(pwd, text):
    crypto  =  AESCipher(pwd)
    message = crypto.encrypt(text)
    return(message)

def decrypt_message(pwd, text):
    crypto  =  AESCipher(pwd)
    message = crypto.decrypt(text)
    return(message)

        
def decode(filename):
        password = "1234"
        key = Image.open("./key/k_" + filename )
        key = key.convert("RGBA")
        stg_image = Image.open("./image/s_"+ filename )
        stg_image = stg_image.convert("RGBA")
        decoded_text = decode_image(stg_image,key)
        decoded_text = decoded_text.strip()
        Decoded_Text =decrypt_message(password,decoded_text)
        return(Decoded_Text)
    


def encode(text,filename):
    password = "1234"
    binary_image.clear()
    plain_text.clear()
    binary_result.clear()
    image_result.clear()
    text = encrypt_message(password, text)
    text = fill_message(text)
    
    # Specify the "key" and "image" folders
    key_folder = "key"
    image_folder = "image"
    
    # Create the full paths for input and output filenames
    input_filename = os.path.join(key_folder, "k_" + filename)
    output_filename = os.path.join(image_folder, "s_" + filename)
    
    key = generate_random(64, 64, input_filename)
    binary_text = get_text(text)
    stg_image = process_image(key, binary_text, output_filename)


