import clang.cindex as cc

def explore(node: cc.Cursor, indent = ''):
    '''
    expand the ast 
    '''
    for i in node.get_children():
        print(indent, i.kind, i.spelling, i.displayname)
        explore(i, indent+'  ')