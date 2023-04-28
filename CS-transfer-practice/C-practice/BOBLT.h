#pragma once
#include<stdio.h>
#include<math.h>//Ƕ��


//��x��n�η�������װ
double power(double x, int n)
{
	if (n == 0)//�����if(n<=1)
	{
		return 1;//������return x;
	}
	else
	{
		return x * power(x, n - 1);
	}
}

#define PI 3.1415926
//Բ�����������װ
double Circle_area(double r)
{
	return PI * r * r;
}

//��ı����������װ
double Ball_area(double r)
{
	return 4 * PI * power(r,2);
}

//������������װ
double Ball_volume(double r)
{
	return PI * power(r,3) * 4 / 3;
}
//�����жϺ�����װ
bool Prime_number(int num)
{
	bool b = true;
	for (int i = 2;i < num;i++)
	{
		if (num % i == 0)
		{
			b = false;
			break;
		}
	}
	return b;
}
//��һԪ���η��̺�����װ
void Solve_equation(int a, int b, int c)
{
	if (a == 0)
	{
		printf("���Ƕ��η��̣�\n");
		return;
	}
	double d = power(b, 2) - 4.0 * a * c;//dert=b^2-4ac
	if (d < 0)
	{
		printf("��ʵ��\n");
		return;
	}

	double x1 = -b + sqrt(d) / (2.0 * a);
	double x2 = -b - sqrt(d) / (2.0 * a);
	printf("x1=%.2lf,x2=%.2lf", x1, x2);
}