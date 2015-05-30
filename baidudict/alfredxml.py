# coding=utf-8
__author__ = 'Philip'



#生成XML文件
def genElement(lists):
    assert(len(lists)%3==0)
    name = lists[0]         # 节点名
    params = lists[1]      # 节点属性list
    content = lists[2]      # 节点内容 ， 可能是String 或者是包含其他Element.
    string = ''
    string +="<%s"%name + '' # 以下为解析XML List的过程

    for k,v in params.items():    # 枚举属性
        string+= " %s = \"%s\" " %(k,v)

    if(isinstance(content, str)):   # 通过递归 解析子节点
        text = content
    else:
        text = genElement(content)
    string +=">" + text + "</%s>\n"%name

    if(len(lists)<=3):  # 通过递归， 解析同级节点
        return string
    else:
        return string + genElement(lists[3:])

def genAlfredXML(rowList):  # 生成alfred所需要的XML String.
    item = []
    for row in rowList:
        tsi = ['title',{},row['title'],'subtitle',{},row['subtitle'],'icon',{},row['icon']]
        item.extend(['item',{'uid':row['uid'],'arg':row['arg'],'autocomplete':row['autocomplete']},tsi])
    items = ['items',{},item]
    return genElement(items)

if __name__=='__main__':
    rowList = [{'uid':'123321','arg':'argsx','autocomplete':'autocompletex','icon':'icon','subtitle':'subtitle','title':'title'}]
    element = genAlfredXML(rowList)

    print(element)
