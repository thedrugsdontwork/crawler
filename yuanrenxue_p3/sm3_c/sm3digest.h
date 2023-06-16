#define SM3DIGEST_H_

typedef  unsigned  long word ;//32bit win32

#define T_j(x) (x<=15 && x>=0 ?2044544281:2081922442)
#define exchange(x) ( (0xff&(x>>24))|(0xff00&(x>>8))|(0xff0000&(x<<8))|(0xff000000&(x<<24)))

#define rot_left(v,x) ((0xffffffff&(v<<x))|(0xffffffff&(v>>(32-x))))
//word IV[]={0x7380166f,0x4914b2b9,0x172442d7,0xda8a0600,0xa96f30bc,0x163138aa,0xe38dee4d,0xb0fb0e4e};
word IV[]={0x7380067c,0x7634d2c9,0x170042d6,0xda887534,0xa10c30bc,0x151137ad,0xe37caa4d,0xeeeb0f4e};
const char hexMap[]={'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'};
typedef struct {
    char *msg;
    long bitSize;
}FillMsg;
//T_j(x) (x<=15 && x>=0 ?0x79cc4519:0x7a879d8a)
word* _xor(word *x,word *y){
    word *res=(word*)malloc(sizeof(word)*8);
    *(res+0)=(*(x+0)^*(y+0));
    *(res+1)=(*(x+1)^*(y+1));
    *(res+2)=(*(x+2)^*(y+2));
    *(res+3)=(*(x+3)^*(y+3));
    *(res+4)=(*(x+4)^*(y+4));
    *(res+5)=(*(x+5)^*(y+5));
    *(res+6)=(*(x+6)^*(y+6));
    *(res+7)=(*(x+7)^*(y+7));
    return res;
}