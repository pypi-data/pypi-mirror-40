import h5py
import matplotlib.pyplot as plt
import numpy as np

param_num = 2

#字典！以键值对的方式保存的一种数据结构
def load_dataset():
    #1.创建文件对象
    hdf5_path = 'my_train_data/cat_vs_dog/dataset5000.hdf5'
    train_dataset = h5py.File(hdf5_path,'r')
    test_dataset = h5py.File(hdf5_path,'r')
    #2.读取数据
    train_set_x = np.array(train_dataset["train_img"][:])
    train_set_y = np.array(train_dataset["train_labels"][:])
    test_set_x = np.array(test_dataset["val_img"][:])
    test_set_y = np.array(test_dataset["val_labels"][:])
    plt.figure(figsize=(2,2))
    plt.imshow(train_set_x[610])
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
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*0.01  #
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(1/fc_net[L-1]) #Xavier初始化，针对tanh函数
        parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(2/fc_net[L-1]) #He初始化，针对ReLU函数
        parameters["b"+str(L)] = np.zeros((fc_net[L],1))   
        
    for L in range(1,Layer_num):
        print("W"+str(L)+"=",parameters["W"+str(L)].shape)
        print("b"+str(L)+"=",parameters["b"+str(L)].shape)                       
    return parameters

def init_parameters_momentum(fc_net):
    parameters = {}
    v = {}
    Layer_num = len(fc_net)  
    
    for L in range(1,Layer_num):
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*0.01   #最普通的随机初始化
        parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])* np.sqrt(2/fc_net[L-1])
        parameters["b"+str(L)] = np.zeros((fc_net[L],1))  #使用BN的时候其实可以去掉偏置b了（要在很多代码里面改，先不改了......）
        
        v["dW" + str(L)] = np.zeros((fc_net[L],fc_net[L-1]))
        v["db" + str(L)] = np.zeros((fc_net[L],1))

    for L in range(1,Layer_num):
        print("W"+str(L)+"=",parameters["W"+str(L)].shape)
        print("b"+str(L)+"=",parameters["b"+str(L)].shape)                       
    return parameters,v

def ReLU(Z):
    return np.maximum(0,Z)

def tanh(Z):
    return np.tanh(Z)

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def forward_pass(A0,parameters,active_func="ReLU"):    #前向计算函数
    cache ={}
    A = A0
    cache["A0"] = A0
    Layer_num = len(parameters) // param_num
    for L in range(1,Layer_num): 
        Z = np.dot(parameters["W"+str(L)],A) + parameters["b"+str(L)] 
        if active_func=="sigmoid":
            A = sigmoid(Z)
        elif active_func=="tanh":
            A = tanh(Z)
        else:
            A = ReLU(Z)
        cache["A"+str(L)] = A
        cache["Z"+str(L)] = Z
        
    Z = np.dot(parameters["W"+str(Layer_num)],A) + parameters["b"+str(Layer_num)] #python的广播机制
    A = sigmoid(Z)
    cache["A"+str(Layer_num)] = A
    cache["Z"+str(Layer_num)] = Z
    return A,cache

def compute_cost(AL,Y):
    m = Y.shape[1]   #Y =（1,209）
    cost = (1/m)*np.sum((1/2)*(AL-Y)*(AL-Y)) #代价函数
    return cost

def backward_pass(AL,parameters,cache,Y,active_func="ReLU"):
    m = Y.shape[1]  #样本总数
    gradient = {}   #保存各层参数梯度的字典
    Layer_num = len(parameters) // param_num
    dZL = (AL-Y)*(AL*(1-AL))#获取最末层误差信号 dZL.shape = (1,209)  
    gradient["dW"+str(Layer_num)] = (1/m)*np.dot(dZL,cache["A"+str(Layer_num-1)].T)
    gradient["db"+str(Layer_num)] = (1/m)*np.sum(dZL,axis=1,keepdims = True)    
    for L in reversed(range(1,Layer_num)): #遍历[3,2,1]，其中reversed函数[1,2,3]颠倒为[3,2,1]
        if active_func=="sigmoid":
            dZL = np.dot(parameters["W"+str(L+1)].T,dZL)*(cache["A"+str(L)]*(1-cache["A"+str(L)]))  #dsigmoid/dz  = a*(1-a)
        elif active_func=="tanh":
            dZL = np.dot(parameters["W"+str(L+1)].T,dZL)*(1-np.power(cache["A"+str(L)],2))#dtanh/dz  = 1-a^2
        else:
            dZL = np.dot(parameters["W"+str(L+1)].T,dZL)* np.array(cache["Z"+str(L)]>0) 
        
        gradient["dW"+str(L)] = (1/m)*np.dot(dZL,cache["A"+str(L-1)].T)
        gradient["db"+str(L)] = (1/m)*np.sum(dZL,axis=1,keepdims = True)        
    return gradient

