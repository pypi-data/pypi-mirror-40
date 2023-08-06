#fc_net = [12288,40,40,40,40,1] 
#交叉熵：迭代6001次，学习率0.01（适合），除了第一层，其它层随着层级递增，a值向0聚拢，同样使得梯度消失
#交叉熵：加入BN后，迭代6001次，学习率0.01（适合），随着层级递增，分布都很均匀，有利于训练！  

#交叉熵：迭代6001次，学习率0.5（过大），随着迭代次数增多，第一层激活值会趋于1和-1（激活函数梯度趋于0） ---->z值向0的两侧扩散，梯度消失
#交叉熵：加入BN后，迭代6001次，学习率0.5（过大），随着迭代次数增多，第一层激活值会缓慢趋于1和-1 ---->z值向0的两侧扩散，梯度消失有所减缓
import time
    start = time.clock()
    parameters = Train_Net(fc_net,train_set_x,train_set_y,iterations=200,LearnRate=0.5,bn_mode="train",use_bn=False,active_func="tanh")
    end = time.clock()
    print ("time cost=",end-start,"s")







import h5py
import matplotlib.pyplot as plt
import numpy as np

#字典！以键值对的方式保存的一种数据结构
def load_dataset():
    #1.创建文件对象
    train_dataset = h5py.File('./我的数据集/train_catvnoncat.h5','r')
    test_dataset = h5py.File('./我的数据集/test_catvnoncat.h5','r')
    #2.读取数据
    train_set_x = np.array(train_dataset["train_set_x"][:])
    train_set_y = np.array(train_dataset["train_set_y"][:])
    test_set_x = np.array(test_dataset["test_set_x"][:])
    test_set_y = np.array(test_dataset["test_set_y"][:])
    plt.figure(figsize=(2,2))
    plt.imshow(train_set_x[110])
    plt.show()
    #3.变化维度以适应神经网络输入
    #(209, 64, 64, 3) -> (12288,209)
    train_set_x = train_set_x.reshape(train_set_x.shape[0],-1).T  #(12288,209)
    test_set_x = test_set_x.reshape(test_set_x.shape[0],-1).T  #(12288,209)
    #(209,)->(1,209)
    train_set_y = train_set_y.reshape(1,train_set_y.shape[0]) #(1,209)
    test_set_y = test_set_y.reshape(1,test_set_y.shape[0]) #(1,209)
    
    return train_set_x,train_set_y,test_set_x,test_set_y

def init_parameters(fc_net):
    parameters = {}
    Layer_num = len(fc_net) #Layer_num=5    
    for L in range(1,Layer_num):
        parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*0.01   #最普通的随机初始化
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])* np.sqrt(1/fc_net[L-1])
        parameters["b"+str(L)] = np.zeros((fc_net[L],1))  #使用BN的时候其实可以去掉偏置b了（要在很多代码里面改，先不改了......）
        parameters["gamma"+str(L)] = np.ones((fc_net[L],1))   
        parameters["beta"+str(L)] = np.zeros((fc_net[L],1))   
        parameters["running_mean"+str(L)] = np.zeros((fc_net[L],1))   
        parameters["running_std"+str(L)] = np.zeros((fc_net[L],1))         
    for L in range(1,Layer_num):
        print("W"+str(L)+"=",parameters["W"+str(L)].shape)
        print("b"+str(L)+"=",parameters["b"+str(L)].shape)                       
    return parameters

def init_parameters_momentum(fc_net):
    parameters = {}
    Layer_num = len(fc_net) #Layer_num=5 
    v = {}
    for L in range(1,Layer_num):
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*0.01  #
        parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(1/fc_net[L-1]) #Xavier初始化，针对tanh函数
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(2/fc_net[L-1]) #He初始化，针对ReLU函数
        parameters["b"+str(L)] = np.zeros((fc_net[L],1))     
        v["dW"+str(L)] = np.zeros((fc_net[L],fc_net[L-1]))
        v["db"+str(L)] = np.zeros((fc_net[L],1))           
    for L in range(1,Layer_num):
        print("W"+str(L)+"=",parameters["W"+str(L)].shape)
        print("b"+str(L)+"=",parameters["b"+str(L)].shape)                       
    return parameters,v

