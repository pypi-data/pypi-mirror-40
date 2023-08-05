'''这是film模块，它包含一个函数：print_l01(),打印列表，列表可能还包含列表，
如果out为可写入的文件，函数就把内容打印到文件'''
import sys

'''该函数接收一个列表，把列表项逐一打印出来'''
def print_l01(the_list,ident=False,level=0,out=sys.stdout):
    for film in the_list:
        if isinstance(film,list):
            print_l01(film,ident,level+1,out)
        else:
            if ident:
                for tab in range(level):
                    print("\t",end='',file=out)
            print(film,file=out)
