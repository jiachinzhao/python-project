#include<iostream>
#include<winsock2.h>
#include<ws2tcpip.h>
#include<cstring>
using namespace std;

///ip报头
typedef struct
{
    unsigned char hdr_len:4;
    unsigned char version:4;
    unsigned char tos;///8位服务类型
    unsigned short total_len;///16位总长度
    unsigned short identifier;///16位标识符
    unsigned short frag_and_flags;///3位标志加13位片偏移
    unsigned char ttl;///生存时间
    unsigned char protocol;///8位上层协议
    unsigned long sourceIP;///32位源Ip地址
    unsigned long destIP;///32位目的Ip地址
} IP_HEADER;

///imcp报头

typedef struct
{
    BYTE type;///8为类型字段
    BYTE code;///8为代码字段
    USHORT cksum;///16位校验和
    USHORT id;///16位标识符
    USHORT seq;///16位序列号
} ICMP_HEADER;

typedef struct
{
    USHORT usSeqNo;///序列号
    DWORD dwRoundTripTime;///往返时间
    in_addr dwIPaddr;///返回报文的ip的地址
} DECODE_RESULT;
USHORT checksum(USHORT *pBuf,int iSize)
{
    unsigned long cksum = 0;
    while(iSize > 1)
    {
        cksum += *pBuf++;
        iSize -= sizeof(USHORT);
    }
    if(iSize)
    {
        cksum += *(UCHAR *)pBuf;
    }
    cksum = (cksum >> 16) + (cksum & 0xffff);
    cksum += (cksum >> 16);
    return (USHORT)(~cksum);
}