def init_parameters_RMSProp(fc_net):
    parameters = {}
    Layer_num = len(fc_net) #Layer_num=5 
    s = {}
    for L in range(1,Layer_num):
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*0.01  #
        parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(1/fc_net[L-1]) #Xavier初始化，针对tanh函数
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(2/fc_net[L-1]) #He初始化，针对ReLU函数
        parameters["b"+str(L)] = np.zeros((fc_net[L],1))     
        s["dW"+str(L)] = np.zeros((fc_net[L],fc_net[L-1]))
        s["db"+str(L)] = np.zeros((fc_net[L],1))           
    for L in range(1,Layer_num):
        print("W"+str(L)+"=",parameters["W"+str(L)].shape)
        print("b"+str(L)+"=",parameters["b"+str(L)].shape)                       
    return parameters,s

def ReLU(Z):
    return np.maximum(0,Z)

def tanh(Z):
    return np.tanh(Z)

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def BN_forward(Z,bn_mode,parameters,L,epsilon=1e-9,mu=0.9):
    gamma,beta = parameters["gamma"+str(L)],parameters["beta"+str(L)]
	Z_mean,Z_std = np.zeros((Z.shape[0],1)),np.zeros((Z.shape[0],1))  
    Z_normed,Z_out = np.zeros(Z.shape),np.zeros(Z.shape)
     
    if bn_mode == 'train':       
        Z_mean = np.mean(Z, axis=1, keepdims=True)#计算均值  
        Z_std = np.std(Z, axis=1, keepdims=True)  #计算标准差  
        Z_normed = (Z - Z_mean) / (Z_std + epsilon)  #归一化  
        Z_out = gamma * Z_normed + beta    #重构变换
        parameters["running_mean"+str(L)] = mu * parameters["running_mean"+str(L)] + (1 - mu) * Z_mean
        parameters["running_std"+str(L)] = mu * parameters["running_std"+str(L)] + (1 - mu) * Z_std
    elif bn_mode == 'test':        
        Z_normed = (Z - parameters["running_mean"+str(L)]) / (parameters["running_std"+str(L)] + epsilon)
        Z_out = gamma * Z_normed + beta
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)
    return Z_out,Z_mean,Z_std,Z_normed,parameters

def BN_backward(dZ,bn_cache,parameters,L,epsilon=1e-9):
    m = dZ.shape[1] #样本数
    Z_mean,Z_std,Z_normed = bn_cache["Z_mean"+str(L)],bn_cache["Z_std"+str(L)],bn_cache["Z_normed"+str(L)]
    gamma,beta = parameters["gamma"+str(L)],parameters["beta"+str(L)]  
    dgamma = np.sum(dZ * Z_normed,axis=1, keepdims=True)            
    dbeta = np.sum(dZ,axis=1, keepdims=True)
    dZ_out = (gamma/(Z_std+epsilon)) * (dZ - dgamma*Z_normed/m - np.mean(dZ,axis=1,keepdims=True))
    return dZ_out, dgamma, dbeta

def forward_pass(A0,parameters,bn_mode,use_bn=True,active_func="ReLU"):    #前向计算函数
    cache = {}
    bn_cache = {}
    A = A0
    cache["A0"] = A0
    Layer_num = len(parameters) // 6 #写成/2代表精确除法，得到一个浮点数，写成//2代表向下取整除法，得到一个整数
   
    for L in range(1,Layer_num): #遍历[1,2,3]
        #1.求和
        if use_bn:
            Z = np.dot(parameters["W"+str(L)],A)
        else:
            Z = np.dot(parameters["W"+str(L)],A) + parameters["b"+str(L)]
        
        #2.批归一化
        if(use_bn):
            Z, Z_mean, Z_std, Z_normed,parameters = BN_forward(Z,bn_mode,parameters,L)
            bn_cache["Z_mean"+str(L)] = Z_mean
            bn_cache["Z_std"+str(L)] = Z_std
            bn_cache["Z_normed"+str(L)] = Z_normed
        #3.激活
        if active_func=="sigmoid":
            A = sigmoid(Z)
        elif active_func=="tanh":
            A = tanh(Z)
        else:
            A = ReLU(Z)
        cache["A"+str(L)] = A
        cache["Z"+str(L)] = Z
        
    Z = np.dot(parameters["W"+str(Layer_num)],A) + parameters["b"+str(Layer_num)] 
    A = sigmoid(Z)
    cache["A"+str(Layer_num)] = A
    cache["Z"+str(Layer_num)] = Z
    return A,cache,bn_cache,parameters


def compute_cost(AL,Y):
    m = Y.shape[1]   #Y =（1,209）
    cost = - np.sum(  Y * np.log(AL) + (1 - Y) * np.log(1 - AL)  ) / m  #交叉熵
    #cost = (1/m)*np.sum((1/2)*(AL-Y)*(AL-Y)) #代价函数
    return cost

