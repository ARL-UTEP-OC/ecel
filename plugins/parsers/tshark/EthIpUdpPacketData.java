class EthIpUdpPacketData extends EthIpPacketData
{
  protected String udpSrcPort;
  protected String udpDstPort;
  
  public EthIpUdpPacketData(String packetData)
  {
	  super(packetData);
	  	String[] answer = packetData.split(",",-1);

		udpSrcPort = answer[PacketData.Fields.UDP_SRCPORT.ordinal()];
		udpDstPort = answer[PacketData.Fields.UDP_DSTPORT.ordinal()];
  }
  public String getUdpSrcPort()
  {
	  return udpSrcPort;
  }
  
  public String getUdpDstPort()
  {
	  return udpDstPort;
  }
  public EthIpUdpPacketData parsePacketData(String packetData)
  {
	return this;
  }

  public String toMapFormat()
  {
	  String answer = super.toMapFormat();
	  	  if (protocol.indexOf("eth:ip:udp") != -1)
	  {
	  if (!ipSrc.equals(""))
		answer+=ipSrc + " | " + "port | " + udpSrcPort +":"+protocol.substring(7) + ": | PASSIVE_SCAN" + "\n";
	  if (!ipDst.equals(""))
		answer+=ipDst + " | " + "port | " + udpDstPort +":"+protocol.substring(7) + ": | PASSIVE_SCAN" + "\n";
	}
	  return answer;
  }
  
  public String toString()
  {
	  return super.toString() + " " + udpSrcPort + " " + udpDstPort;
  }


}
