public abstract class PacketData
{
	protected String protocol;
	public enum Fields {
		FRAME_PROTOCOLS, FRAME_TIMEEPOCH, ETH_SRC, ETH_DST, ARP_IP_SRC, ARP_IP_DST, IP_SRC, IP_DST,
		UDP_SRCPORT, UDP_DSTPORT, TCP_SRCPORT, TCP_DSTPORT, TCP_FLAGS, RIP_DATA
	}
	public String getProtocol()
	{
		return protocol;
	}
	public abstract PacketData parsePacketData(String PacketData);
	public abstract String toMapFormat();
	public abstract String toString();
}
