#include "MyParseNumber.h"

void myParseInt_(long *pos, char *number, char delimiter){
  *pos = 0;
  
  bool isNegative = (*number=='-');
  if (isNegative) number++;

  while (*number != delimiter){
    if (isdigit(*number)) { 
        *pos = (*pos * 10) + (*number - '0');
    }
    number++;
  }
  if(isNegative) *pos = -(*pos);
}

/* void bytesToLong_(long *pos, char *number, char delimiter){ */
/*   *pos = 0; */
/*   int x = 0; */

/*   while (number[x] != delimiter)  x++; */

/*   x = min(4, x); */
/*   for (int i = 0; i < x; i++) */
/*     *pos |= number[i] << ((x-i-1)*8); */
/* } */

/* long myParseInt() */
/* // A modified function to Serial.parseInt */
/* { */
/*   while(Serial.available()==0) {} */

/*   long value = 0; */
/*   char c = Serial.read(); */
/*   if(c<0) return -1; */

/*   // check if we're negative, and if so, skip to the next character */
/*   bool isNegative = (c=='-'); */
/*   if(isNegative) {c = Serial.read();} */

/*   while (c != '\n'){ */
/*     if (isdigit(c)) { */ 
/*         value = (value * 10) + (c - '0'); */
/*     } */
/*     c = Serial.read(); */
/*   } */
/*   if(isNegative) value = -value; */
/*   return value; */
/* } */
