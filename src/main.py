import sys
import clang.cindex as cc
from utils import *

FILE = sys.argv[1]
index = cc.Index.create()
translation_unit = index.parse(FILE)


def count_global_variables(tu):
    global_variable_count = 0
    
    for node in tu.cursor.walk_preorder():
        is_global_variable = (
            node.kind == cc.CursorKind.VAR_DECL and 
            node.is_definition() and 
            (node.storage_class == cc.StorageClass.EXTERN or 
             node.storage_class == cc.StorageClass.STATIC)
        )
        if is_global_variable:
            global_variable_count += 1
    
    return global_variable_count


def count_recursive_structures(tu):
    recursive_structure_count = 0
    
    for node in tu.cursor.walk_preorder():
        if node.kind == cc.CursorKind.STRUCT_DECL and node.is_definition():
            struct_name = 'struct ' + node.spelling
            for child_node in node.get_children():
                for type_node in child_node.get_children():
                    if type_node.kind == cc.CursorKind.TYPE_REF and type_node.spelling == struct_name:
                        recursive_structure_count += 1
    
    return recursive_structure_count


def count_bounded_loops(tu):
    # bounded_loop_count = 0
    
    # for node in tu.cursor.walk_preorder():
    #     if node.kind == cc.CursorKind.FOR_STMT:
    #         bounded_loop_count += 1
    
    # return bounded_loop_count
    return 0


def count_unbounded_loops(tu):
    # unbounded_loop_count = 0
    
    # for node in tu.cursor.walk_preorder():
    #     if node.kind == cc.CursorKind.WHILE_STMT:
    #         unbounded_loop_count += 1
    
    # return unbounded_loop_count
    return 0


# get the max depth of nesting loop
def loop_nesting_level(tu):    
    
    def is_loop(node):
        return ( 
            node.kind == cc.CursorKind.FOR_STMT or 
            node.kind == cc.CursorKind.WHILE_STMT or 
            node.kind == cc.CursorKind.DO_STMT
        )
    
    def nesting_level(node):
        max = 0
        for child in node.get_children():
            nl = nesting_level(child)
            if nl > max:
                max = nl
                
        if is_loop(node): return max +1
        return max
        
    return nesting_level(tu.cursor)
    

def has_recursion(tu):
    for node in tu.cursor.walk_preorder():
        if node.kind == cc.CursorKind.FUNCTION_DECL:
            function_name = node.spelling
            for child_node in node.walk_preorder():
                if child_node.kind == cc.CursorKind.CALL_EXPR and child_node.spelling == function_name:
                    return True
    
    return False

def has_heap_access(tu):
    for node in tu.cursor.walk_preorder():
        if node.kind == cc.CursorKind.CALL_EXPR:
            function_name = node.spelling
            if function_name == "malloc" or function_name == "calloc" or function_name == "realloc" or function_name == "free":
                return True
    
    return False

def accesses_recursive_structures(tu):
    # for node in tu.cursor.walk_preorder():
    #     if node.kind == cc.CursorKind.MEMBER_REF_EXPR:
    #         struct_name = node.type.spelling
    #         if struct_name in tu.spelling:
    #             return True
    
    return False


def accesses_global_variables(tu):
    # for node in tu.cursor.walk_preorder():
    #     access = (
    #         node.kind == cc.CursorKind.DECL_REF_EXPR and  
    #         (node.storage_class == cc.StorageClass.EXTERN or
    #          node.storage_class == cc.StorageClass.STATIC)
    #     )
        
    #     print(node.spelling, node.storage_class, node.kind)
    #     if access:
    #         return True
    
    return False

# Generate report
report = f"Report for {FILE}:\n"
report += f"Global Variable Count: {count_global_variables(translation_unit)}\n"
report += f"Recursive Structure Count: {count_recursive_structures(translation_unit)}\n"
report += f"Bounded Loop Count: {count_bounded_loops(translation_unit)}\n"
report += f"Unbounded Loop Count: {count_unbounded_loops(translation_unit)}\n"
report += f"Max Loop Nesting Level: {loop_nesting_level(translation_unit)}\n"
report += f"Has Recursion: {has_recursion(translation_unit)}\n"
report += f"Has Heap Access: {has_heap_access(translation_unit)}\n"
report += f"Accesses Recursive Structures: {accesses_recursive_structures(translation_unit)}\n"
report += f"Accesses Global Variables: {accesses_global_variables(translation_unit)}\n"

print(report)