#!/usr/bin/env python
# coding: utf-8

# ## 衍生变量的选择
# ### 根据变量的预测能力 ---- IV

# * IV值越大，预测能力越强，分箱效果也就越好
# $$IV = \sum^n_{n=1}IV_i =  \sum^n_{n=1}(p_{yi}-p_{ni}\times WOE_i$$
# $$WOE_i = ln(\frac{p_{yi}}{p_{ni}}) = ln(\frac{y_i/y_T}{n_i/n_T})$$
# * WOE 越大，该分组的样本响应的可能性也就越大

# In[ ]:


import numpy as np
import pandas as pd
import math

def compute_woe_iv(path,var_list,Y_flag):
'''
path = 'modeldata.csv'
var_list = ['x1','x2','x3','x4','x5','x6']
Y_flag = 'ifgood'
'''

    df = pd.read_csv(path, header=0)
    var_num = len(var_list)
    totalG_B = df.groupby([Y_flag])[Y_flag].count()  # 计算正负样本多少个
    G = totalG_B[1]
    B = totalG_B[0]
    woe_all = np.zeros((1, 8))
    var_iv = np.zeros((var_num))
    data_index = []
    for k in range(0, var_num):
        var1 = df.groupby([var_list[k]])[Y_flag].count()  # 计算col每个分组中的组的个数
        var_class = var1.shape[0]
        woe = np.zeros((var_class, 8))
        woe_pre = pd.DataFrame(data={'x1': [], 'ifgood': [],'values' : []})
        total = df.groupby([var_list[k], Y_flag])[Y_flag].count()  # 计算该变量下每个分组响应个数
        total1 = pd.DataFrame({'total': total})
        mu = []
        for u,group in df.groupby([var_list[k], Y_flag])[Y_flag]:
            mu.append(list(u))
        print(mu)
        for lab1 in total.index.levels[0]:
            for lab2 in total.index.levels[1]:
                print(lab1,lab2)
                # temporary = pd.DataFrame(data={'x1': [lab1], 'ifgood': [lab2], 'values': [1]})
                if [lab1,lab2] not in mu:
                    temporary = pd.DataFrame(data={'x1': [lab1], 'ifgood': [lab2], 'values' : [0]})
                else:
                    temporary = pd.DataFrame(data={'x1': [lab1], 'ifgood': [lab2], 'values' : [total1.xs((lab1, lab2)).values[0]]})
                woe_pre = pd.concat([woe_pre, temporary])
            #print(woe_pre)
        woe_pre.set_index(['x1','ifgood'], inplace=True)
        print(woe_pre)

        # 计算 WOE
        for i in range(0, var_class):   #var_class
            woe[i,0] = woe_pre.values[2 * i + 1]
            woe[i,1] = woe_pre.values[2 * i]
            woe[i,2] = woe[i,0] + woe[i,1]
            woe[i, 3] = woe_pre.values[2 * i + 1] / G  # pyi
            woe[i, 4] = woe_pre.values[2 * i] / B  # pni
            abb = lambda i:(math.log(woe[i, 3] / woe[i, 4])) if woe[i, 3] != 0 else 0 # 防止 ln 函数值域报错 
            woe[i, 5] = abb(i)
            woe[np.isinf(woe)] = 0  #将无穷大替换为0，参与计算 woe 计算

            woe[i, 6] = (woe[i, 3] - woe[i, 4]) * woe[i, 5]  # iv_part
            var_iv[k] += woe[i, 6]
        iv_signal = np.zeros((1,8))
        iv_signal[0,7] =var_iv[k]
        woe_all = np.r_[woe_all, woe,iv_signal]
        index_var = df.groupby([var_list[k]])[Y_flag].count()
        u = index_var.index.values.tolist()
        data_index += u
        data_index += [var_list[k]]
    woe_all = np.delete(woe_all,0,axis=0)
    result = pd.DataFrame(data = woe_all,columns=['good', 'bad', 'class_sum','pyi','pni','woe','iv_part','iv'])
    result.index = data_index
    
    result.to_csv("data.csv")
    return {print(result)}

path = 'modeldata.csv'
var_list = ['x1','x2','x3','x4','x5','x6']
Y_flag = 'ifgood'

print(compute_woe_iv(path,var_list,Y_flag))

