from PIL import Image
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Reshape, Input, Dropout, Conv2D, UpSampling2D, BatchNormalization, Activation, Flatten, LeakyReLU, ZeroPadding2D
from tqdm import tqdm
import os
import gc
import sys
import numpy as np
import matplotlib.pyplot as plt
class GenAdvNet:
    def __init__(self,image_width,image_height,channels,label):
        self.image_width = image_width
        self.image_height = image_height

        self.channels = channels

        self.label = label

        self.image_shape = (self.image_height,self.image_width,self.channels)

        self.random_noise_dimension = 100

        optimizer = Adam(0.0002,0.5)

        self.discriminator = self.build_discriminator(0.25)
        self.discriminator.compile(loss="binary_crossentropy",optimizer=optimizer,metrics=["accuracy"])
        self.generator = self.build_generator()

        random_input = Input(shape=(self.random_noise_dimension,))

        generated_image = self.generator(random_input)

        self.discriminator.trainable = False

        validity = self.discriminator(generated_image)

        self.combined = Model(random_input,validity)
        self.combined.compile(loss="binary_crossentropy",optimizer=optimizer)

    def get_training_data(self,datafolders):
        print("Loading training data...")
        over_training_data = []
        for datafolder in datafolders:
            training_data = []
            filenames = os.listdir(datafolder)
            for filename in tqdm(filenames):
                try:
                    path = os.path.join(datafolder,filename)
                    image = Image.open(path)
                    image = image.resize((self.image_width,self.image_height),Image.ANTIALIAS)
                    pixel_array = np.asarray(image)
                    if (pixel_array.shape[-1] >= self.image_shape[-1]+1):
                        pixel_array = pixel_array[:,:,:self.image_shape[-1]]
                    training_data.append(pixel_array)
                except Exception as e:
                    print(e)
            training_data = np.array(training_data)
            training_data = np.reshape(training_data,(-1,self.image_height,self.image_width,self.channels))
            Image.fromarray(training_data[0]).save("examp.png")
            over_training_data+=list(training_data)
        return np.array(over_training_data)


    def build_generator(self):
        model = Sequential()
        layerCount = 3 #number of UpSamplings in the model
        shapemodA = int(self.image_width/(2**layerCount))
        shapemodB = int(self.image_height/(2**layerCount))
        model.add(Dense(256*shapemodA*shapemodB,activation="relu",input_dim=self.random_noise_dimension))
        model.add(Reshape((shapemodB,shapemodA,256)))

        model.add(UpSampling2D())
        model.add(Conv2D(256,kernel_size=3,padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))

        model.add(UpSampling2D())
        model.add(Conv2D(256,kernel_size=3,padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))

        model.add(UpSampling2D())
        model.add(Conv2D(128,kernel_size=3,padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))
        """
        model.add(UpSampling2D())
        model.add(Conv2D(128,kernel_size=3,padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))
        """

        model.add(Conv2D(self.channels,kernel_size=3,padding="same"))
        model.add(Activation("tanh"))

        model.summary()

        input = Input(shape=(self.random_noise_dimension,))
        generated_image = model(input)

        return Model(input,generated_image)


    def build_discriminator(self,dropRate):
        model = Sequential()

        model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=self.image_shape, padding="same"))
        model.add(LeakyReLU(alpha=0.2))

        model.add(Dropout(dropRate))
        model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
        model.add(ZeroPadding2D(padding=((0,1),(0,1))))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))

        model.add(Dropout(dropRate))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))

        model.add(Dropout(dropRate))
        model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        """
        model.add(Dropout(dropRate))
        model.add(Conv2D(512, kernel_size=3, strides=1, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        """
        model.add(Dropout(dropRate))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))

        model.summary()

        input_image = Input(shape=self.image_shape)

        validity = model(input_image)

        return Model(input_image, validity)

    def train(self, datafolders,epochs,batch_size,save_images_interval,save_model_interval):
        training_data = self.get_training_data(datafolders)
        print("Training Data Loaded")
        print("about to process training data")
        gc.collect()
        training_data = (training_data / 127.5) - 1
        print("Training Data Processed")
        print("about to label images")
        labels_for_real_images = np.ones((batch_size,1))
        labels_for_generated_images = np.zeros((batch_size,1))
        print("Ready to train")
        for epoch in range(epochs):
            indices = np.random.randint(0,training_data.shape[0],batch_size)
            real_images = training_data[indices]

            random_noise = np.random.normal(0,1,(batch_size,self.random_noise_dimension))
            generated_images = self.generator.predict(random_noise)

            discriminator_loss_real = self.discriminator.train_on_batch(real_images,labels_for_real_images)
            discriminator_loss_generated = self.discriminator.train_on_batch(generated_images,labels_for_generated_images)
            discriminator_loss = 0.5 * np.add(discriminator_loss_real,discriminator_loss_generated)

            generator_loss = self.combined.train_on_batch(random_noise,labels_for_real_images)
            print ("%d [Discriminator loss: %f, acc.: %.2f%%] [Generator loss: %f]" % (epoch, discriminator_loss[0], 100*discriminator_loss[1], generator_loss))

            if epoch % save_images_interval == 0:
                self.save_images(epoch)
            if epoch % save_model_interval == 0:
                self.generator.save_weights("saved_models/facegenerator_" + self.label + str(epoch) + ".hdf5")
                self.discriminator.save_weights("saved_models/facediscriminator_" + self.label + str(epoch) + ".hdf5")
        self.generator.save_weights("saved_models/facegenerator"+self.label+".hdf5")
        self.discriminator.save_weights("saved_models/facediscriminator"+self.label+".hdf5")


    def save_images(self,epoch):
        rows, columns = 5, 5
        noise = np.random.normal(0, 1, (rows * columns, self.random_noise_dimension))
        generated_images = self.generator.predict(noise)

        generated_images = 0.5 * generated_images + 0.5

        figure, axis = plt.subplots(rows, columns)
        image_count = 0
        for row in range(rows):
            for column in range(columns):
                axis[row,column].imshow(generated_images[image_count, :], cmap='spring')
                axis[row,column].axis('off')
                image_count += 1
        figure.savefig("gan/images/generated_%d.png" % epoch)
        plt.close()
    def load_weighting(self,gen_path,disc_path):
        self.generator.load_weights(gen_path)
        self.discriminator.load_weights(disc_path)
    def generate_single_image(self,image_save_path):
        noise = np.random.normal(0,1,(1,self.random_noise_dimension))
        model = self.generator
        generated_image = model.predict(noise)
        generated_image = (generated_image+1)*127.5
        print(generated_image)
        generated_image = np.reshape(generated_image,self.image_shape)

        image = Image.fromarray(generated_image,"RGB")
        image.save(image_save_path)