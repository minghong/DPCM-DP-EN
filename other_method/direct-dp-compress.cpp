#include<iostream>
#include<cmath>
#include<stack>
#include<bits/stdc++.h>
using namespace std;

const int N = 1500*1500+1;
int p[N+1];
int length(int i);
void Compress(int n,int p[],int s[],int l[],int b[]);
int TraceBack(int n,int l[],int b[]);  //返回有多少个段
void Out(int m,int min_len,int l[],int b[]);
void test()
{

	ifstream in("matrix.txt");
	string line;
	while (getline(in, line)){//获取文件的一行字符串到line中
		stringstream ss(line);//初始化 法1
		int x;
		int i=1;
		while (ss >> x){//每一行包含不同个数的数字

			p[i++]=int(x);

		}

	}
}

int main()
{
    //int p[] = {0,10,12,15,255,1,2};//图像灰度数组 下标从1开始计数
    test();
    int s[N]={0},l[N]={0},b[N]={0};

	int aa;int bb;cin>>aa>>bb;
	int mm=aa*bb;
    Compress(mm,p,s,l,b);
    int m=TraceBack(mm,l,b);
    Out(m,s[mm],l,b);
    return 0;
}

void Compress(int n,int p[],int s[],int l[],int b[])
{
    int Lmax = 256,header = 12;
    s[0] = 0;
    for(int i=1; i<=n; i++)
    {
        b[i] = length(p[i]);//计算像素点p需要的存储位数
        int bmax = b[i];
        s[i] = s[i-1] + bmax + header;
        l[i] = 1;

        for(int j=2; j<=i && j<=Lmax;j++)  //最后一段含有一个像素，两个像素，所有像素
        {
            //if(bmax<b[i-j+1])   //最后一个b[i-j+1]有效，是前一段当中的最大值，并不是后一段中的最大值
            if(bmax<length(p[i-j+1]))
            {
                bmax = length(p[i-j+1]);
            }

            if(s[i]>s[i-j]+j*bmax+header)
            {
                s[i] = s[i-j] + j*bmax+header;
                l[i] = j;
                b[i] = bmax;  //我加，跟新当前组，所需的存储位数
            }
        }
    }
}

int length(int i)
{
    int k=1;
    i = i/2;
    while(i>0)
    {
        k++;
        i=i/2;
    }
    return k;
   //return ceil(log(i+1)/log(2));
}

int TraceBack(int n,int l[],int b[]) //从后向前检查，因而之后对应段的，最后一个存储有效
{
    stack<int>ss;
    ss.push(l[n]);
    ss.push(b[n]);
    while (n!=0)
    {
        n=n-l[n];
        ss.push(l[n]);  //l[0]=0,也被压入栈中
        ss.push(b[n]);
    }
    int i=0;
    while (!ss.empty())
    {
        b[i]=ss.top();
        ss.pop();
        l[i]=ss.top(); //此时　ｌ[]，用来存储，第ｉ组中，元素个数
        ss.pop();
        i++;
    }
    return i-1;
}

void Out(int m,int min_len,int l[],int b[])
{
    int i=0;
    ofstream outfile("signal_pixel.txt");
    cout<<min_len;
    for(int j=1; j<=m; j++)
    {
        outfile << l[j] << " "<<b[j]<<endl;
    }

    outfile.close();
}
