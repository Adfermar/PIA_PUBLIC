# Version v2.4
# Last modification: 24/11/2022
from PIL import Image

import numpy as np

from random import randint



class ImgNumpy:

  def __init__(self, name='', W = 1, H = 1, R = 0, G = 0, B = 0):
    # En los métodos para imágenes primero va el ancho y luego el alto
    # En los arrays numpy primer va el alto y luego el ancho
    # np.zeros((height, width))
    self._array = np.zeros((H, W, 3), dtype = np.uint8)
    self._name = name
    self._height = H
    self._width = W
    self._red = R
    self._green = G
    self._blue = B
    for i in range(0, self._array.shape[0]):
      for j in range(0, self._array.shape[1]):
        self._array[i, j] = [R, G, B]
  
  # propiedad imagen: devuelve una imagen creada desde el array
  # equivale a tener una variable de instancia tipo <self._img>
  @property
  def img(self):
      return Image.fromarray(self._array) #self._img 

  # name
  @property
  def name(self):
      return self._name  

  @name.setter
  def name(self, value):
      if value.isalpha():
        self._name = value
      else:
        raise ValueError("Not a valid name.\n \
        Only alphabetic characters allowed.")

  #array
  @property
  def array(self):
    return self._array

  # Nuevo en la versión v2.3
  #-------------------------
  # array setter
  @array.setter
  def array(self, new_np_array):
    self._array = new_np_array
    self._height = new_np_array.shape[0]
    self._width = new_np_array.shape[1]
    self._red = 0
    self._green = 0
    self._blue = 0
    #-------------------------

  # height
  @property
  def height(self):
      return self._height

  @height.setter
  def height(self, value):
    img = self.img
    img = img.resize((self._width, value))
    self._array = np.asarray(img)
    self._height = value

  # width
  @property
  def width(self):
      return self._width

  @width.setter
  def width(self, value):
    img = self.img
    img = img.resize((value, self._height))
    self._array = np.asarray(img)        
    self._width = value

  # red
  @property
  def red(self):
      return self._red

  @red.setter
  def red(self, value):
        self._red = value
        new_arr = self._array.copy()
        for i in range(0, self._array.shape[0]):
          for j in range(0, self._array.shape[1]):
            # self._array[i, j] = [value, self._green, self._blue]
            new_arr[i, j] = [value, self._green, self._blue]
        self._array = new_arr
  
  # green
  @property
  def green(self):
      return self._green

  @green.setter
  def green(self, value):
        self._green = value
        new_arr = self._array.copy()
        for i in range(0, self._array.shape[0]):
          for j in range(0, self._array.shape[1]):
            new_arr[i, j] = [self._red, value, self._blue]
        self._array = new_arr

  # blue
  @property
  def blue(self):
      return self._blue

  @blue.setter
  def blue(self, value):
        self._blue = value
        new_arr = self._array.copy()
        for i in range(0, self._array.shape[0]):
          for j in range(0, self._array.shape[1]):
            new_arr[i, j] = [self._red, self._green, value]
        self._array = new_arr 

  # About image info
  #-----------------------------------------------------------
  def get_img_format(self):
    img = Image.fromarray(self._array)
    return img.format

  def get_img_format_desc(self):
    img = Image.fromarray(self._array)
    return img.format_description

  def get_img_size(self):
    img = Image.fromarray(self._array)
    return img.size

  def get_img_mode(self):
    img = Image.fromarray(self._array)
    return img.mode

  def get_img_info(self):
    img = Image.fromarray(self._array)
    return (img.format, img.format_description, img.size, img.mode) 
    return print("\nFormat: ", img.format,
              "\nFormat Description: ", img.format_description,
              "\nSize: ", img.size, 
              "\nMode: ", img.mode)

  #-----------------------------------------------------------

  # Devuelve información sobre las
  # variables del objeto
  def print_info(self):
    return print("\nNombre: ", self._name,
                 "\nAncho: ", self._width,
                 "\nAlto: ", self._height, 
                 "\nColor rojo: ", self._red,
                 "\nColor verde: ", self._green,
                 "\nColor azul: ", self._blue)
  
  # Devuelve el shape del array
  def get_ndim(self):
    return self._array.ndim

  # Devuelve el shape del array    
  def get_itemsize(self):
    return self._array.itemsize

  # Devuelve el shape del array
  def get_size(self):
    return self._array.size
  
  # Devuelve el shape del array
  def get_shape(self):
    return self._array.shape

  # Exercise's methods:
  # -------------------

  # c.) Redimensiona la imagen

  def resize(self, width, height):
    # resize(width, height)
    img = self.img
    img = img.resize((width, height))
    self._array = np.asarray(img)        
    self._height = height        
    self._width = width

  # ------------------------------------------------------------------------

  # d.) Redimensiona el ancho dejando el mismo alto
  
  def resize_w(self, new_width):
    # resize(width, height)
    img = Image.fromarray(self._array)
    img = img.resize((new_width, self._height))
    self._array = np.asarray(img)              
    self._width = new_width     

  # ------------------------------------------------------------------------

  # e.) Redimensiona el alto dejando el mismo ancho
 
  def resize_h(self, new_height):
    # resize(width, height)
    img = Image.fromarray(self._array)
    img = img.resize((self._width, new_height))
    self._array = np.asarray(img)              
    self._height = new_height 

  # ------------------------------------------------------------------------

  # f.) Implementa un método que devuelva un trozo de una imagen 
  # especificando la posición horizontal y vertical y el ancho y el alto,
  # si las dimensiones especificadas son superiores a la
  # imagen original, debe devolver el recorte disponible.

  # Opción A
  
  def cropped(self, x_start, y_start, x_end, y_end):
    img = Image.fromarray(self._array)
    cropped = Image.fromarray(self._array)
    if ( 
        ( x_start < x_end ) and
        ( y_start < y_end ) and
        ( x_start + x_end < img.size[0] ) and
        ( y_start + y_end < img.size[1] ) 
      ):
      tuple_params = (x_start, y_start, x_end, y_end)
      cropped = img.crop(tuple_params)
    else: 
      raise ValueError("Incorrect input values")
    return cropped

  # ........................................................................
  
  # f.)
  
  # Opción B
  
  def slice_image(self, X_start=0, Y_start=0, X_end=10, Y_end=10):
    result = Image.fromarray(self._array)
    if  ( X_start < self._width ) and ( Y_start < self._height ):
      if ( X_end + X_start ) < self._width: last_x = X_end + X_start
      else: last_x = self._width
      if ( Y_end + Y_start ) < self._height: last_y = Y_end + Y_start
      else: last_y = self._height
      result = Image.fromarray(self._array[Y_start:last_y, X_start:last_x])
    return result
     
  
  # ------------------------------------------------------------------------

  # g.) Implementa un método que apile dos imágenes horizontal o verticalmente,
  # sin deformarlas. El método debe especificar en sus argumentos qué 
  # dimensiones son las que se deben adaptar. 

  # Opción A

  # This method returns a new image stacked vertically
  # or horizontally according to "position" parameter
  # First parameter: object class ImgNumpy
  # Second parameter: string of value "horizontal" or "vertical"
  def create_stacked_img(self, image, position="vertical"):
    image_result = Image.fromarray(self._array) 
    if position == "vertical":
      image.resize_w(self._width)
      image1 = Image.fromarray(self._array)
      image2 = Image.fromarray(image.array)
      array = np.vstack([image1, image2])
      image_result = Image.fromarray(array)
    elif position == "horizontal":
      image.resize_h(self._height)
      image1 = Image.fromarray(self._array)
      image2 = Image.fromarray(image.array)
      array = np.hstack([image1, image2])
      image_result = Image.fromarray(array)
      pass
    else:
      raise ValueError("Wrong position input") 
    return image_result      
  
  # ........................................................................
  
  # h.)
  # Implementa un método que apile dos imágenes horizontal o  verticalmente, 
  # si las dimensiones de las imágenes no coinciden, debe adaptarlas a la imagen 
  # más ancha o más alta, deformándolas si fuera necesario
  
  def stack_images_deforming(self, img, position = "vertical"):
    result = self.img
    if ( position == "horizontal" ):
      if ( self._height > img.height ): 
        result = self.create_stacked_img(img, "horizontal")
      else:
        result = img.create_stacked_img(self, "horizontal")
    elif ( position == "vertical" ):
      if ( self._width > img.width ): 
        result = self.create_stacked_img(img, "vertical")
      else:
        result = img.create_stacked_img(self, "vertical")    
    else: raise ValueError("Wrong position")
    return result

  # ------------------------------------------------------------------------

  # i.)
  # Implementa un método que inserte una imagen dentro de otra imagen en la 
  # posición horizontal y vertical especificada. 
  # Si la imagen que se va a insertar no cabe entera, debe recortarla.

  # Ejemplo: La primera imagen se inserta en dos imágenes diferentes.
  # En la primera imagen, la posición de inserción especificada no permite 
  # insertar la imágen completa. 
  
  # En la segunda imagen, la posición de inserción permite insertar la 
  # imagen de forma completa.
  def insert_image_force(self, img, x=1, y=1):
    output = self.img
    if ( x >= 0) and  ( y >= 0):
      arr_a = np.copy(self._array)
      arr_b = np.copy(img.array)
      shape_x_a = x + arr_b.shape[0]
      shape_y_a = y + arr_b.shape[1]
      shape_x_b = arr_a.shape[0] - x
      shape_y_b = arr_a.shape[1] - y
      if(shape_x_a > arr_a.shape[0]): shape_x_a = arr_a.shape[0]
      if(shape_y_a > arr_a.shape[1]): shape_y_a = arr_a.shape[1]
      arr_a[x:shape_x_a,y:shape_y_a] = arr_b[0:shape_x_b,0:shape_y_b]
      output = Image.fromarray(arr_a)
    else:
        raise ValueError("Wrong (x, y) inputs")    
    return output

  # ------------------------------------------------------------------------

  # j.)
  # Implementa un método que inserte dentro de una imagen otra imagen
  # en la posición horizontal y vertical especificada con el ancho y el
  # alto especificado. Si la imagen que se vaa insertar no cabe entera,
  # debe recortarla
  def insert_image_redim(self, img, x, y, width, height):
    img_copy = img
    img_copy.width = width
    img_copy.height = height
    return self.insert_image_force(img_copy, x, y)

  # ------------------------------------------------------------------------

  # k.)
  # Implementa un método al que se le pasa el número de elementos horizontales y
  # verticales, así como el ancho y el alto de los elementos horizontales y 
  # verticales y que devuelva la imagen creada con un color de fondo diferente 
  # para cada elemento.

  # Ejemplo: 

  # Imagen con 8 por 8 elementos del mismo ancho y alto e imagen 
  # con 8 por 3 elementos con diferente ancho y alto.
  @staticmethod
  def mosaic(x = 10, y = 10, width = 10, height = 10):
    total_width = x * width
    total_height = y * height
    _data = np.zeros((total_height, total_width, 3), dtype = np.uint8)
    for i in range(0, total_width, width):
        for j in range(0, total_height, height):
            _data[j : j + height, i : i + width] = \
                      (randint(0, 255), randint(0, 255), randint(0, 255))
    return Image.fromarray(_data)

