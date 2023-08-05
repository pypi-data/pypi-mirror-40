from __future__ import division        # for 1/2=0.5
import numpy as np


def Batch_Normalization(batch_data, gamma=1, beta=0):
    mean = np.mean(batch_data)
    std = np.std(batch_data)
    # Use adjusted standard deviation here, in case the std == 0.
    # std = np.max([np.std(batch_data), 1.0/np.sqrt(batch_data.shape[1]*batch_data.shape[2]*batch_data.shape[3])])
    batch_norm_data = (batch_data - mean) / std
    return gamma*batch_norm_data + beta


def Batch_Normalization_derivative(batch_data, gamma, beta, der):   # der 是上层求得的二维矩阵残差  输入x也是一个矩阵
    dim_1 = batch_data.shape[0]
    dim_2 = batch_data.shape[1]
    m = dim_1*dim_2
    epo = 10**(-6)
    mean = np.mean(batch_data)
    std = np.std(batch_data)
    var = std**2
    batch_norm_data = (batch_data - mean) / std
    der_gamma = sum(sum(batch_norm_data*der))
    der_beta = sum(sum(der))
    der_var = gamma * (-0.5) * (var ** (-(3 / 2))) * sum(sum(der * (batch_data - mean)))
    der_batch_norm_data = der * gamma
    der_mean = sum(sum(der_batch_norm_data)) * (-1) / np.sqrt(var + epo) + der_var * (-2 / m) * sum(sum(batch_data - mean))
    der_batch_data = der_batch_norm_data*(1/np.sqrt(var + epo)) + der_var*(2/m)*(batch_data - mean) + der_mean*(1/m)
    return der_gamma, der_beta, der_batch_data


def convolve(image, kernel):       # image, kernel 都是二维矩阵(不一定是正方形)  stride = 1
    (iH, iW) = image.shape[:2]
    (kH, kW) = kernel.shape[:2]
    output = np.zeros((iH-kH+1, iW-kW+1), dtype="float32")
    for y in np.arange(0, iH-kH+1):
        for x in np.arange(0, iW-kW+1):
            roi = image[y:y+kH, x:x+kW]
            k = (np.array(roi)*np.array(kernel)).sum()
            output[y, x] = k
    return output


def sigmoid(x):
    return 1./(1+np.exp(-x))


def ReLu(x):
    if x < 0:
        return 0
    else:
        return x


def sigmoid_derivative(x):     # sigmoid(x)的导数
    return (1./(1+np.exp(-x)))*(1-(1./(1+np.exp(-x))))


def ReLu_derivative(x):        # ReLu(x)的导数
    if x < 0:
        return 0
    else:
        return 1


def ave_pooling(image, p_size, stride):         # 最好是简单的可以整除  p_size =[2, 2] stride = 2
    (iH, iW) = image.shape[:2]
    (kH, kW) = p_size
    out = np.zeros((int(iH/stride), int(iW/stride)))     # 输入输出的大小关系
    for ii in range(0, iH, stride):
        for jj in range(0, iW, stride):                 # 相当于和np.ones((2,2))做卷积
            out[int(ii/stride), int(jj/stride)] = image[ii:(ii+kH), jj:(jj+kW)].sum()
    return out/4


def max_pooling(image, p_size, stride):
    (iH, iW) = image.shape[:2]
    (kH, kW) = p_size
    out = np.zeros((int(iH/stride), int(iW/stride)))     # 输入输出的大小关系
    for ii in range(0, iH, stride):
        for jj in range(0, iW, stride):                 # 相当于和np.ones((2,2))做卷积
            out[int(ii/stride), int(jj/stride)] = np.amax(image[ii:(ii+kH), jj:(jj+kW)])
    return out


def expand(inputs, stride):  # 二维矩阵
    (w, h) = inputs.shape
    out = np.zeros((w*stride, h*stride))
    for ii in range(0, w*stride, stride):
        for jj in range(0, h*stride, stride):
            out[ii:(ii + stride), jj:(jj+stride)] = inputs[int(ii/2), int(jj/2)]*np.ones((stride, stride))
    return out


def deconvolution(image, weight):    # 残差和卷积核得到上一层残差   in: [8, 8] [5, 5] out :[12, 12]
    (iH, iW) = image.shape[:2]
    (kH, kW) = weight.shape[:2]
    image_exp = np.zeros((iH+2*(kH-1), iW+2*(kW-1)))
    image_exp[4:12, 4:12] = image
    out = convolve(image_exp, weight)
    return out

