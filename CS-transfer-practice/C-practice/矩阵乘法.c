/*
A(m*n)
B(n*p)
C=A*B
2 3 4
1 0 3
3 4 0
1 0 2 1
2 3 4 5
2 1 1 5

7 3 5 16
11 12 22 23
*/

#include<stdio.h>
int main(){
	int m,n,p,i,j,x;
	int a[15][15],b[15][15],c[15][15];
	scanf("%d%d%d",&m,&n,&p);
	for(i=0;i<m;i++)
		for(j=0;j<n;j++)
			scanf("%d",&a[i][j]);
	for(i=0;i<n;i++)
		for(j=0;j<p;j++)
			scanf("%d",&b[i][j]);
	for(i=0;i<m;i++)
		for(j=0;j<p;j++){
			c[i][j]=0;
			for(x=0;x<n;x++)
				c[i][j]+=a[i][x]*b[x][j];
		}
	for(i=0;i<m;i++){
		for(j=0;j<p;j++)
			printf("%d ",c[i][j]);
		printf("\n");
	}
	return 0;
}
