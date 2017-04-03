class FramePacketData extends PacketData
{
  protected String frameProtocols;
  protected String frameTimeEpoch;
  
  public FramePacketData(String packetData)
  {
	String[] answer = packetData.split(",",-1);
	frameProtocols = answer[PacketData.Fields.FRAME_PROTOCOLS.ordinal()];
	frameTimeEpoch = answer[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()];
  }
  
  public String getFrameProtocols()
  {
	  return frameProtocols;
  }
  
  public String getFrameTimeEpoch()
  {
	  return frameTimeEpoch;
  }
  
  public FramePacketData parsePacketData(String packetData)
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
	  return frameProtocols + " " + frameTimeEpoch;
  }


}
