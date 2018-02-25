#include<iostream>
#include<winsock2.h>
#include<ws2tcpip.h>
#include<cstring>
using namespace std;

///ip��ͷ
typedef struct
{
    unsigned char hdr_len:4;
    unsigned char version:4;
    unsigned char tos;///8λ��������
    unsigned short total_len;///16λ�ܳ���
    unsigned short identifier;///16λ��ʶ��
    unsigned short frag_and_flags;///3λ��־��13λƬƫ��
    unsigned char ttl;///����ʱ��
    unsigned char protocol;///8λ�ϲ�Э��
    unsigned long sourceIP;///32λԴIp��ַ
    unsigned long destIP;///32λĿ��Ip��ַ
} IP_HEADER;

///imcp��ͷ

typedef struct
{
    BYTE type;///8Ϊ�����ֶ�
    BYTE code;///8Ϊ�����ֶ�
    USHORT cksum;///16λУ���
    USHORT id;///16λ��ʶ��
    USHORT seq;///16λ���к�
} ICMP_HEADER;

typedef struct
{
    USHORT usSeqNo;///���к�
    DWORD dwRoundTripTime;///����ʱ��
    in_addr dwIPaddr;///���ر��ĵ�ip�ĵ�ַ
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

///�����ݰ����н���
BOOL DecodeIcmpResponse(char *pBuf,int iPacketSize,DECODE_RESULT &DecodeResult,
                        BYTE ICMP_ECHO_REPLY,BYTE ICMP_TIMEOUT)
{
    ///������ݱ���С�ĺϷ���

    IP_HEADER *pIpHdr = (IP_HEADER *)pBuf;
    int iIpHdrLen = pIpHdr->hdr_len << 2;
    if(iPacketSize < (int)(iIpHdrLen + sizeof(ICMP_HEADER)))
        return false;
    ICMP_HEADER *pIcmpHdr = (ICMP_HEADER * )(pBuf + iIpHdrLen);///��ȡicmp����
    USHORT usId,usSquNo;

    if(pIcmpHdr->type == ICMP_ECHO_REPLY)  ///�ж��Ƿ���icmp����Ӧ����
    {
        usId = pIcmpHdr->id;///����ID
        usSquNo = pIcmpHdr->seq ;///�������к�
    }
    else if(pIcmpHdr->type == ICMP_TIMEOUT)///��ʱ�����
    {
        char *pInnerIpHdr = pBuf + iIpHdrLen + sizeof(ICMP_HEADER); ///�غ��е�ipͷ
        int iInnerIPHdrLen = ((IP_HEADER *)pInnerIpHdr)->hdr_len >> 2;///�غ��е�Ipͷ����
        ICMP_HEADER *pInnerIcmpHdr = (ICMP_HEADER * )(pInnerIpHdr + iInnerIPHdrLen);///�غ��е�icmpͷ

        usId = pInnerIcmpHdr->id;///����ID
        usSquNo = pInnerIcmpHdr->seq ;///�������к�
    }
    else
    {
        return false;
    }

    if(usId != (USHORT)GetCurrentProcessId() || usSquNo != DecodeResult.usSeqNo)
    {
        return false;
    }

    ///��¼ip��ַ����������ʱ��
    DecodeResult.dwIPaddr.s_addr = pIpHdr->sourceIP;
    DecodeResult.dwRoundTripTime = GetTickCount() - DecodeResult.dwRoundTripTime;

    ///������ȷ�յ���icmp���ݱ�
    if(pIcmpHdr->type == ICMP_ECHO_REPLY || pIcmpHdr->type == ICMP_TIMEOUT)
    {
        ///�������ʱ����Ϣ
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
    cout<<"������һ��IP��ַ������: ";
    cin>>IpAddress;
    ///�õ�ip��ַ
    u_long ulDestIP = inet_addr(IpAddress);
    ///ת�����ɹ�ʱ����������
    if(ulDestIP == INADDR_NONE)
    {
        hostent *pHostent = gethostbyname(IpAddress);
        if(pHostent)
        {
            ulDestIP = (*(in_addr*)pHostent->h_addr).s_addr;
        }
        else
        {
            cout<<"�����Ip��ַ��������Ч!"<<endl;
            WSACleanup();
            return 0;
        }
    }
    cout<<"Tracing route to "<<IpAddress<<"with a maximum of 30 hops.\n"<<endl;

    ///���Ŀ�Ķ�socket��ַ
    sockaddr_in destSockAddr;
    ZeroMemory(&destSockAddr,sizeof(sockaddr_in));
    destSockAddr.sin_family = AF_INET;
    destSockAddr.sin_addr.s_addr = ulDestIP;
    ///����ԭʼ�׽���
    SOCKET sockRaw = WSASocket(AF_INET,SOCK_RAW,IPPROTO_ICMP,NULL,0,WSA_FLAG_OVERLAPPED);
    int iTimeout = 3000;
    ///���ý��պͷ��ͳ�ʱʱ��
    setsockopt(sockRaw,SOL_SOCKET,SO_RCVTIMEO,(char*)&iTimeout,sizeof(iTimeout));
    setsockopt(sockRaw,SOL_SOCKET,SO_SNDTIMEO,(char*)&iTimeout,sizeof(iTimeout));

    ///����icmp����������Ϣ
    const BYTE ICMP_ECHO_REQUEST = 8;
    const BYTE ICMP_ECHO_REPLY = 0;
    const BYTE ICMP_TIMEOUT = 11;

    const int DEF_ICMP_DATA_SIZE = 32;
    const int MAX_ICMP_PACKET_SIZE = 1024;
    const DWORD DEF_ICMP_TIMEOUT = 3000;
    const int DEF_MAX_HOP = 30;

    ///���icmp������ÿ�η���ʱ������ֶ�

    char IcmpSendBuf[sizeof(ICMP_HEADER) + DEF_ICMP_DATA_SIZE];///���ͻ�����
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
    DECODE_RESULT DecodeResult; ///���ݸ����Ľ��뺯���Ľṹ������

    while(!bReachDestHost && iMaxHot--)
    {
        ///����ip��ͷ��ttl�ֶ�
        setsockopt(sockRaw,IPPROTO_IP,IP_TTL,(char*)&iTTL,sizeof(iTTL));
        cout<<iTTL<<flush;

        ///���icmp������ÿ�η��ͱ仯���ֶ�
        ((ICMP_HEADER*)IcmpSendBuf)->cksum = 0;
        ((ICMP_HEADER*)IcmpSendBuf)->seq = htons(usSeqNo++);
        ((ICMP_HEADER*)IcmpSendBuf)->cksum = checksum((USHORT*)IcmpSendBuf,sizeof(ICMP_HEADER)+DEF_ICMP_DATA_SIZE);///����У���

        ///��¼���кź͵�ǰʱ��
        DecodeResult.usSeqNo = ((ICMP_HEADER*)IcmpSendBuf)->seq;///��ǰ���
        DecodeResult.dwRoundTripTime = GetTickCount();///��ǰʱ��

        ///����tcp����������Ϣ
        sendto(sockRaw,IcmpSendBuf,sizeof(IcmpSendBuf),0,(sockaddr*)&destSockAddr,sizeof(destSockAddr));
        ///����icmp����Ľ��н�������
        sockaddr_in from;///�Զ�socket��ַ
        int iFromLen = sizeof(from);
        int iReadDataLen;///�������ݳ���
        while(1)
        {
            ///��������
            iReadDataLen = recvfrom(sockRaw,IcmpRecvBuf,MAX_ICMP_PACKET_SIZE,0,(sockaddr*)&from,&iFromLen);
            cout<<WSAGetLastError()<<endl;
            if(iReadDataLen != SOCKET_ERROR)///�����ݵ���
            {
                ///�����ݱ����н���
                if(DecodeIcmpResponse(IcmpRecvBuf,iReadDataLen,DecodeResult,ICMP_ECHO_REPLY,ICMP_TIMEOUT))
                {
                    ///����Ŀ�ĵأ��˳�ѭ��
                    if(DecodeResult.dwIPaddr.s_addr == destSockAddr.sin_addr.s_addr)
                        bReachDestHost = TRUE;
                    cout<<'\t'<<inet_ntoa(DecodeResult.dwIPaddr)<<endl;
                    break;
                }
            }
            else if(WSAGetLastError() == WSAETIMEDOUT) ///���ճ�ʱ�����*
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
