import tensorflow as tf
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.training import moving_averages
import math

def batch_norm(x, scope_name, is_training=True):
    """Batch normalization."""
    with tf.variable_scope(scope_name):

        params_shape = [x.get_shape()[-1]]

        beta = tf.get_variable(
               'beta', params_shape, tf.float32,
                initializer=tf.constant_initializer(0.0, tf.float32))
        gamma = tf.get_variable(
                'gamma', params_shape, tf.float32,
                initializer=tf.constant_initializer(1.0, tf.float32))
        # 求滑动均值方差
        moving_mean = tf.get_variable(
                      'moving_mean', params_shape, tf.float32,
                      initializer=tf.constant_initializer(0.0, tf.float32),
                      trainable=False)
        moving_variance = tf.get_variable(
                      'moving_variance', params_shape, tf.float32,
                      initializer=tf.constant_initializer(1.0, tf.float32),
                      trainable=False)

        # these ops will only be performed when training.
        mean, variance = tf.nn.moments(x, [0, 1, 2], name='moments')

         # 求滑动平均值
        update_moving_mean = moving_averages.assign_moving_average(
                             moving_mean, mean, 0.9)
        update_moving_variance = moving_averages.assign_moving_average(
                             moving_variance, variance, 0.9)

        tf.add_to_collection("UPDATE_OPS_COLLECTION", update_moving_mean)
        tf.add_to_collection("UPDATE_OPS_COLLECTION", update_moving_variance)

        mean, variance = control_flow_ops.cond(is_training, lambda:(mean, variance), lambda:(moving_mean, moving_variance))

        # epsilon used to be 1e-5. Maybe 0.001 solves NaN problem in deeper net.
        y = tf.nn.batch_normalization(x, mean, variance, beta, gamma, 0.001)
        y.set_shape(x.get_shape())
        return y

def create_variables(name, shape, weight_decay, initializer=tf.contrib.layers.xavier_initializer(), is_fc_layer=False):
    '''
    :param name: A string. The name of the new variable
    :param shape: A list of dimensions
    :param initializer: User Xavier as default.
    :param is_fc_layer: Want to create fc layer variable? May use different weight_decay for fc
    layers.
    :return: The created variable
    '''

    # TODO: to allow different weight decay to fully connected layer and conv layer
    if is_fc_layer is True:
        regularizer = tf.contrib.layers.l2_regularizer(scale=weight_decay)
    else:
        regularizer = tf.contrib.layers.l2_regularizer(scale=weight_decay)

    new_variables = tf.get_variable(name, shape=shape, initializer=initializer,
                                    regularizer=regularizer, trainable=True)
    return new_variables


# 池化，大小k*k
def max_pool(x, k_size=(2, 2), stride=(2, 2), pad = 'VALID'):
    return tf.nn.max_pool(x, ksize=[1, k_size[0], k_size[1], 1],
                          strides=[1, stride[0], stride[1], 1], padding=pad)


def ave_pool(x, k_size=(2, 2), stride=(2, 2), pad = 'VALID'):
    return tf.nn.avg_pool(x, ksize=[1, k_size[0], k_size[1], 1],
                          strides=[1, stride[0], stride[1], 1], padding=pad)


def Bin_conv(img, weight, strides=1):
    w, h, in_size, out_size = weight.get_shape().as_list()
    B = tf.sign(weight)
    alpha = tf.div(tf.reduce_sum(abs(weight), [0, 1]), w * h)
    B_alpha = tf.multiply(B, alpha)          # 刚好对应位置相乘
    conv_img = tf.nn.conv2d(img, B_alpha, strides=[1, strides, strides, 1], padding='SAME')
    return conv_img


def hard_tanh(img):
    active_img = tf.maximum(tf.minimum(img, 1), -1)
    return active_img


# Bit_count operation:统计二进制表达式中”1“的个数  bit运算的kernel
def Bit_count(A, B):
    # 判断多维数组对应元素是否相等  tf.cast 保证A B精度相等  XNOR运算
    C = tf.equal(tf.cast(A, tf.int8), tf.cast(B, tf.int8))
    count = tf.reduce_sum(tf.to_float(C))
    return count


def XNOR_convolutional(img, weight, strides=1):
    w, h, in_channel, out_channel = weight.get_shape().as_list()
    _, w_in, h_in, img_channel = img.get_shape().as_list()
    pad_w = math.ceil((w_in/strides-1)*strides + w - w_in)   # math.ceil  向上取整
    pad_h = math.ceil((h_in/strides - 1) * strides + h - h_in)
    assert in_channel == img_channel
    conv_img = img
    batch_list = []
    conv_out = tf.nn.conv2d(img, weight, strides=[1, strides, strides, 1], padding='SAME')
    conv_conv = tf.div(tf.add(conv_out, tf.ones_like(conv_out) * (w**2)), 2)
    # for ii in range(batch_size):
    #     output_list = []
    #     for pp in range(out_channel):
    #         sum_img = []
    #         for qq in range(in_channel):
    #             each_img = []
    #             for jj in range(0, w_in, strides):
    #                 for kk in range(0, h_in, strides):
    #                     print(pp, qq, jj, kk)
    #                     if w == 1:
    #                         padding = conv_img[ii, :, :, qq]
    #                     else:
    #                         # print(ii, pp, qq, jj, kk, int(pad_w/2), int(pad_w-int(pad_w/2)))
    #                         padding = tf.pad(conv_img[ii, :, :, qq], paddings=[[int(pad_w/2), int(pad_w-int(pad_w/2))], [int(pad_h/2), int(pad_h-int(pad_h/2))]])
    #                     B = Bit_count(padding[jj:jj + w, kk:kk + h], weight[:, :, qq, pp])
    #                     each_img.append(B)
    #             sum_img.append(each_img)
    #         output_list.append(tf.reduce_sum(sum_img, 0))
    #     batch_list.append(output_list)
    # con_out = tf.stack(batch_list)                          # [batch_size, out_size, weight, height]
    # reshape_out = tf.reshape(con_out, [batch_size,  out_channel, w_in, h_in])
    # out_img = tf.transpose(reshape_out, perm=[0, 2, 3, 1])   # 转置为标准维度顺序[batch_size, weight, height , out_channel]
    return conv_conv


def XNOR_Active(img, weight, strides=1):   # img [batch_size, w, h, channel]
    batch_size, w_in, h_in, in_channel = img.get_shape().as_list()
    w, h, _, _ = weight.get_shape().as_list()
    # c = tf.constant(in_channel)
    A = tf.reduce_sum(abs(img), [3])
    A = tf.cast(tf.div(A, in_channel), tf.float32)
    k_weight = tf.ones([w, h])*(1/(w*h))  # tf.constant(1/(w*h), )
    K = tf.nn.conv2d(tf.expand_dims(A, 3), tf.expand_dims(tf.expand_dims(k_weight, 2), 3), strides=[1, strides, strides, 1], padding="SAME")
    I = tf.sign(img)
    return I, K  # [batch_size, w_in, h_in, in_channel], [batch_size, w_in, h_in, 1]
