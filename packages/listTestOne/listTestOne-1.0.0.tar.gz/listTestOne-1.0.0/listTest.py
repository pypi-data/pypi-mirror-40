#coding:utf-8
'''这是"listTest.py"模块，提供了一个名为printItem()的函数，
这个函数的作用是打印列表（支持打印嵌套列表）。'''

def printItem(the_list,indent=False,level=0):
    '''这个函数取一个位置参数，名为：the_list,这可以是任何python列表。
indent的值控制是否缩进，level控制缩进的\t个数
所指定的列表中的每个数据项会递归输出到屏幕上，各数据项各占一行。'''
    for item in the_list:
        if isinstance(item,str) or isinstance(item,int) or isinstance(item,float):
            if indent:
                print(level*'\t',end='')
            print(item)
        elif isinstance(item,dict):
            if indent:
                for key,value in item.items():
                    print(level*'\t',end='')
                    print(key+':'+str(value))
            else:
                for key,value in item.items():
                    print(key+':'+str(value))
        else:
            printItem(item,indent,level+1)
        

        
    

