import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from keras.layers import Flatten, Dense
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator , img_to_array, load_img 
from keras.applications.mobilenet import MobileNet, preprocess_input
from keras.losses import categorical_crossentropy


# Working with pre trained model
base_model = MobileNet( input_shape=(224,224,3), include_top= False )
for layer in base_model.layers:
    layer.trainable = False
    x = Flatten()(base_model.output)
    x = Dense(units=7 , activation='softmax' )(x)


# creating our model.
model = Model(base_model.input, x)


#compile the model
model.compile(optimizer='adam', loss= categorical_crossentropy , metrics=['accuracy'] )


#preparing our data using DataGenerator
train_datagen = ImageDataGenerator( zoom_range = 0.2,shear_range = 0.2, horizontal_flip=True,rescale = 1./255)
train_data = train_datagen.flow_from_directory(directory= "Train",target_size=(224,224), batch_size=32,)
train_data.class_indices


#scaling the images
val_datagen = ImageDataGenerator(rescale = 1./255 )
val_data = val_datagen.flow_from_directory(directory= "Test",target_size=(224,224), batch_size=32,)




#visualizing the data that is fed to train data gen
# to visualize the images in the training data generator
t_img , label = train_data.next()
#-----------------------------------------------------------------------------
# function when called will prot the images 
"""
input :- images array output :- plots the images """
def plotImages(img_arr, label):
    count = 0
    for im, l in zip(img_arr,label) :
        plt.imshow(im)
        plt.title(im.shape) 
        plt.axis = False 
        plt.show()
        count += 1
        if count == 10:
            break
#-----------------------------------------------------------------------------
 
# function call to plot the images
plotImages(t_img, label)


## having early stopping and model check point
from keras.callbacks import ModelCheckpoint, EarlyStopping
# early stopping
es = EarlyStopping(monitor='val_accuracy', min_delta= 0.01 , patience= 5, verbose= 1, mode='auto')
# model check point
mc = ModelCheckpoint(filepath="best_model.h5", monitor= 'val_accuracy', verbose= 1, save_best_only= True, mode = 'auto')
# puting call back in a list
call_back = [es, mc]


# fitting the train_data in to model
hist = model.fit_generator(train_data,steps_per_epoch= 10,epochs= 30, validation_data= val_data, validation_steps= 8, callbacks=[es,mc])

# Loading the best fit model
from keras.models import load_model
model = load_model("content/best_model.h5") 
h = hist.history
h.keys()


#plotting the training accuracy plt.plot(h['accuracy']) plt.plot(h['val_accuracy'] , c = "red") plt.title("acc vs v-acc")
plt.show()


#plotting the training loss
 
plt.plot(h['loss'])
plt.plot(h['val_loss'] , c = "red") 
plt.title("loss vs v-loss") 
plt.show()

# just to map o/p values
op = dict(zip( train_data.class_indices.values(), train_data.class_indices.keys()))


# path for the image to see if it predicts correct class
path = "Train/Happy/Happy.jpeg"
img = load_img(path, target_size=(224,224) ) 
i = img_to_array(img)/255
input_arr = np.array([i]) 
input_arr.shape
pred = np.argmax(model.predict(input_arr)) 
print(f" the image is of {op[pred]}")

# to display the image R
plt.imshow(input_arr[0]) 
plt.title("input image") 
plt.show()