def one_hot(batch_label, class_num):            # label 是batch  class_num 是分类数  输出one_hot的label
    length = batch_label.shape[0]
    Class_list = [kk for kk in range(class_num)]
    out_label = np.zeros((length, class_num))
    for kk in range(length):
        out_label[kk, Class_list.index(int(batch_label[kk]))] = 1.0
    return out_label


def one_hot_to_index(batch_label):
    batch_size, class_num = batch_label.shape
    out_label = []
    for kk in range(batch_size):
        out_label.append(np.argmax(batch_label[kk]))
    return out_label


def Sign(x):
    if x < 0:
        return -1
    else:
        return 1


def Sign_derivative(x):
    if abs(x) > 1:
        return 0
    else:
        return 1


def hard_sigmoid(x):
    return max(0, min(1, (x + 1)/2))


def hard_sigmoid_derivative(x):
    if abs(x) <= 1:
        return 1./2
    else:
        return 0


def hard_tanh(x):
    x = np.array(x)
    shape = len(x.shape)
    assert shape < 3
    out = np.zeros_like(x)
    if shape == 1:
        dim_1 = x.shape[0]
        for ii in range(dim_1):
            out[ii] = max(-1, min(1, x[ii]))
    if shape == 2:
        dim_1 = x.shape[0]
        dim_2 = x.shape[1]
        for ii in range(dim_1):
            for jj in range(dim_2):
                out[ii, jj] = max(-1, min(1, x[ii, jj]))
    return out   # 2*hard_sigmoid(x) - 1


def hard_tanh_derivative(x):
    x = np.array(x)
    shape = len(x.shape)
    assert shape < 4
    out = np.zeros_like(x)
    if shape == 1:
        if abs(x) <= 1:
            return 1
        else:
            return 0
    if shape == 3:
        dim_1 = x.shape[0]
        dim_2 = x.shape[1]
        dim_3 = x.shape[2]
        for ii in range(dim_1):
            for jj in range(dim_2):
                for kk in range(dim_3):
                    if abs(x[ii, jj, kk]) <= 1:
                        out[ii, jj, kk] = 1
                    else:
                        out[ii, jj, kk] = 0
        return out


def bin_function(x):   # 输入x可以是一维、二维、三维
    x = np.array(x)
    shape = len(x.shape)
    assert shape < 4
    output = np.ones_like(x)
    dim_1 = x.shape[0]
    if shape == 1:
        for ii in range(dim_1):
            if hard_sigmoid(x[ii]) < 0.5:
                output[ii] = -1
    if shape == 2:
        dim_2 = x.shape[1]
        for ii in range(dim_1):
            for jj in range(dim_2):
                if hard_sigmoid(x[ii, jj]) < 0.5:
                    output[ii, jj] = -1
    elif shape == 3:
        dim_2 = x.shape[1]
        dim_3 = x.shape[2]
        for ii in range(dim_1):
            for jj in range(dim_2):
                for kk in range(dim_3):
                    if hard_sigmoid(x[ii, jj, kk]) < 0.5:
                        output[ii, jj, kk] = -1
    return output


def Binary_weight(x):     # x是二维矩阵
    n_1 = x.shape[0]
    n_2 = x.shape[1]
    # print(n_1, n_2)
    B_new = np.zeros_like(x)
    alpha = 0
    for ii in range(n_1):
        for jj in range(n_2):
            B_new[ii, jj] = Sign(x[ii, jj])
            alpha += abs(x[ii, jj])
    alpha = alpha/(n_1*n_2)
    return alpha, B_new


def Softmax(x):
    sum_exp = 0
    for t in x:
        sum_exp += np.exp(t)
    return [np.exp(f)/sum_exp for f in x]


def Leaky_ReLu(x):
    if x < 0:
        return 0.001*x
    else:
        return x


def Data_augmentation(x):     # x 是标准输入：[batch_size, weight, height, depth]
    data_out = np.zeros_like(x)
    for ii in range(x.shape[0]):
        rot = np.random.randint(4)    # 旋转一定角度
        for jj in range(x.shape[3]):
            data_out[ii, :, :, jj] = np.rot90(x[ii, :, :, jj], rot)
    return data_out
