#include "MyParseNumber.h"

/* void myParseInt_(long *pos, char *number, char delimiter){ */
/*   *pos = 0; */
  
/*   bool isNegative = (*number=='-'); */
/*   if (isNegative) number++; */

/*   while (*number != delimiter){ */
/*     if (isdigit(*number)) { */ 
/*         *pos = (*pos * 10) + (*number - '0'); */
/*     } */
/*     number++; */
/*   } */
/*   if(isNegative) *pos = -(*pos); */
/* } */

void bytesToLong_(long *pos, char *number){
  *pos = 0;
  for (int i = 0; i < 4; i++)
    *pos |= (long) ((byte)number[i] << (i*8));
}

