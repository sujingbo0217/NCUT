﻿/* 某手机组装厂，按绩效得分的多少给工资
   每生产一个合格手机给4分，每生产一个不合格手机不仅不记分，还要扣除15分
   某工人组装了1000个手机，共得3525分
   问其中有多少个手机组装不合格?良品率是百分之多少?精确到小数点后两位 */
#include<stdio.h>
int main()
{
	int a, b;
	double c;
	for (a = 1; a < 1000; a++)
	{
		

		
			b = 1000 - a;
			if (4 * a - 15 * b == 3525)
			{
				printf("组装不合格的有:%d\n", b);
				c = a / 10;
				printf("组装产品的良品率为:%.2f%%", c);
			}
			
		
		
	}
}