# ------------------------------------------------------------------------

  # Nuevo método: cargar una imagen desde un archivo en nuestro objeto
  # tomamos una imagen. La descomponemos y cambiamos los atributos de 
  # nuestro objeto para que imiten a la imagen.
  def adopt_img_from_file(self, img):
    self._array = np.asarray(img)
    self._height = img.height 
    self._width = img.width
    self._red = 0
    self._green = 0
    self._blue = 0   


# ------------------------------------------------------------------------
# MÉTODO ESTÁTICO
# ------------------------------------------------------------------------
#  Versión estática de 'create_stacked_img'
  
  # This method returns a new image stacked vertically
  # or horizontally according to "position" parameter
  # First and seconds parameters: PIP.Image.Image class
  # Third parameter: string of value "horizontal" or "vertical"
  @staticmethod
  def create_stacked_img_static(img1, img2, position="vertical"):
    image_result = img1
    i = Image.new("RGB", (1,1))
    # Comprobamos que "img1" e "img2" son de la clase 'PIL.Image.Image'
    if (isinstance(img1, (type(i)))) and (isinstance(img2, (type(i)))):
      # Tratamos de unificar el modo de color de las imágenes
      # Sólo trabajamos con el tipo RGB así que intentamos convertir
      # las imágenes de entrada a este formato
      if img1.mode != "RGB":
        try:
          img1 = img1.convert("RGB")
        except ValueError as err:
          print(f"Conversión no permitida {err}, {type(err)}")
        except Exception as err:
          print(f"Error indeterminado {err}, {type(err)}")
          raise
      else: pass
      if img2.mode != "RGB":
        try:
          img2 = img2.convert("RGB")
        except ValueError as err:
          print(f"Conversión no permitida {err}, {type(err)}")
        except Exception as err:
          print(f"Error indeterminado {err}, {type(err)}")
          raise
      else: pass              
      # Comprobación del parámetro de tipo de apilamiento
      if position == "vertical":
        # Se adapta el ancho de la segunda imagen al de la primera
        img2 = img2.resize((img1.width, img2.height))
        image_result = Image.fromarray(np.vstack((np.asarray(img1), np.asarray(img2))))
      elif position == "horizontal":
        # Se adapta el alto de la segunda imagen al de la primera
        img2 = img2.resize((img2.width, img1.height))
        image_result = Image.fromarray(np.hstack((np.asarray(img1), np.asarray(img2))))
      else:
        raise ValueError("Wrong position inputs")
    else:
      raise AttributeError("img1 or img1 are not 'PIL.Image.Image' classes")
    return image_result


