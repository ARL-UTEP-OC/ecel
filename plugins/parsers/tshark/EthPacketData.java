class EthPacketData extends FramePacketData
{
  protected String ethSrc;
  protected String ethDst;
  
  public EthPacketData(String packetData)
  {
	super(packetData);
	String[] answer = packetData.split(",",-1);
	
	ethSrc = answer[PacketData.Fields.ETH_SRC.ordinal()];
	ethDst = answer[PacketData.Fields.ETH_DST.ordinal()];

  }
  
  public String getEthSrc()
  {
	  return ethSrc;
  }
  
  public String getEthDst()
  {
	  return ethDst;
  }
  
  public EthPacketData parsePacketData(String packetData)
  {
	return this;
  }
  
  public String toMapFormat()
  {
	  //return ethSrc + " | " + "host_mac | " + ethSrc + " | PASSIVE_SCAN" + "\n";
	  return "";
  }
  
  public String toString()
  {
	  String answer = super.toString() + " " + ethSrc + " " + ethDst;
	  return answer;
  }


}
