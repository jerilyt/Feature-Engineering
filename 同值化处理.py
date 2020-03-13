#!/usr/bin/env python
# coding: utf-8

# ## 删除维度占比过大值过高的比例的函数

# In[ ]:


def primaryvalue_ratio(data, ratiolimit = 1):
    #按照命中率进行筛选      
    #首先计算每个变量的命中率,这个命中率是指 维度中占比最大的值的占比       
    recordcount = data.shape[0]
    x = []
    #循环每一个列，并取出出现频率最大的那个值;index[0]是取列名,iloc[0]是取列名对应的值
    for col in data.columns:
        primaryvalue = data[col].value_counts().index[0]
        ratio = float(data[col].value_counts().iloc[0])/recordcount
        x.append([ratio,primaryvalue])       
    feature_primaryvalue_ratio = pd.DataFrame(x,index = data.columns)
    feature_primaryvalue_ratio.columns = ['primaryvalue_ratio','primaryvalue']

    needcol = feature_primaryvalue_ratio[feature_primaryvalue_ratio['primaryvalue_ratio']<ratiolimit]
    needcol = needcol.reset_index()
    select_data = data[list(needcol['index'])]
    return select_data   

