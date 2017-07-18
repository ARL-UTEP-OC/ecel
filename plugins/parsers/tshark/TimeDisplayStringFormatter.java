import java.io.*;
import java.util.*;
import java.text.*;

public class TimeDisplayStringFormatter {
	static HashSet<String> uniqueElementsPerWindow = new HashSet<String>();
    static long numXYItems = 0;
    static long numProtoItems = 0;

		public static void writeJSONFiles(String buffer, double windowSize, String outputDirectory) {
		String protocolJSON = "[";
		String throughputJSON = "[";
		String[] lines = buffer.split(System.getProperty("line.separator"));

		double currWindowStartTime = 0.0;
		double currPacketTime = 0.0;
		int packetsPerSecond = 0;
		String tempString;
		String[] parsedPacket;
		String timestamp;
		long packetsInWindow = 1;
		SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
		try {						
			//first grab the time_epoch from the line:
			if(lines.length > 1)
			{
				currWindowStartTime = Double.parseDouble(lines[0].split(" ",-1)[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);

			for (int i=0; i<lines.length; i++)
			{
				//System.out.println("line: " + lines[i]);
				parsedPacket = lines[i].split(" ",-1);
				currPacketTime = Double.parseDouble(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);;
				
				//This is the case when the data is still within the window size threshold, and there are still data left
				if((currPacketTime - currWindowStartTime) < windowSize && i != lines.length-1)
				{
					packetsInWindow++;
					//remove any unwanted elements from the array before storing in the map
					//System.out.println(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] );
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println(lines[i] + "\nremoved: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				}
				//The data is part of a new window because the log time is larger than the window size
				else
				{
				    timestamp = toFormat.format(new Date((long)(currWindowStartTime*1000)));
					//System.out.println("Starting new window");

					//////////////////////Append to Protocol JSON//////////////////////
					protocolJSON += "{ \"traffic_all_id\" : "+(numProtoItems++)+", ";
					protocolJSON += "\"content\" :\"";
					packetsPerSecond = (int)(packetsInWindow/windowSize);
					if(packetsPerSecond<1)
						protocolJSON+=quote("<1 p/s");
					else protocolJSON+=quote(packetsPerSecond+" p/s");
					protocolJSON += "\", ";
					
					protocolJSON += "\"className\" : \"traffic";
					protocolJSON += "\", ";
					
					protocolJSON += "\"title\" : \"";
					for(String element : uniqueElementsPerWindow)
					{
						tempString = element.replace(";","\n");
						tempString = quote(tempString);
						protocolJSON += tempString;
					}
					protocolJSON += "\", ";
										
					protocolJSON += "\"start\" : \"" + timestamp;
					if(i == lines.length-1){
						protocolJSON += "\" }\n";
					}
					else{
						protocolJSON += "\" },\n";
					}


					//////////////////////Append to Throughput JSON//////////////////////
					throughputJSON += "{ \"traffic_xy_id\" : "+(numXYItems++)+", ";
					throughputJSON += "\"className\" : \"trafficThroughput";
					throughputJSON += "\", ";
					throughputJSON += "\"x\":\"" + timestamp;
					throughputJSON += "\", ";
					
					throughputJSON += "\"y\" : ";
					packetsPerSecond = (int)(packetsInWindow/windowSize);
					throughputJSON+=packetsPerSecond;
					if(i == lines.length-1){
						throughputJSON += " }\n";
					}
					else{
						throughputJSON += " },\n";
					}


					currWindowStartTime = currPacketTime;
					uniqueElementsPerWindow.clear();
					packetsInWindow = 1;
					//remove any unwanted elements from the array before storing in the map
					
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println("removed: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				} 
			}
			}
		}catch (Exception e) {
			e.printStackTrace();
		}
		protocolJSON += "]";
		throughputJSON += "]";
		
		//Write to the output folder
		FileOutput.WriteToFile(outputDirectory+"/networkDataAll.JSON", protocolJSON);
		FileOutput.WriteToFile(outputDirectory+"/networkDataXY.JSON", throughputJSON);
	}



	public static String formatXMLString(String buffer, double windowSize) {
		String answer = "<?xml version='1.0' encoding='UTF-8'?>\n"+
					"<data>\n";
		String[] lines = buffer.split(System.getProperty("line.separator"));
		double currWindowStartTime = 0.0;
		double currPacketTime = 0.0;
		int packetsPerSecond = 0;
		String tempString;
		String[] parsedPacket;
		try {						
			//first grab the time_epoch from the line:
			if(lines.length > 0)
			{
				currWindowStartTime = Double.parseDouble(lines[0].split(" ",-1)[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);

			for (int i=0; i<lines.length; i++)
			{
				//System.out.println("line: " + lines[i]);
				parsedPacket = lines[i].split(" ",-1);
				currPacketTime = Double.parseDouble(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);;
				//System.out.println(lines[i]);
				if((currPacketTime - currWindowStartTime) < windowSize && i != lines.length-1)
				{
					//remove any unwanted elements from the array before storing in the map
					//System.out.println(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] );
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println(lines[i] + "\nremoved: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				}
				else
				{
					//System.out.println("Starting new window");
					packetsPerSecond = (int)(uniqueElementsPerWindow.size()/windowSize);
					answer += "<event durationEvent='true' start='" + new Date((long)(currWindowStartTime*1000)).toString();
					answer += "' title='" ;
					packetsPerSecond = (int)(uniqueElementsPerWindow.size()/windowSize);
					if(packetsPerSecond<2)
						answer+="&lt;2 p/s";
					else answer+=packetsPerSecond+" p/s";
					answer += "' end='" +new Date((long)(currPacketTime*1000)).toString()+"'>\n";
					for(String element : uniqueElementsPerWindow)
					{
						tempString = element.replace(";","&lt;br/&gt;");
						tempString = tempString.replace("\n","&lt;br/&gt;");
						answer += tempString;
					}
					answer += "\n</event>";
					currWindowStartTime = currPacketTime;
					uniqueElementsPerWindow.clear();
					//remove any unwanted elements from the array before storing in the map
					
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println("removed: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				} 
			}
			}
		}catch (Exception e) {
			e.printStackTrace();
		}
		answer += "</data>";
		return answer;
	}
	
		public static String formatJSONString(String buffer, double windowSize) {
		String answer = "[";
		String[] lines = buffer.split(System.getProperty("line.separator"));

		double currWindowStartTime = 0.0;
		double currPacketTime = 0.0;
		int packetsPerSecond = 0;
		String tempString;
		String[] parsedPacket;
		String timestamp;
		long packetsInWindow = 1;
		SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
		try {						
			//first grab the time_epoch from the line:
			if(lines.length > 1)
			{
				currWindowStartTime = Double.parseDouble(lines[0].split(" ",-1)[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);

			for (int i=0; i<lines.length; i++)
			{
				//System.out.println("line: " + lines[i]);
				parsedPacket = lines[i].split(" ",-1);
				currPacketTime = Double.parseDouble(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);;
				
				//This is the case when the data is still within the window size threshold, and there are still data left
				if((currPacketTime - currWindowStartTime) < windowSize && i != lines.length-1)
				{
					packetsInWindow++;
					//remove any unwanted elements from the array before storing in the map
					//System.out.println(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] );
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println(lines[i] + "\nremoved: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				}
				//The data is part of a new window because the log time is larger than the window size
				else
				{
				    timestamp = toFormat.format(new Date((long)(currWindowStartTime*1000)));
					//System.out.println("Starting new window");
					answer += "{ \"traffic_all_id\" : "+(numProtoItems++)+", ";
					answer += "\"content\" :\"";
					packetsPerSecond = (int)(packetsInWindow/windowSize);
					if(packetsPerSecond<1)
						answer+=quote("<1 p/s");
					else answer+=quote(packetsPerSecond+" p/s");
					answer += "\", ";
					
					answer += "\"className\" : \"traffic";
					answer += "\", ";
					
					answer += "\"title\" : \"";
					for(String element : uniqueElementsPerWindow)
					{
						tempString = element.replace(";","\n");
						tempString = quote(tempString);
						answer += tempString;
					}
					answer += "\", ";
										
					answer += "\"start\" : \"" + timestamp;
					if(i == lines.length-1){
						answer += "\" }\n";
					}
					else{
						answer += "\" },\n";
					}

					currWindowStartTime = currPacketTime;
					uniqueElementsPerWindow.clear();
					packetsInWindow = 1;
					//remove any unwanted elements from the array before storing in the map
					
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println("removed: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				} 
			}
			}
		}catch (Exception e) {
			e.printStackTrace();
		}
		answer += "]";
		return answer;
	}
		
	public static String formatJSONStringXY(String buffer, double windowSize) {
		String answer = "[";
		String[] lines = buffer.split(System.getProperty("line.separator"));
		double currWindowStartTime = 0.0;
		double currPacketTime = 0.0;
		int packetsPerSecond = 0;
		String tempString;
		String[] parsedPacket;
		String timestamp;
		long packetsInWindow = 1;
		SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
		try {
			//first grab the time_epoch from the line:
			if(lines.length > 1)
			{
				currWindowStartTime = Double.parseDouble(lines[0].split(" ",-1)[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);

			for (int i=0; i<lines.length; i++)
			{
				//System.out.println("line: " + lines[i]);
				parsedPacket = lines[i].split(" ",-1);
				currPacketTime = Double.parseDouble(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()]);;
				//System.out.println(lines[i]);
				if((currPacketTime - currWindowStartTime) < windowSize && i != lines.length-1)
				{
					packetsInWindow++;
					//remove any unwanted elements from the array before storing in the map
					//System.out.println(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] );
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println(lines[i] + "\nremoved: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				}
				else
				{
					//System.out.println("Starting new window");
					timestamp = toFormat.format(new Date((long)(currWindowStartTime*1000)));
					
					answer += "{ \"traffic_xy_id\" : "+(numXYItems++)+", ";
					answer += "\"className\" : \"trafficThroughput";
					answer += "\", ";
					answer += "\"x\":\"" + timestamp;
					answer += "\", ";
					
					answer += "\"y\" : ";
					packetsPerSecond = (int)(packetsInWindow/windowSize);
					answer+=packetsPerSecond;
					if(i == lines.length-1){
						answer += " }\n";
					}
					else{
						answer += " },\n";
					}


					currWindowStartTime = currPacketTime;
					uniqueElementsPerWindow.clear();
					packetsInWindow = 1;
					//remove any unwanted elements from the array before storing in the map
					
					lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_SRC.ordinal()], "");
					//lines[i] = lines[i].replace(parsedPacket[PacketData.Fields.ETH_DST.ordinal()], "");
					//System.out.println("removed: " + parsedPacket[PacketData.Fields.FRAME_TIMEEPOCH.ordinal()] + "\n");
					uniqueElementsPerWindow.add(lines[i]+"\n");
				} 
			}
			}
		}catch (Exception e) {
			e.printStackTrace();
		}
		answer += "]";
		return answer;
	}
	/**
	* Code adapted from Jettison JSONObject open source software:
	* http://grepcode.com/file/repo1.maven.org/maven2/org.codehaus.jettison/jettison/1.3.3/org/codehaus/jettison/json/JSONObject.java#JSONObject
	*/
	public static String quote(String string) {
         if (string == null || string.length() == 0) {
             return "";
         }

         char         c = 0;
         int          i;
         int          len = string.length();
         StringBuilder sb = new StringBuilder(len + 4);
         String       t;

         //sb.append('"');
         for (i = 0; i < len; i += 1) {
             c = string.charAt(i);
             switch (c) {
             case '\\':
             case '"':
                 sb.append('\\');
                 sb.append(c);
                 break;
             case '/':
 //                if (b == '<') {
                     sb.append('\\');
 //                }
                 sb.append(c);
                 break;
             case '\b':
                 sb.append("\\b");
                 break;
             case '\t':
                 sb.append("\\t");
                 break;
             case '\n':
                 sb.append("\\n");
                 break;
             case '\f':
                 sb.append("\\f");
                 break;
             case '\r':
                sb.append("\\r");
                break;
             default:
                 if (c < ' ') {
                     t = "000" + Integer.toHexString(c);
                     sb.append("\\u" + t.substring(t.length() - 4));
                 } else {
                     sb.append(c);
                 }
             }
         }
         //sb.append('"');
         return sb.toString();
     }
}
