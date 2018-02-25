#include "ping.h"


struct hostent * pHost = NULL;		//����������Ϣ
int sock_icmp;				//icmp�׽���
int nSend = 1;
char *IP = NULL;

void Call(int argc, char *argv[])
{

	struct protoent *protocol;
	struct sockaddr_in dest_addr; 	//IPv4ר��socket��ַ,����Ŀ�ĵ�ַ

	in_addr_t inaddr;		//ip��ַ�������ֽ���

	if (argc < 2)
	{
		printf("Usage: %s [hostname/IP address]\n", argv[0]);
		exit(EXIT_FAILURE);	
	}

	if ((protocol = getprotobyname("icmp")) == NULL)
	{
		perror("getprotobyname");
		exit(EXIT_FAILURE);
	}

	/* ����ICMP�׽��� */
	//AF_INET:IPv4, SOCK_RAW:IPЭ�����ݱ��ӿ�, IPPROTO_ICMP:ICMPЭ��
	if ((sock_icmp = socket(PF_INET, SOCK_RAW, protocol->p_proto/*IPPROTO_ICMP*/)) < 0)
	{
		perror("socket");
		exit(EXIT_FAILURE);
	}
	dest_addr.sin_family = AF_INET;

	/* �����ʮ����ip��ַת��Ϊ�����ֽ��� */
	if ((inaddr = inet_addr(argv[1])) == INADDR_NONE)
	{
		/* ת��ʧ�ܣ�������������,��ͨ����������ȡip */
		if ((pHost = gethostbyname(argv[1])) == NULL)
		{
			herror("gethostbyname()");
			exit(EXIT_FAILURE);
		}
		memmove(&dest_addr.sin_addr, pHost->h_addr_list[0], pHost->h_length);
	}
	else
	{
		memmove(&dest_addr.sin_addr, &inaddr, sizeof(struct in_addr));
	}

	if (NULL != pHost)
		printf("PING %s", pHost->h_name);
	else
		printf("PING %s", argv[1]);
	printf("(%s) %d bytes of data.\n", inet_ntoa(dest_addr.sin_addr), ICMP_LEN);

	IP = argv[1];
	signal(SIGINT, Statistics);
	while (nSend < SEND_NUM)
	{
		int unpack_ret;
		
		SendPacket(sock_icmp, &dest_addr, nSend);
		
		unpack_ret = RecvePacket(sock_icmp, &dest_addr);
		if (-1 == unpack_ret)	//��ping�ػ�ʱ���յ����Լ������ı���,���µȴ�����
			RecvePacket(sock_icmp, &dest_addr);
			

		sleep(1);
		nSend++;
	}
	
	Statistics(0);	//�����Ϣ���ر��׽���
}

int main(int argc, char *argv[])
{
	Call(argc, argv);

	return 0;
}