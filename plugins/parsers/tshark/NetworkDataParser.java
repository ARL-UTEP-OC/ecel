import java.io.*;
import java.util.*;

public class NetworkDataParser {

  public static void main(String args[]) {
	  String ifx = "";
	  String inputFilename = "";
	  String outputpath = "";
	  try
	  {
		  
		if(args.length == 2)
		{
			//ifx = args[0]; //eventually we will have the option to output this in-vivo
			inputFilename = args[0];
			outputpath = args[1];
		}
		else
		{
			System.out.println("Usage: java NetworkDataParser <input_pcap_filename> <output-directory>");
			System.exit(-1);
		}
	startPassiveScanner(ifx, inputFilename, outputpath);
	}
	catch(Exception err)
	{
		System.out.println("ERROR: " + err.toString());
	} 
	  
  }
  
  protected static void startPassiveScanner(String ifx, String inputFilename, String outputDirectory)
  {
	  int windowSize = 1;
	  System.out.println("Parsing network data " + outputDirectory);
	  try {
			String buffer = "";
			String tsharkCommand = "tshark";
			String capinfosCommand = "capinfos";
			long numLines = 0;
            System.out.println("\tExtracting data using tshark...");

      		//get line count:
       		String line;
            Process process = new ProcessBuilder(capinfosCommand, inputFilename, "-cTrb").start();
       		InputStream is = process.getInputStream();
       		InputStreamReader isr = new InputStreamReader(is);
      		BufferedReader br = new BufferedReader(isr);
       		line = br.readLine();
       		br.close();
      		numLines = Long.parseLong(line.split(" ")[1]);

            System.out.println("\tFound "+numLines+ " data items.");
            //start processing pcap file
    	    process = new ProcessBuilder(
   		    //tsharkCommand, "-i", ifx, "-n", "-T", "fields", "-E", "separator=,", "-eframe.protocols", "-eframe.time_epoch", "-eeth.src", "-eeth.dst", "-earp.src.proto_ipv4", "-earp.dst.proto_ipv4", "-eip.src", "-eip.dst", "-eudp.srcport", "-eudp.dstport", "-etcp.srcport", "-etcp.dstport", "-etcp.flags", "-erip.ip", "-erip.netmask", "-erip.next_hop", "-erip.metric" ).start();
      		tsharkCommand, "-r", inputFilename, "-T", "fields", "-E", "separator=,", "-eframe.protocols", "-eframe.time_epoch", "-eeth.src", "-eeth.dst", "-earp.src.proto_ipv4", "-earp.dst.proto_ipv4", "-eip.src", "-eip.dst", "-eudp.srcport", "-eudp.dstport", "-etcp.srcport", "-etcp.dstport", "-etcp.flags", "-erip.ip", "-erip.netmask", "-erip.next_hop", "-erip.metric" ).start();

            //start the readers from the beginning to process input
       		is = process.getInputStream();
       		isr = new InputStreamReader(is);
       		br = new BufferedReader(isr);

       		FramePacketData frame;
       		PacketData packetData = null;
       		long updatePeriod = 500;
       		long currLine = 0;
       		while ((line = br.readLine()) != null) {
       		    currLine++;
                if (currLine%updatePeriod == 0 || currLine == numLines)
				    System.out.println("STAGE I: Processing packet: " + currLine + "/" + (numLines));
       			frame = new FramePacketData(line);
       			if (frame.getFrameProtocols().startsWith("eth:ip:tcp") || frame.getFrameProtocols().startsWith("eth:ethertype:ip:tcp"))
       				packetData = new EthIpTcpPacketData(line);
       			else if (frame.getFrameProtocols().startsWith("eth:ip:udp:rip") || frame.getFrameProtocols().startsWith("eth:ethertype:ip:udp:rip"))
       				packetData = new EthIpUdpRipPacketData(line);
       			else if (frame.getFrameProtocols().startsWith("eth:ip:udp") || frame.getFrameProtocols().startsWith("eth:ethertype:ip:udp"))
       				packetData = new EthIpUdpPacketData(line);
       			else if (frame.getFrameProtocols().startsWith("eth:ip") || frame.getFrameProtocols().startsWith("eth:ethertype:ip"))
       				packetData = new EthIpPacketData(line);
       			else if (frame.getFrameProtocols().startsWith("eth:arp") || frame.getFrameProtocols().startsWith("eth:ethertype:arp"))
       				packetData = new EthArpPacketData(line);
       			else if (frame.getFrameProtocols().startsWith("eth") || frame.getFrameProtocols().startsWith("eth:ethertype"))
       				packetData = new EthPacketData(line);
       			buffer+=packetData.toString() + "\n";
            }

		    System.out.println("\tWriting " + (buffer.split("\r\n|\r|\n").length-1) +" data items to JSON");
			TimeDisplayStringFormatter.writeJSONFiles(buffer, windowSize, outputDirectory);
		    System.out.println("\tProcessing complete ");
		if(buffer.trim().equals(""))
		{
            System.out.println("\tNo network data items found");
		}

    }
    catch (Exception err) {
      err.printStackTrace();
    }
  }  
}
