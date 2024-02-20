static int a = 1;

struct b{
    struct b* lll;
    int i;
};

int foo(){
    int i = a;
    return 1;
}

int loop(){
    for(int i = 0; i< 10; i++);
    while(1){
        for(int i = 1; i< 1; i++){
            while(1);
        };
    }
    
    return 0;
}