def update_parameters_with_momentum(gradient,parameters,LearnRate,v,momentum=0.9):
    Layer_num = len(parameters) // param_num
    for L in range(1,Layer_num+1): #遍历[1,2,3,4]
        #["dW" + str(L)] = momentum * v["dW" + str(L)] + (1 - momentum) * gradient["dW" + str(L)]
        v["dW" + str(L)] = momentum * v["dW" + str(L)] + gradient["dW" + str(L)]
        parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*v["dW"+str(L)]
        #["db" + str(L)] = momentum * v["db" + str(L)] + (1 - momentum) * gradient["db" + str(L)]
        v["db" + str(L)] = momentum * v["db" + str(L)] + gradient["db" + str(L)]
        parameters["b"+str(L)] = parameters["b"+str(L)] - LearnRate*v["db"+str(L)]
    return parameters,v

def update_parameters(gradient,parameters,LearnRate):
    #w:=w-lr*dw  ;   b:=b-lr*db
    Layer_num = len(parameters) // param_num
    for L in range(1,Layer_num+1): #遍历[1,2,3,4]
        parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*gradient["dW"+str(L)]
        parameters["b"+str(L)] = parameters["b"+str(L)] - LearnRate*gradient["db"+str(L)]   
    return parameters
              
def Train_Net(fc_net,train_set_x,train_set_y,check=False,iterations=2000,LearnRate=0.01,active_func="ReLU"):
    #4.初始化参数
    #arameters = init_parameters(fc_net)  
    parameters,v = init_parameters_momentum(fc_net)
    costs = [] 
    for iteration in range(0,iterations):
        AL,cache= forward_pass(train_set_x,parameters,active_func) #AL=(1,209)
        #6.计算代价值
        cost = compute_cost(AL,train_set_y)         
        if iteration%500 == 0: 
            print("iteration = ",iteration,";    cost = ",cost)
            costs.append(cost)
        #7.反向传播计算梯度
        gradient = backward_pass(AL,parameters,cache,train_set_y,active_func)
        #8.根据梯度更新一次参数
        #arameters = update_parameters(gradient,parameters,LearnRate)
        parameters,v = update_parameters_with_momentum(gradient,parameters,LearnRate,v)
           
    plt.plot(costs,'r')
    plt.xlabel("iteration")
    plt.ylabel("cost")
    plt.show()
    return parameters

def Predict(A0,Y,parameters,active_func):
    AL,_ = forward_pass(A0,parameters,active_func)#AL是（1,50）
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
    print("train_set_x.shape=",train_set_x.shape,"    train_set_y.shape=",train_set_y.shape)
    print("test_set_x.shape=",test_set_x.shape,"    test_set_y.shape=",test_set_y.shape)

    #2.对输入像素值做归一化（0~255）->(0~1)
    train_set_x = train_set_x/255.
    test_set_x = test_set_x/255.
    #3.定义全连接神经网络各层神经元个数，并初始化参数w和b
    fc_net = [12288,10,3,2,1]       #四层网络（梯度消失）
    #4.开始训练
    parameters = Train_Net(fc_net,train_set_x,train_set_y,iterations=3001,LearnRate=0.1,active_func="ReLU") 
    #5.开始预测
    print("===Predict Train Set ===")
    Predict(train_set_x,train_set_y,parameters,active_func="ReLU")
    print("===Predict Test Set ===")
    Predict(test_set_x,test_set_y,parameters,active_func="ReLU")
    
    
    
#把数据重新打乱顺序，进行输入，可以让数据更加具备典型性和更优良的泛化能力！
#对输入顺序进行随机化处理是为了保证能够有监督学习，同时使算法按照梯度下降法则进行学习。
#假如训练数据是有序的，那么会导致训练结果很难收敛到偏置值。只有保证数据的随机性才能使得BP算法训练结果尽可能地收敛。  
#打乱数据集:要确保特征和标签都被同步地重新排列。
"""
这来自于信息理论（Information Theory）——“学习到一件不太可能发生的事却发生了，比学习一件很可能发生的事已经发生，包含更多的信息。”同样的，
把训练样例的顺序随机化（在不同周期，或者 mini-batch），会导致更快的收敛。如果模型看到的很多样例不在同一种顺序下，运算速度会有小幅提升。

"""
def random_mini_batches(X, Y, mini_batch_size = 64):
    m = X.shape[1]                  # number of training examples
    mini_batches = []        
    # Step 1: 打乱数据集
    permutation = list(np.random.permutation(m))#获取0~m-1的随机排列数,这些随机排列数作为列索引，就能把batch打乱了（必要的步骤）
    shuffled_X = X[:, permutation] 
    shuffled_Y = Y[:, permutation].reshape((1,m))
    # Step 2: 分组 (shuffled_X, shuffled_Y)
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, k * mini_batch_size : (k+1) * mini_batch_size]
        mini_batch_Y = shuffled_Y[:, k * mini_batch_size : (k+1) * mini_batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)  
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[:, (k+1) * mini_batch_size :]
        mini_batch_Y = shuffled_Y[:, (k+1) * mini_batch_size :]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)    
    return mini_batches
    
