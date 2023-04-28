#include <stdio.h>

/*example*/
const int b = 100;
static int a;

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
  // print answer
  printf("%d\n", b);
  return 0;
}