def backward_pass(AL,parameters,cache,bn_cache,Y,use_bn=False,active_func="ReLU"):
    m = Y.shape[1]  #样本总数
    gradient = {}   #保存各层参数梯度的字典
    Layer_num = len(parameters) // 6
    dZL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL)) * AL*(1-AL)  #交叉熵代价函数dZ
    #dZL = (AL-Y)*(AL*(1-AL))#获取最末层误差信号 dZL.shape = (1,209)  #最后一层无需做BN处理
    gradient["dW"+str(Layer_num)] = (1/m)*np.dot(dZL,cache["A"+str(Layer_num-1)].T)
    gradient["db"+str(Layer_num)] = (1/m)*np.sum(dZL,axis=1,keepdims = True)    
    for L in reversed(range(1,Layer_num)): #遍历[3,2,1]，其中reversed函数[1,2,3]颠倒为[3,2,1]
        if active_func=="sigmoid":
            dZL = np.dot(parameters["W"+str(L+1)].T,dZL)*(cache["A"+str(L)]*(1-cache["A"+str(L)]))  
        elif active_func=="tanh":
            dZL = np.dot(parameters["W"+str(L+1)].T,dZL)*(1-np.power(cache["A"+str(L)],2))#dtanh/dz  = 1-a^2
        else:
            dZL = np.dot(parameters["W"+str(L+1)].T,dZL)* np.array(cache["Z"+str(L)]>0)           
        if(use_bn):
            dZL, dgamma, dbeta = BN_backward(dZL,bn_cache,parameters,L)
            gradient["dgamma"+str(L)] = dgamma
            gradient["dbeta"+str(L)] = dbeta       
        gradient["dW"+str(L)] = (1/m)*np.dot(dZL,cache["A"+str(L-1)].T)
        if use_bn==False:
            gradient["db"+str(L)] = (1/m)*np.sum(dZL,axis=1,keepdims = True)    
    return gradient

def update_parameters(gradient,parameters,LearnRate,use_bn=False):
    Layer_num = len(parameters) // 6
    if(use_bn):
        for L in range(1,Layer_num): #遍历[1,2,3] ,因为最后一层不做BatchNormalization
            parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*gradient["dW"+str(L)]
            parameters["gamma"+str(L)] = parameters["gamma"+str(L)] - LearnRate*gradient["dgamma"+str(L)]
            parameters["beta"+str(L)] = parameters["beta"+str(L)] - LearnRate*gradient["dbeta"+str(L)]  
        parameters["W"+str(Layer_num)] = parameters["W"+str(Layer_num)] - LearnRate*gradient["dW"+str(Layer_num)]
        parameters["b"+str(Layer_num)] = parameters["b"+str(Layer_num)] - LearnRate*gradient["db"+str(Layer_num)]  
    else:
        for L in range(1,Layer_num+1): #遍历[1,2,3,4]
            parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*gradient["dW"+str(L)]
            parameters["b"+str(L)] = parameters["b"+str(L)] - LearnRate*gradient["db"+str(L)]  
    return parameters

def update_parameters_with_momentum(gradient,parameters,LearnRate,v,momentum=0.9):
    #w:=w-lr*dw  ;   b:=b-lr*db
    Layer_num = len(parameters) // 6
    for L in range(1,Layer_num+1): #遍历[1,2,3,4]
        v["dW"+str(L)] = momentum*v["dW"+str(L)] + gradient["dW"+str(L)]   
        parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*v["dW"+str(L)]
        v["db"+str(L)] = momentum*v["db"+str(L)] + gradient["db"+str(L)] 
        parameters["b"+str(L)] = parameters["b"+str(L)] - LearnRate*v["db"+str(L)]
    return parameters,v

def update_parameters_with_RMSProp(gradient,parameters,LearnRate,s,decay=0.9,esp=1e-8):
    #w:=w-lr*dw  ;   b:=b-lr*db
    Layer_num = len(parameters) // 6
    for L in range(1,Layer_num+1): #遍历[1,2,3,4]
        s["dW"+str(L)] = decay*s["dW"+str(L)] + (1-decay)*gradient["dW"+str(L)]**2  
        parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*gradient["dW"+str(L)]/np.sqrt(s["dW"+str(L)]+esp)
        s["db"+str(L)] = decay*s["db"+str(L)] + (1-decay)*gradient["db"+str(L)]**2 
        parameters["b"+str(L)] = parameters["b"+str(L)] - LearnRate*gradient["db"+str(L)]/np.sqrt(s["db"+str(L)]+esp)
    return parameters,s


