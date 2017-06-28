package parsers;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.XML;

public class XMLToJSONBuilder
{
	private static final String PRIMARY_KEY = "nmaprun", ITERABLE_KEY = "host", START_KEY = "startstr";
	private	static final String ID_FIELD = "nmap_id", CONTENT_FIELD = "content",
								START_FIELD = "start", CLASS_NAME_FIELD = "className", CLASS_NAME_VALUE = "nmap";
	private static final int INDENT_FACTOR = 4;
	private JSONObject json, rawJSON;
	private JSONArray iterable;
	private String xml, startTime;
	private StringBuilder nmapJSON;


	public XMLToJSONBuilder(String filePath)
	{
		this.xml = buildXMLString(filePath);
		this.rawJSON = xmlToJSON(xml);
		this.json = this.rawJSON.getJSONObject(PRIMARY_KEY);
		this.iterable = this.json.getJSONArray(ITERABLE_KEY);
		this.startTime = this.json.getString(START_KEY);
		this.nmapJSON = new StringBuilder();
		buildNmapJSON();
	}

	public XMLToJSONBuilder(String filePath, boolean useRaw)
	{
		this.xml = buildXMLString(filePath);
		this.rawJSON = xmlToJSON(xml);

	}

	public String getRawJSON()
	{
		return this.rawJSON.toString(INDENT_FACTOR);
	}

	private String buildXMLString(String filePath)
	{
	    StringBuilder xml = new StringBuilder();
	    BufferedReader br = null;
	    String line;

	    try
	    {
	    	br = new BufferedReader(new FileReader(new File(filePath)));
			while((line=br.readLine())!= null)
			{
			    xml.append(line.trim());
			}
	    }
	    catch (Exception e)
	    {
	    	e.printStackTrace();
	    }

	    return xml.toString();
	}

	private JSONObject xmlToJSON(String xml)
	{
	   return XML.toJSONObject(xml);
	}
	
	public String getNmapJSON()
	{
		return this.nmapJSON.toString();
	}
	
	private void buildNmapJSON()
	{
		    boolean appendEndString;
		    String endString, data;
		    
		    System.out.println("Building nmap json file...");
		    
		    this.nmapJSON.append("[");
		    
		    for(int i = 0; i < this.iterable.length(); i++)
		    {
			    appendEndString = i < this.iterable.length() - 1;
			    data = this.iterable.getJSONObject(i).toString(INDENT_FACTOR);
			    
				this.nmapJSON.append("{" + (appendKeyValuePair(ID_FIELD, (i+1),"int")));
				this.nmapJSON.append(",");
				this.nmapJSON.append((appendKeyValuePair(CONTENT_FIELD, data,"obj")));
				this.nmapJSON.append(",");
				this.nmapJSON.append((appendKeyValuePair(START_FIELD, this.startTime,"String")));
				this.nmapJSON.append(",");
				this.nmapJSON.append((appendKeyValuePair(CLASS_NAME_FIELD, CLASS_NAME_VALUE ,"String")));
				endString = (appendEndString ? "}, " : "}");
				
				this.nmapJSON.append(endString);			
		    }
		    
		this.nmapJSON.append("]");
		System.out.println("Done.");
	}
	
	private String appendKeyValuePair(String key, Object value, String type)
	{
	    switch(type)
	    {
	    	case "int": return "\"" + key + "\":" + (int)value;
	    	case  "obj":  return "\"" + key + "\":" + (String)value;
	    	default: return "\"" + key + "\":" + "\"" + (String)value + "\"" ;
	    }
	}
	
}
