#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*example*/
static int a;
const int _b = 1\
    00; // new line test
char c = 'c';   // character test
double d = 4.2; // float number test
char * message = "Hello, world!";   // string test

int main() {
  // test goto
  L0: a = 2 * (1 + 3);
  if (_b > 10) {
    a = 1;
  } else if (_b >= 5) {
    a = 2;
  } else {
    goto L0;
  }

  /* 
   * Test 
   * multi-line
   * command 
  **/

  // print answer
  printf("%d\n", _b + a);
  printf("%s", message);
  puts("");
  return 0;
}