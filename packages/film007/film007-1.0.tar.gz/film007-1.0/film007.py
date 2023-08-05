'''这是film模块，它包含一个函数：print_l01(),打印影片信息,影片信息存储在列表里，列表中可能还包含列表'''

movies = ["The Holy Grail",["Graham",1975,"TerryJones and Terry",91,["Michael Palin","John Cless","Terry Gilliam","Eric ldle and TerryJones"]]]

'''该函数接收一个列表，把列表项逐一打印出来'''
def print_l01(the_list,level=0):
    for film in the_list:
        if isinstance(film,list):
            print_l01(film,level+1)
        else:
            for tab in range(level):
                print("\t",end='')
            print(film)
