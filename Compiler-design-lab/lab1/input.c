#include <stdio.h>
#include <stdlib.h>

/*example*/
static int a;
const int b \
    = 100;
char * message = "Hello, world!";
char ch = 'c';

int main() {
  // test goto
  101 : a = 2 * (1 + 3);
  if (b > 10) {
    a = 1;
  } else if (b >= 5) {
    a = 2;
  } else {
    goto 101;
  }

  /* Test command */

  // print answer
  printf("%d\n", b);
  printf("%s\n", message);
  return 0;
}