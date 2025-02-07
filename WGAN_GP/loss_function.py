import numpy as np
import tensorflow as tf

def gradient_penalty(Discriminator, reals, fakes):
    batch_size = len(reals)

    with tf.GradientTape() as tape:
        epsilon = tf.random.uniform(shape = (batch_size,1,1,1))
        epsilon = tf.tile(epsilon, [1,64,64,3])
        tf_reals = tf.Variable(reals, dtype = float)
        tf_fakes = tf.Variable(fakes)
        inter_images = tf.multiply(tf_reals,epsilon) + tf.multiply(tf_fakes,1-epsilon)
        mixed_score = Discriminator(inter_images, training = True)
        grad = tape.gradient(mixed_score, inter_images)
        grad = tf.norm(grad, 2)
        grad = tf.reduce_mean((grad - 1) ** 2)
    return grad

def WGAN_loss_D(obj):
    ans = tf.reduce_mean(obj.Discriminator(obj.reals, training = True)) - tf.reduce_mean(obj.Discriminator(obj.fakes, training = True))
    ans = ans - obj.lamda * gradient_penalty(obj.Discriminator, obj.reals, obj.fakes)
    return -ans

def WGAN_loss_G(y_pred):
    ans = tf.reduce_mean(y_pred)
    return -ans