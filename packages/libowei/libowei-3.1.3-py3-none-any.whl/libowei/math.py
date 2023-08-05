import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import rfft
from sklearn import preprocessing
from mpl_toolkits.mplot3d import axes3d
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
np.set_printoptions(suppress=True)
# np.random.seed(0)

def Fourier_transform(data,precision=10,pi=3.141592653589793):
    n = len(data)
    t = np.linspace(0, pi * 2, n)
    M=max(data)
    m=min(data)

    ft=rfft(data)
    y=abs(ft)/n*2
    phase=np.angle(ft)+pi/2

    #系数矩阵处理
    coef_mat=np.vstack((y,np.arange(len(y)),phase))
    #权重排序
    coef_mat=coef_mat.T[np.lexsort(-coef_mat[0,None])].T
    coef_mat=coef_mat[:,:precision]
    print("系数矩阵\n",coef_mat)

    fit_y=[]
    for i in t:
        s=sum(coef_mat[0]*np.sin(coef_mat[1]*i+coef_mat[2]))
        fit_y.append(s)

    fig=plt.figure(figsize=(14,10))
    plt.subplot(211)
    plt.plot(t,data,label="原始数据")
    scaler=preprocessing.MinMaxScaler(feature_range=(m,M))
    fit_y=scaler.fit_transform(np.array(fit_y).reshape(n,1)).reshape(1,n)[0]
    plt.plot(t,fit_y,color="red",label="拟合数据")
    plt.legend()

    ax = fig.add_subplot(223,projection='3d')
    dx,dy = np.array(coef_mat[1])/20,np.array(coef_mat[2])/20
    ax.bar3d(coef_mat[1],coef_mat[2],0,dx,dy,coef_mat[0])
    ax.set_xlabel("频率",color="red"),ax.set_ylabel("相位",color="red"),ax.set_zlabel("振幅",color="red")
    ax.set_title("离散傅里叶变换\n频谱/相位图\n")

    plt.subplot(224)
    func = "拟合公式\nY=\n"
    for coef in coef_mat.T:
        func = func + "%s*sin(%s*X+(%s))+\n" % (coef[0], coef[1], coef[2])
    print(func)
    func = func + "\n\nn=输入数据长度(采样数据数量)\nk=采样数据下标\nX(k)=2*pi/n*(k-1)"
    plt.text(.2,.2,func)
    plt.show()
    return coef_mat