import pandas as pd
import argparse
from pathlib import Path
import numpy as np
from keras.callbacks import LearningRateScheduler, ModelCheckpoint
from keras.optimizers import SGD, Adam
from keras.utils import np_utils
from wideresnet import WideResNet
from utils import load_data, load_adience_data, load_imdb, image_generator
from keras.preprocessing.image import ImageDataGenerator
from mixup_generator import MixupGenerator


def get_random_eraser(p=0.5, s_l=0.02, s_h=0.4, r_1=0.3, r_2=1 / 0.3, v_l=0, v_h=255):
    def eraser(input_img):
        img_h, img_w, _ = input_img.shape
        p_1 = np.random.rand()

        if p_1 > p:
            return input_img

        while True:
            s = np.random.uniform(s_l, s_h) * img_h * img_w
            r = np.random.uniform(r_1, r_2)
            w = int(np.sqrt(s / r))
            h = int(np.sqrt(s * r))
            left = np.random.randint(0, img_w)
            top = np.random.randint(0, img_h)

            if left + w <= img_w and top + h <= img_h:
                break

        c = np.random.uniform(v_l, v_h)
        input_img[top:top + h, left:left + w, :] = c

        return input_img

    return eraser


class Schedule:
    def __init__(self, nb_epochs, initial_lr):
        self.epochs = nb_epochs
        self.initial_lr = initial_lr

    def __call__(self, epoch_idx):
        if epoch_idx < self.epochs * 0.25:
            return self.initial_lr
        elif epoch_idx < self.epochs * 0.50:
            return self.initial_lr * 0.2
        elif epoch_idx < self.epochs * 0.75:
            return self.initial_lr * 0.04
        return self.initial_lr * 0.008


def get_optimizer(opt_name, lr):
    if opt_name == "sgd":
        return SGD(lr=lr, momentum=0.9, nesterov=True)
    elif opt_name == "adam":
        return Adam(lr=lr)
    else:
        raise ValueError("optimizer name should be 'sgd' or 'adam'")


input_path = '/run/user/1000/gvfs/smb-share:server=192.168.43.124,share=project_phase2/wiki/wiki.mat'
batch_size = 12
nb_epochs = 100
lr = 1e-1
opt_name = 'adam'
depth = 16
k = 3
validation_split = 10
use_augmentation = True
output_path = 'models'
# output_path = Path(__file__).resolve().parent.joinpath('models')
# output_path.mkdir(parents=True, exist_ok=True)

print("Loading data...")

# image, gender, age, _, image_size, _ = load_data(input_path)
# image, gender, age, _, image_size, _ = load_data(input_path)
# image, gender, age, _, image_size, _ = load_adience_data()

# image, gender, age, _, image_size, _ = load_data(input_path)

# X_data = image
# y_data_g = np_utils.to_categorical(gender, 2)
# y_data_a = np_utils.to_categorical(age, 101)

train_path = '/run/user/1000/gvfs/smb-share:server=192.168.43.124,share=project_phase2/data/train/'
test_path = '/run/user/1000/gvfs/smb-share:server=192.168.43.124,share=project_phase2/data/test/'


traindata = image_generator(train_path, batch_size=52)
testdata = image_generator(test_path,  batch_size=52)
# y_data_a = np_utils.to_categorical(age, 81)
image_size = 62
model = WideResNet(image_size, depth=depth, k=k)()
opt = get_optimizer(opt_name, lr)
model.compile(optimizer=opt, loss=["categorical_crossentropy", "categorical_crossentropy"],
              metrics=['accuracy'])

print("Model summary...")
model.count_params()
model.summary()

callbacks = [LearningRateScheduler(schedule=Schedule(nb_epochs, lr)),
             ModelCheckpoint(str(output_path) + "/weights.{epoch:02d}-{val_loss:.2f}.hdf5",
                             monitor="val_loss",
                             verbose=1,
                             save_best_only=True,
                             mode="auto")
             ]

print("Running training...")

# data_num = len(X_data)
# train_num = int(data_num * (1 - validation_split))
# train_last_elem = int(data_num - (data_num * 0.3))

# datagen = ImageDataGenerator(
#     width_shift_range=0.1,
#     height_shift_range=0.1,
#     horizontal_flip=True,
#     preprocessing_function=get_random_eraser(v_l=0, v_h=255))
#
# training_generator = MixupGenerator(np.array(X_data[0:train_last_elem]),
#                                     [np.array(y_data_g[0:train_last_elem]), np.array(y_data_a[0:train_last_elem])],
#                                     batch_size=batch_size, alpha=0.2,
#                                     datagen=datagen)()

hist = model.fit_generator(generator=traindata,
                           steps_per_epoch=100,
                           validation_steps=100//52,
                           validation_data=testdata,
                           epochs=nb_epochs, verbose=1,
                           callbacks=callbacks)


# training_generator = MixupGenerator(X_train, [y_train_g, y_train_a], batch_size=batch_size, alpha=0.2,
#                                     datagen=datagen)()
# hist = model.fit_generator(generator=training_generator,
#                            steps_per_epoch=train_num // batch_size,
#                            validation_data=(X_test, [y_test_g, y_test_a]),
#                            epochs=nb_epochs, verbose=1,
#                            callbacks=callbacks)

pd.DataFrame(hist.history).to_hdf(output_path.joinpath("history_{}_{}.h5".format(depth, k)), "history")