#8001   cost =  0.000935400328228   accuracy = 0.76 (gd+relu)
#8001   cost =  0.000540447819058   accuracy = 0.72 (momentum+relu)->数据量太少，过拟合

#iteration =  7000 ;    cost =  0.000439735530467  accuracy = 0.70 (gd+relu)
#7001   cost =  0.0290159490925   accuracy = 0.62 (momentum+relu)   
#多次试验，在本例中，gd和momentum各有胜负，可能是数据量太小，看不出太明显的区别来
import time
start =time.clock()

#中间写上代码块

end = time.clock()
print('Running time: %s Seconds'%(end-start))














def update_parameters_with_momentum(gradient,parameters,LearnRate,v,momentum=0.9):
    Layer_num = len(parameters) // 2
    for L in range(1,Layer_num+1): #遍历[1,2,3,4]
        #["dW" + str(L)] = momentum * v["dW" + str(L)] + (1 - momentum) * gradient["dW" + str(L)]
        v["dW" + str(L)] = momentum * v["dW" + str(L)] + gradient["dW" + str(L)]
        parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*v["dW"+str(L)]
        #["db" + str(L)] = momentum * v["db" + str(L)] + (1 - momentum) * gradient["db" + str(L)]
        v["db" + str(L)] = momentum * v["db" + str(L)] + gradient["db" + str(L)]
        parameters["b"+str(L)] = parameters["b"+str(L)] - LearnRate*v["db"+str(L)]
    return parameters,v
	
def init_parameters_momentum(fc_net):
    parameters = {}
    v = {}
    Layer_num = len(fc_net)     
    for L in range(1,Layer_num):
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*0.01   #最普通的随机初始化
        parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])* np.sqrt(2/fc_net[L-1])
        parameters["b"+str(L)] = np.zeros((fc_net[L],1))  #使用BN的时候其实可以去掉偏置b了（要在很多代码里面改，先不改了......）     
        v["dW" + str(L)] = np.zeros((fc_net[L],fc_net[L-1]))
        v["db" + str(L)] = np.zeros((fc_net[L],1))
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
        #parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(1/fc_net[L-1]) #Xavier初始化，针对tanh函数
        parameters["W"+str(L)] = np.random.randn(fc_net[L],fc_net[L-1])*np.sqrt(2/fc_net[L-1]) #He初始化，针对ReLU函数
        parameters["b"+str(L)] = np.zeros((fc_net[L],1))     
        s["dW"+str(L)] = np.zeros((fc_net[L],fc_net[L-1]))
        s["db"+str(L)] = np.zeros((fc_net[L],1))           
    for L in range(1,Layer_num):
        print("W"+str(L)+"=",parameters["W"+str(L)].shape)
        print("b"+str(L)+"=",parameters["b"+str(L)].shape)                       
    return parameters,s

	
def update_parameters_with_RMSProp(gradient,parameters,LearnRate,s,decay=0.9,eps=1e-8):
    #w:=w-lr*dw  ;   b:=b-lr*db
    Layer_num = len(parameters) // 2
    for L in range(1,Layer_num+1): #遍历[1,2,3,4]
        s["dW"+str(L)] = decay*s["dW"+str(L)] + (1-decay)*(gradient["dW"+str(L)]**2)    
        parameters["W"+str(L)] = parameters["W"+str(L)] - LearnRate*gradient["dW"+str(L)]/np.sqrt(s["dW"+str(L)]+eps)
        s["db"+str(L)] = decay*s["db"+str(L)] + (1-decay)*(gradient["db"+str(L)]**2)
        parameters["b"+str(L)] = parameters["b"+str(L)] - LearnRate*gradient["db"+str(L)]/np.sqrt(s["db"+str(L)]+eps)
    return parameters,s
