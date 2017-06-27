package parsers;
import org.json.JSONException;
import org.json.JSONObject;

import utils.FileOutput;

/*
 	Uses https://github.com/stleary/JSON-java repository to convert xml nmap output file to its JSON representation.
  */

public class NmapDataParser {

	public static void main(String[] args) 
	{
		String xmlFilePath, outputFilePath;
		XMLToJSONBuilder json;
		
		if(args.length != 2)
		{
			System.out.println("Argument error.");
			System.out.println("Usage: java -jar xmlFilePath outputFilePath");
			return;
		}
		
		xmlFilePath = args[0];
	    outputFilePath = args[1];
		
		try
		{
			System.out.println("Parsing " + xmlFilePath + ", converting to " + outputFilePath);
			
			json = new XMLToJSONBuilder(xmlFilePath);
			FileOutput.WriteToFile(outputFilePath, json.getNmapJSON());
		}
		catch(JSONException e)
		{
			json = new XMLToJSONBuilder(xmlFilePath, true);
			FileOutput.WriteToFile(outputFilePath, json.getRawJSON()); //something went wrong, just return raw json
			System.out.println("An exception was thrown while trying to parse, returning raw json file instead...");
			System.out.println("Exception details: " + e.getMessage());
			
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}		
	}
}
