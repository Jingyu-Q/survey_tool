struct Llist {
    Llist *next;
};

/* 
head is the head of a linked list, node is a linked list node, the function 
checks whether the following properties hold:
    1. node is in the linked list
    2. n is inside a loop in the linked list
if so, return true, otherwise, return false
*/
bool test(Llist* head, Llist* node){
    Llist* ll = head;

    // node is in the linked list
    while(ll != node && ll != nullptr){
        ll = ll->next;
    }
    if(ll != node) return false;

    // node is inside a loop
    while(ll != nullptr){
        ll = ll->next;
        if(ll == node) return true; //there is a loop coming back to n
    }

    return false;
}

/*
It takes in a linked list, return nullptr if there is no loop inside the linked list
otherwise, it returns one node inside that linked list
*/
Llist* magic_algorithm(Llist* head){
    Llist* p1 = head;
    Llist* p2 = head;

    while(p2->next != nullptr && p2->next->next != nullptr){
        p1 = p1->next;
        p2 = p2->next->next;
        if(p1 == p2) return p1;
    }
    return nullptr;
}
