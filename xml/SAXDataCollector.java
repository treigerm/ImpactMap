import javax.xml.parsers.*;
import org.xml.sax.*;
import org.xml.sax.helpers.*;

import java.util.*;
import java.io.*;

public class SAXDataCollector  extends DefaultHandler {

	private boolean checkA = false;
	private boolean checkB = false;
	private boolean pop = false;
	private boolean mobile = false;
	private boolean water = false;
	private static double pop_density = 0;
	private static double mobile_subs = 0;
	private static double water_access = 0;
  private boolean skip = false;

    public void startDocument() throws SAXException {
      ;
    }

    StringBuilder builder;

    public void startElement(String namespaceURI, String localName, String qName, Attributes atts) throws SAXException {

    	if (checkA && skip) {
        if (qName == "field") {
          if (atts.getValue("name").equals("Value")) {
            builder = new StringBuilder();
          }
        }     
      } else if (!(checkA && checkB)) {
    		if (qName == "field") {
    			try {
    				if (atts.getValue("key").equals("EN.POP.DNST")){
    					checkA = true;
    					pop = true;
    				} else if (atts.getValue("key").equals("SH.H2O.SAFE.RU.ZS")) {
    					checkA = true;
    					water = true;
    				} else if (atts.getValue("key").equals("IT.CEL.SETS.P2")) {
    					checkA = true;
    					mobile = true;
    				}
    			} catch (NullPointerException e) {
    				;
    			}
    		}
		}
    	
	}

	public void characters(char[] ch, int start, int length) {
   		try {
   			if (checkA && skip) {
   				builder.append(ch,start,length);
   				}
   			}
   		catch (NullPointerException e) {;}
	}

	public void endElement(String uri, String localName, String qName) {
  		try {
  			if (checkA && !skip) {
  				skip = true;
  			} else if (checkA && skip && !checkB) {
          checkB = true; //this just skips the year part
        } else if (checkA && checkB) {
  				String theFullText = builder.toString().replaceAll("\\s+","");
  				if (theFullText.length() > 0) {
  				  if (pop) pop_density = Double.parseDouble(theFullText);
  				  else if (mobile) mobile_subs = Double.parseDouble(theFullText);
  				  else if (water) water_access = Double.parseDouble(theFullText);
          }
          builder.setLength(0);
          pop = false;
          mobile = false;
          water = false;
          checkA = false;
          checkB = false;
          skip = false;
  			}
  		}
  		catch (NullPointerException e) {;}
	}

  public void endDocument() throws SAXException {
    ;
  }


	private static String convertToFileURL(String filename) {
        String path = new File(filename).getAbsolutePath();
        if (File.separatorChar != '/') {
            path = path.replace(File.separatorChar, '/');
        }

        if (!path.startsWith("/")) {
            path = "/" + path;
        }
        return "file:" + path;
    }

  public static double getPopDensity() {
    return pop_density;
  }

  public static double getMobileSubs() {
    return mobile_subs;
  }

  public static double getWaterAccess() {
    return water_access;
  }

  public static void nullify() {
    pop_density = 0;
    mobile_subs = 0;
    water_access = 0;
  }

	static public void main(String[] args) throws Exception {
    	String filename = null;
      String country;
      double pop, mobile, water;
      PrintWriter writer = new PrintWriter("countries.xml", "UTF-8");
      writer.println("<?xml version=\"1.0\" ?>");
      writer.println("<Countries>");
    	for (int i = 0; i < args.length; i++) {
        
        filename = args[i];
        SAXParserFactory spf = SAXParserFactory.newInstance();
        spf.setNamespaceAware(true);
        SAXParser saxParser = spf.newSAXParser(); 
        XMLReader xmlReader = saxParser.getXMLReader();
        xmlReader.setContentHandler(new SAXDataCollector());
        xmlReader.parse(convertToFileURL(filename));

        country = filename.replaceAll(".xml","");
        writer.println(String.format("    <Country>"));
        pop = SAXDataCollector.getPopDensity();
        mobile = SAXDataCollector.getMobileSubs();
        water = SAXDataCollector.getWaterAccess();
        SAXDataCollector.nullify();
        writer.println("        <Name>" + country + "</Name>");
        if (pop != 0) {
          writer.println("        <PopulationDensity>" + pop + "</PopulationDensity>");
        } else {
          writer.println("        <PopulationDensity/>");
        }
        if (mobile != 0) {
          writer.println("        <MobileOwners>" + mobile + "</MobileOwners>");
        } else {
          writer.println("        <MobileOwners/>");
        }
        if (water != 0) {
          writer.println("        <WaterAccess>" + water + "</WaterAccess>");
        } else {
          writer.println("        <WaterAccess/>");
        }
        writer.println("    </Country>");
    	}
      writer.println("</Countries>");
      writer.close();
	}
}