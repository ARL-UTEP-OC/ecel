class EthIpUdpRipPacketData extends EthIpUdpPacketData
{
  protected String[] ips;
  protected String[] subnets;
  protected String[] metrics;
  protected String[] nextHops;
  
  public EthIpUdpRipPacketData(String packetData)
  {
		
	super(packetData);
	String[] answer = packetData.split(",",-1);

	if(!answer[PacketData.Fields.RIP_DATA.ordinal()].equals(""))
	{
		int numberOfEntries = (answer.length - PacketData.Fields.RIP_DATA.ordinal())/4; //we are taking 4 fields
		//System.out.println("numEntries: "+numberOfEntries);
		ips = new String[numberOfEntries];
		subnets = new String[numberOfEntries];
		metrics = new String[numberOfEntries];
		nextHops = new String[numberOfEntries];
	
		for (int i=0; i<numberOfEntries; i++)
		{
			ips[i] = answer[PacketData.Fields.RIP_DATA.ordinal()+(numberOfEntries*0+i)];
			subnets[i] = answer[PacketData.Fields.RIP_DATA.ordinal()+(numberOfEntries*1+i)];
			nextHops[i] = answer[PacketData.Fields.RIP_DATA.ordinal()+(numberOfEntries*2+i)];
			metrics[i] = answer[PacketData.Fields.RIP_DATA.ordinal()+(numberOfEntries*3+i)];
		}
	}

  }
  
  public String[] getIps()
  {
	  return ips;
  }
  
  public String[] getSubnets()
  {
	  return subnets;
  }
  
  public String[] getNextHops()
  {
	  return nextHops;
  }
  
  public String[] getMetrics()
  {
	  return metrics;
  }
  
  public EthIpUdpRipPacketData parsePacketData(String packetData)
  {
	return this;
  }
  
  public String toMapFormat()
  {
	  String answer = super.toMapFormat();
	
	  if (ips != null && subnets != null && nextHops != null && metrics != null)
	  {
		    int i=0;
			/*answer+=ipSrc + " | " + "rip | ";
			for(i=0; i<ips.length-1; i++)
				answer+=ips[i]+","+subnets[i]+","+nextHops[i]+","+metrics[i]+":";
			answer+=ips[i]+","+subnets[i]+","+nextHops[i]+","+metrics[i];
			answer += " | PASSIVE_SCAN" + "\n";*/
			for(i=0; i<ips.length-1; i++)
				answer +=ips[i]+" | "+" rip | " + subnets[i]+" | " + " PASSIVE_SCAN"+"\n";
			
	  }
	  return answer;
  }
  
  public String toString()
  {
	  String answer = super.toString() + ";";
	  if(ips!=null)
	{
		for(int i=0; i<ips.length;i++)
		{
			answer+= ips[i]+", "+subnets[i]+", "+nextHops[i]+", "+metrics[i]+";";
		}
	}
	return answer;
  }


}

