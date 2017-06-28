package parsers;

import utils.FileOutput;

/*
 	* Uses https://github.com/stleary/JSON-java repository to convert xml nmap output file to its JSON representation.
 	*
 	* As of now, the nmap command that generates the xml file is 'nmap -sP -oX {output_file_path} 10.0.0.0/24'.
 	* 	This returns a list of 'hosts' that were scanned for that ip range.
 	*   XMLToJSON builder will create an array of JSON objects with information about those hosts.
 	*   The format being:
 	*   				 [ {
 	*   						"nmap_id": ID of current obj,
 	*   						"start": start time of command,
 	*   						"className": name of command,
 	*   						"content": host information (address, address type, status...)
 	*   					},
 	*   					.....
 	*   				 ]
 	*   The format of the json follows that seen in the other collectors parsed json files.
 	*   If for any reason an there was an error thrown while parsing host data, the application will instead just output the raw json it
 	*   receieved from the output xml file.
 	* Returns an array of json objects
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
			System.out.println("Converting nmap xml file to JSON object...");
			json = new XMLToJSONBuilder(xmlFilePath);
			System.out.println("Writing json data to output file " +  outputFilePath + "...");
			FileOutput.WriteToFile(outputFilePath, json.getNmapJSON());
			System.out.println("Done...");
		}
		catch(Exception e)
		{
			System.out.println("An exception was thrown while trying to parse nmaps xml file, returning raw json file instead...");
			json = new XMLToJSONBuilder(xmlFilePath,true);
			FileOutput.WriteToFile(outputFilePath, json.getRawJSON());
			System.out.println("Exception details: " + e.getMessage());

		}		
	}
}
