class EthIpPacketData extends EthPacketData
{
  protected String ipSrc;
  protected String ipDst;
  
  public EthIpPacketData(String packetData)
  {
	  super(packetData);
	  	String[] answer = packetData.split(",",-1);
		ipSrc = answer[PacketData.Fields.IP_SRC.ordinal()];
		ipDst = answer[PacketData.Fields.IP_DST.ordinal()];
  }
  
  public String getIpSrc()
  {
	  return ipSrc;
  }
  
  public String getEthDst()
  {
	  return ipDst;
  }
  
  public EthIpPacketData parsePacketData(String packetData)
  {
	return this;
  }
  
  public String toMapFormat()
  {
	  String answer = super.toMapFormat();
	  if (!ipSrc.equals(""))
	  {
		answer+=ipSrc + " | " + "host | " + ipSrc + " | PASSIVE_SCAN" + "\n";
		answer+=ipSrc + " | " + "host_mac | " + ethSrc + " | PASSIVE_SCAN" + "\n";
	  }
	  if (!ipDst.equals(""))
	  {
		answer+=ipDst + " | " + "host | " + ipDst + " | PASSIVE_SCAN" + "\n";
		answer+=ipDst + " | " + "host_mac | " + ethDst + " | PASSIVE_SCAN" + "\n";
	  }
	return answer;
  }
  
  public String toString()
  {
	  return super.toString() + " " + ipSrc + " " + ipDst;
  }


}
