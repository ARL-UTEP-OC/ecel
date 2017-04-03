class EthIpTcpPacketData extends EthIpPacketData
{
  protected String tcpSrcPort;
  protected String tcpDstPort;
  protected String tcpFlags;
  
  public EthIpTcpPacketData(String packetData)
  {
	  super(packetData);
	  	String[] answer = packetData.split(",",-1);

		tcpSrcPort = answer[PacketData.Fields.TCP_SRCPORT.ordinal()];
		tcpDstPort = answer[PacketData.Fields.TCP_DSTPORT.ordinal()];
		tcpFlags = answer[PacketData.Fields.TCP_FLAGS.ordinal()];
  }
  
  public String getTcpSrcPort()
  {
	  return tcpSrcPort;
  }
  
  public String getTcpDstPort()
  {
	  return tcpDstPort;
  }
  
  public EthIpTcpPacketData parsePacketData(String packetData)
  {
	return this;
  }

  public String toMapFormat()
  {
	  String answer = super.toMapFormat();
	  if (protocol.indexOf("eth:ip:tcp") != -1)
	  {
		if (!ipSrc.equals(""))
			answer+=ipSrc + " | " + "port | " + tcpSrcPort+":"+protocol.substring(7) + ": | PASSIVE_SCAN" + "\n";
		if (!ipDst.equals(""))
			answer+=ipDst + " | " + "port | " + tcpDstPort+":"+protocol.substring(7) + ": | PASSIVE_SCAN" + "\n";
	}
	  return answer;
  }
  
  
  public String toString()
  {
	  return super.toString() + " " + tcpSrcPort + " " + tcpDstPort + " " + tcpFlags;
  }


}
