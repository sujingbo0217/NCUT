#include<stdio.h>
int main()
{
	int x,y,z,max;                    /*����*/  
	printf("��������������");
	scanf("%d%d%d",&x,&y,&z);
	max=x;                            *****
	if (max<y)
	max=y;
	if (max<z)
	max=z;
	printf("max is %d",max);
}