def cut_data(train_set_x,train_set_y,batch_size=64):
    m = train_set_x.shape[1]
    #1.打乱数据集
    permutation=list(np.random.permutation(m))
    X_shuffled = train_set_x[:,permutation]
    Y_shuffled = train_set_y[:,permutation]
    
    train_set_cutted=[]
    #2.分批
    num_batch = m//batch_size  #3
    
    for i in range(num_batch):
        mini_batch_X = X_shuffled[:,i*batch_size:(i+1)*batch_size]
        mini_batch_Y = Y_shuffled[:,i*batch_size:(i+1)*batch_size]
        mini_batch = (mini_batch_X,mini_batch_Y)
        train_set_cutted.append(mini_batch)
        
    if m%batch_size!=0:
        mini_batch_X = X_shuffled[:,(i+1)*batch_size:]
        mini_batch_Y = Y_shuffled[:,(i+1)*batch_size:]
        mini_batch = (mini_batch_X,mini_batch_Y)
        train_set_cutted.append(mini_batch)
        
    return train_set_cutted
            
    
def Train_Net(fc_net,train_set_x,train_set_y,batch_size,check=False,num_epoch=500,
                          LearnRate=0.01,active_func="ReLU",optimizer="SGD",use_bn=False,bn_mode="train"):
    #4.初始化参数
    if(optimizer=="momentum"):    
        parameters,v = init_parameters_momentum(fc_net)
    elif(optimizer=="RMSProp"):
        parameters,s = init_parameters_RMSProp(fc_net)
    else:
        parameters = init_parameters(fc_net)
    costs = []
    for epoch in range(0,num_epoch):
        train_set_cutted = cut_data(train_set_x,train_set_y,batch_size)
        for minibatch in train_set_cutted:#遍历所有批次，每一个批次都更新一次参数，从而加快收敛速度
            mini_batch_X,mini_batch_Y = minibatch
            AL,cache,bn_cache,parameters= forward_pass(mini_batch_X,parameters,bn_mode,use_bn,active_func) 
            #6.计算代价值
            cost = compute_cost(AL,mini_batch_Y)         
            if epoch%500 == 0: 
                print("epoch = ",epoch,";    cost = ",cost)
                costs.append(cost)
            #7.反向传播计算梯度
            gradient = backward_pass(AL,parameters,cache,bn_cache,mini_batch_Y,use_bn,active_func)
            #8.根据梯度更新一次参数
            if(optimizer=="momentum"):    
                parameters,v = update_parameters_with_momentum(gradient,parameters,LearnRate,v)
            elif(optimizer=="RMSProp"):
                parameters,s = update_parameters_with_RMSProp(gradient,parameters,LearnRate,s)
            else:
                parameters = update_parameters(gradient,parameters,LearnRate,use_bn)

    plt.plot(costs,'r')
    plt.xlabel("iteration")
    plt.ylabel("cost")
    plt.show()
    return parameters

def Predict(A0,Y,parameters,active_func,bn_mode="test",use_bn=True):
    AL,_0,_1,_2 = forward_pass(A0,parameters,bn_mode,use_bn,active_func)
    m = AL.shape[1]
    p = np.zeros(AL.shape)
    for i in range(0,AL.shape[1]):
        if AL[0,i]>0.5:
            p[0,i]=1
        else:
            p[0,i]=0           
    accuracy = (1/m)* np.sum(p==Y)
    print("accuracy =",accuracy)
            
    
if __name__ == '__main__':
    #1.加载数据
    train_set_x,train_set_y,test_set_x,test_set_y = load_dataset()
    #2.对输入像素值做归一化（0~255）->(0~1)
    train_set_x = train_set_x/255.
    test_set_x = test_set_x/255.
    #3.定义全连接神经网络各层神经元个数，并初始化参数w和b
    #fc_net = [12288,10,3,2,1]  
    fc_net = [12288,20,20,20,20,1] 
    #4.开始训练   #考虑到计算机硬件结构，一般把batch_size设置为16、32、64、128、256，可以加快计算速度  #False True
    parameters = Train_Net(fc_net,train_set_x,train_set_y,batch_size=64,num_epoch=6001,LearnRate=0.01,
                               active_func="tanh",optimizer="SGD",use_bn=True) 
    #5.开始预测
    print("===predict train_set===")
    Predict(train_set_x,train_set_y,parameters,active_func="tanh",use_bn=True)
    print("===predict test_set===")
    Predict(test_set_x,test_set_y,parameters,active_func="tanh",use_bn=True)
    
    

    

    



    