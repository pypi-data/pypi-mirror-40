def print_lol(the_list,level=0):
    """这个函数有一个位置参数，名为“the_list”,
        这可以是任何Python列表（包含或不包含嵌套列表），
        所提供列表中的各个数据项会(递归地)打印到屏幕上，而且各占一行。
        第二个参数（名为"level"）用来在遇到嵌套列表时插入制表符。
        为了将一个函数的必要参数变成可选的参数，需要为这个参数提供
        一个缺少值。方法是在参数名后面指定这个缺省值，使得这个
        参数level成为可选参数。"""
    #书本P83,92
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
            """增加level参数的目的就是为了能控制嵌套输出。
                每次处理一个嵌套列表时，都需要将level的值增1。"""
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