///对数据包进行解码
BOOL DecodeIcmpResponse(char *pBuf,int iPacketSize,DECODE_RESULT &DecodeResult,
                        BYTE ICMP_ECHO_REPLY,BYTE ICMP_TIMEOUT)
{
    ///检查数据报大小的合法性

    IP_HEADER *pIpHdr = (IP_HEADER *)pBuf;
    int iIpHdrLen = pIpHdr->hdr_len << 2;
    if(iPacketSize < (int)(iIpHdrLen + sizeof(ICMP_HEADER)))
        return false;
    ICMP_HEADER *pIcmpHdr = (ICMP_HEADER * )(pBuf + iIpHdrLen);///提取icmp报文
    USHORT usId,usSquNo;

    if(pIcmpHdr->type == ICMP_ECHO_REPLY)  ///判断是否是icmp回显应答报文
    {
        usId = pIcmpHdr->id;///报文ID
        usSquNo = pIcmpHdr->seq ;///报文序列号
    }
    else if(pIcmpHdr->type == ICMP_TIMEOUT)///超时差错报文
    {
        char *pInnerIpHdr = pBuf + iIpHdrLen + sizeof(ICMP_HEADER); ///载荷中的ip头
        int iInnerIPHdrLen = ((IP_HEADER *)pInnerIpHdr)->hdr_len >> 2;///载荷中的Ip头长度
        ICMP_HEADER *pInnerIcmpHdr = (ICMP_HEADER * )(pInnerIpHdr + iInnerIPHdrLen);///载荷中的icmp头

        usId = pInnerIcmpHdr->id;///报文ID
        usSquNo = pInnerIcmpHdr->seq ;///报文序列号
    }
    else
    {
        return false;
    }

    if(usId != (USHORT)GetCurrentProcessId() || usSquNo != DecodeResult.usSeqNo)
    {
        return false;
    }

    ///记录ip地址并计算往返时间
    DecodeResult.dwIPaddr.s_addr = pIpHdr->sourceIP;
    DecodeResult.dwRoundTripTime = GetTickCount() - DecodeResult.dwRoundTripTime;

    ///处理正确收到的icmp数据报
    if(pIcmpHdr->type == ICMP_ECHO_REPLY || pIcmpHdr->type == ICMP_TIMEOUT)
    {
        ///输出往返时间信息
        if(DecodeResult.dwRoundTripTime)
            cout<<"        "<<DecodeResult.dwRoundTripTime<<"ms"<<flush;
        else cout<<"        1ms"<<flush;
    }
    return true;
}
int main()
{
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2),&wsa);
    char IpAddress[255];
    cout<<"请输入一个IP地址或域名: ";
    cin>>IpAddress;
    ///得到ip地址
    u_long ulDestIP = inet_addr(IpAddress);
    ///转换不成功时按域名解析
    if(ulDestIP == INADDR_NONE)
    {
        hostent *pHostent = gethostbyname(IpAddress);
        if(pHostent)
        {
            ulDestIP = (*(in_addr*)pHostent->h_addr).s_addr;
        }
        else
        {
            cout<<"输入的Ip地址或域名无效!"<<endl;
            WSACleanup();
            return 0;
        }
    }
    cout<<"Tracing route to "<<IpAddress<<"with a maximum of 30 hops.\n"<<endl;

    ///填充目的段socket地址
    sockaddr_in destSockAddr;
    ZeroMemory(&destSockAddr,sizeof(sockaddr_in));
    destSockAddr.sin_family = AF_INET;
    destSockAddr.sin_addr.s_addr = ulDestIP;
    ///创建原始套接字
    SOCKET sockRaw = WSASocket(AF_INET,SOCK_RAW,IPPROTO_ICMP,NULL,0,WSA_FLAG_OVERLAPPED);
    int iTimeout = 3000;
    ///设置接收和发送超时时间
    setsockopt(sockRaw,SOL_SOCKET,SO_RCVTIMEO,(char*)&iTimeout,sizeof(iTimeout));
    setsockopt(sockRaw,SOL_SOCKET,SO_SNDTIMEO,(char*)&iTimeout,sizeof(iTimeout));

    ///构造icmp回显请求消息
    const BYTE ICMP_ECHO_REQUEST = 8;
    const BYTE ICMP_ECHO_REPLY = 0;
    const BYTE ICMP_TIMEOUT = 11;

    const int DEF_ICMP_DATA_SIZE = 32;
    const int MAX_ICMP_PACKET_SIZE = 1024;
    const DWORD DEF_ICMP_TIMEOUT = 3000;
    const int DEF_MAX_HOP = 30;

    ///填充icmp报文中每次发送时不变的字段

    char IcmpSendBuf[sizeof(ICMP_HEADER) + DEF_ICMP_DATA_SIZE];///发送缓冲区
    memset(IcmpSendBuf,0,sizeof(IcmpSendBuf));
    char IcmpRecvBuf[MAX_ICMP_PACKET_SIZE];
    memset(IcmpRecvBuf,0,sizeof(IcmpRecvBuf));

    ICMP_HEADER * pIcmpHeader = (ICMP_HEADER *)IcmpSendBuf;

    pIcmpHeader->type = ICMP_ECHO_REQUEST;
    pIcmpHeader->code = 0;
    pIcmpHeader->id = (USHORT)GetCurrentProcessId();
    memset(IcmpSendBuf+sizeof(ICMP_HEADER),'E',DEF_ICMP_DATA_SIZE);

    USHORT usSeqNo = 0;
    int iTTL = 1;
    BOOL bReachDestHost = FALSE;
    int iMaxHot = DEF_MAX_HOP;
    DECODE_RESULT DecodeResult; ///传递给报文解码函数的结构化参数

    while(!bReachDestHost && iMaxHot--)
    {
        ///设置ip报头的ttl字段
        setsockopt(sockRaw,IPPROTO_IP,IP_TTL,(char*)&iTTL,sizeof(iTTL));
        cout<<iTTL<<flush;

        ///填充icmp报文中每次发送变化的字段
        ((ICMP_HEADER*)IcmpSendBuf)->cksum = 0;
        ((ICMP_HEADER*)IcmpSendBuf)->seq = htons(usSeqNo++);
        ((ICMP_HEADER*)IcmpSendBuf)->cksum = checksum((USHORT*)IcmpSendBuf,sizeof(ICMP_HEADER)+DEF_ICMP_DATA_SIZE);///计算校验和

        ///记录序列号和当前时间
        DecodeResult.usSeqNo = ((ICMP_HEADER*)IcmpSendBuf)->seq;///当前序号
        DecodeResult.dwRoundTripTime = GetTickCount();///当前时间

        ///发送tcp回显请求信息
        sendto(sockRaw,IcmpSendBuf,sizeof(IcmpSendBuf),0,(sockaddr*)&destSockAddr,sizeof(destSockAddr));
        ///接收icmp差错报文进行解析处理
        sockaddr_in from;///对端socket地址
        int iFromLen = sizeof(from);
        int iReadDataLen;///接受数据长度
        while(1)
        {
            ///接收数据
            iReadDataLen = recvfrom(sockRaw,IcmpRecvBuf,MAX_ICMP_PACKET_SIZE,0,(sockaddr*)&from,&iFromLen);
            cout<<WSAGetLastError()<<endl;
            if(iReadDataLen != SOCKET_ERROR)///有数据到达
            {
                ///对数据报进行解码
                if(DecodeIcmpResponse(IcmpRecvBuf,iReadDataLen,DecodeResult,ICMP_ECHO_REPLY,ICMP_TIMEOUT))
                {
                    ///到达目的地，退出循环
                    if(DecodeResult.dwIPaddr.s_addr == destSockAddr.sin_addr.s_addr)
                        bReachDestHost = TRUE;
                    cout<<'\t'<<inet_ntoa(DecodeResult.dwIPaddr)<<endl;
                    break;
                }
            }
            else if(WSAGetLastError() == WSAETIMEDOUT) ///接收超时，输出*
            {
                cout<<"           *"<<'\t'<<"Request timed out."<<endl;
                break;
            }
            else
            {
                break;
            }
        }
        iTTL++;
    }
    return 0;
}
