# -*- coding: utf-8 -*-

"""
Author: Zhou Zhi-Jian
Institution: Hunan University
Email: zjzhou@hnu.edu.cn
Copyright：Copyright (c) Zhou Zhi-Jian
Time: 2020/12/14 16:45
LICENSE：GNU General Public License v3.0
"""
import os              # 导入设置路径的库
import pandas as pd    # 导入数据处理的库

def seq_filter(seqfile_path,date_other_file_path,condition_list,outfile_path):

    seq_file = open(seqfile_path, "r")    # 标准fasta格式序列

    seq_list =[]

    for line in seq_file:
        line = line.strip()   # 去掉首尾制表符、空格、换行符
        seq_list.append(line)   # 把输入文件里的每一行都存入到列表中，一行即一个元素

    seq_file.close()
    n = len(seq_list)

    # 将序列数据储存入数据框
    seq_datatab  = pd.DataFrame(columns = ["name", "sequence"])

    for i in range(int(n / 2)):
        seq_name = seq_list[2 * i].replace(">","")
        seq = (seq_list[2 * i + 1]).upper()
        new_line = pd.DataFrame({"name": seq_name,"sequence": seq},index=[i+1])  # index：自定义索引

        seq_datatab = seq_datatab.append(new_line)

    # print(seq_datatab["name"].tolist())  # 获取name列并转换为列表


    # 读取日期（或日期+地点）文件
    date_file = open(date_other_file_path, "r")

    date_list = []

    for line in date_file:
        line = line.strip()     # 去掉首尾制表符、空格、换行符
        date_list.append(line)

    date_file.close()
    date_date = []

    for x in range(1,len(date_list)):
        label_list = date_list[x].split("\t")
        date_date.append(label_list)

    date_tab = pd.DataFrame(date_date)
    date_tab.columns = date_list[0].split("\t")  # 设置列名

    column1 = date_list[0].split("\t")[0]  # 获取date_tab第一列的名称

    # 设置成“category”数据类型
    date_tab[column1] = date_tab[column1].astype("category")

    # inplace = True，使 reorder_categories生效(如果list元素多，需要使用使用set_categories）
    date_tab[column1].cat.reorder_categories(seq_datatab["name"].tolist(), inplace=True)  # 按照序列的名称顺序对时间文件进行排序

    # inplace = True，使 df生效
    date_tab.sort_values(column1, inplace=True)

    # print(date_tab)

    # 给seq_datatab数据框增加列

    my_datatbl = seq_datatab

    date_tab_cloums = date_list[0].split("\t")

    for n in range(1,len(date_tab_cloums)):
        my_datatbl[date_tab_cloums[n]] = date_tab[date_tab_cloums[n]].tolist()

    # print(my_datatbl)

    condition_list.append("sequence")

    new_datatbl = my_datatbl.drop_duplicates(subset=condition_list) # 根据指定的多列去重

    #输出结果
    out = open(outfile_path,"w")
    for row in new_datatbl.itertuples():

        out.write(">" + getattr(row, 'name') + "\n" + getattr(row, 'sequence') + "\n")

    out.close()


# 注意，上面已经为封装的函数，代码不需要改动，只需要调节下面这里

seq_file = r"C:\Users\j\Desktop\Test_seq.fasta"  # 序列文件路径，要求为标准fasta格式序列

date_file = r"C:\Users\j\Desktop\Test_date.txt" # 日期文件（或者日期加地点文件）路径

out_file = r"C:\Users\j\Desktop\out.fasta"  # 输出文件路径

label_list = ["date"]  # 指定筛选列表。如果需要剔除 相同采集时间+相同地点 的同一性100%序列，设置为["date","location"]

seq_filter(seq_file,date_file,label_list,out_file)