# Nuevo en la versión v2.4
# ------------------------------------------------------------------------
# MÉTODO DE CLASE
# ------------------------------------------------------------------------
#  Versión de clase de 'create_stacked_img'
  
  # This method returns a new image stacked vertically
  # or horizontally according to "position" parameter
  # First and seconds parameters: PIP.Image.Image class
  # Third parameter: string of value "horizontal" or "vertical"
  def create_collage(self, list_of_imgs, X, Y):
    image_result = self.img
    img1 = self.img
    
    if(X > 0) and ((X % 2) == 0) and (Y > 0) and ((Y % 2 == 0)) and \
        (len(list_of_imgs) > 0) and (len(list_of_imgs) % 2 == 0): 
        print("funciona")
    else:
        print("no admitido")


    # i = Image.new("RGB", (1,1))
    # # Comprobamos que "img1" e "img2" son de la clase 'PIL.Image.Image'
    # if (isinstance(img1, (type(i)))) and (isinstance(img2, (type(i)))):
    #   # Tratamos de unificar el modo de color de las imágenes
    #   # Sólo trabajamos con el tipo RGB así que intentamos convertir
    #   # las imágenes de entrada a este formato
    #   if img1.mode != "RGB":
    #     try:
    #       img1 = img1.convert("RGB")
    #     except ValueError as err:
    #       print(f"Conversión no permitida {err}, {type(err)}")
    #     except Exception as err:
    #       print(f"Error indeterminado {err}, {type(err)}")
    #       raise
    #   else: pass
    #   if img2.mode != "RGB":
    #     try:
    #       img2 = img2.convert("RGB")
    #     except ValueError as err:
    #       print(f"Conversión no permitida {err}, {type(err)}")
    #     except Exception as err:
    #       print(f"Error indeterminado {err}, {type(err)}")
    #       raise
    #   else: pass              
    #   # Comprobación del parámetro de tipo de apilamiento
    #   if position == "vertical":
    #     # Se adapta el ancho de la segunda imagen al de la primera
    #     img2 = img2.resize((img1.width, img2.height))
    #     image_result = Image.fromarray(np.vstack((np.asarray(img1), np.asarray(img2))))
    #   elif position == "horizontal":
    #     # Se adapta el alto de la segunda imagen al de la primera
    #     img2 = img2.resize((img2.width, img1.height))
    #     image_result = Image.fromarray(np.hstack((np.asarray(img1), np.asarray(img2))))
    #   else:
    #     raise ValueError("Wrong position inputs")
    # else:
    #   raise AttributeError("img1 or img1 are not 'PIL.Image.Image' classes")
    # # Getting result's attributes for self image
    # self._array = np.asarray(image_result)
    # self._height = image_result.shape[0]
    # self._width = image_result.shape[1]
    # self._red = 0
    # self._green = 0
    # self._blue = 0
    