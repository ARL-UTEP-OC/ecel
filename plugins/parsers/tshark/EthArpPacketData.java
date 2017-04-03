class EthArpPacketData extends EthPacketData
{
  
  protected String arpIpSrc;
  protected String arpIpDst;
  
  public EthArpPacketData(String packetData)
  {
	  super(packetData);
	  	String[] answer = packetData.split(",",-1);

		arpIpSrc = answer[PacketData.Fields.ARP_IP_SRC.ordinal()];
		arpIpDst = answer[PacketData.Fields.ARP_IP_DST.ordinal()];
  }
  
  public String getArpIpSrc()
  {
	  return arpIpSrc;
  }
  
  public String getArpEthDst()
  {
	  return arpIpDst;
  }
  
  public EthArpPacketData parsePacketData(String packetData)
  {
	return this;
  }
  
    public String toMapFormat()
  {
	  String answer = super.toMapFormat();
	  //only add when both source and dst ip address exist
	  if (!arpIpSrc.equals("") && !arpIpDst.equals(""))
	  {
		answer+=arpIpSrc + " | " + "host | " + arpIpSrc + " | PASSIVE_SCAN" + "\n";
		answer+=arpIpSrc + " | " + "host_mac | " + ethSrc + " | PASSIVE_SCAN" + "\n";
		answer+=arpIpDst + " | " + "host | " + arpIpDst + " | PASSIVE_SCAN" + "\n";
		answer+=arpIpDst + " | " + "host_mac | " + ethDst + " | PASSIVE_SCAN" + "\n";
	}
	  return answer;
  }
  
  public String toString()
  {
	  return super.toString() + " " + arpIpSrc + " " + arpIpDst;
  }


}
