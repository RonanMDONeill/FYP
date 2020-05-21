import json
import math
import datetime

def replace_special_char(oldString):
    """"
    Replaces special characters for Neo4j compatibility
    
    oldString (string): String for replacement
    """

    if oldString[-1:] == "\\":
        oldString = oldString[:-1] + "..."

    return oldString.replace("\"", "'")

def wrap_string(oldString):
    """"
    Wraps strings with " for Neo4j
    
    oldString (string): String for wrapping
    """
    
    return "\"" + oldString + "\""

def split_dataset(file, numRows, splits, output, badIDs):
    """"
    Splits the DBLP dataset into smaller chunks for easier manipulation.
    Dataset will be split into relationship and detail content and textual content.
    
    file (string): Directory location of the dataset
    numRows (integer): Number of rows within the dataset
    splits (integer): Number of times to split the dataset
    output (string): Directroy location of the output files
    badIDs (list of strings): List of the corrupted entries identified in the dataset
    """
    
    # Initialize count and file number variables
    count = 0
    fileNo = 1
    
    # Calculate the limit for an output file
    splitLimit = int(math.ceil(numRows/splits))
    
    # Define output file name structure
    rdPrefix = output + "Split_DBLP_RD_"
    textPrefix = output + "Split_DBLP_Text_"
    rdSuffix = ".csv"
    textSuffix = ".json"
    
    # CSV file headers
    rdHeader = "id,title,year,publisher,doi,authorsName,authorsID,venueName,venueID,fosName,fosWeight,references,n_citation"
    textHeader = "id,title,fosNames,Abstract"
    
    print(str(datetime.datetime.now()) + ": Splitting initiated.")
    
    # Open the original dataset and parse line by line
    with open(file) as f:
        for line in f:
            # Read in line as JSON object
            jsonLine = json.loads(line)
            
            # Get details for paper
            # Not every detail is stored for each paper, so use try except methods
            paperID = str(jsonLine["id"])
            
            # If ID is in list of bad IDs, skip
            if paperID in badIDs:
                print("Bad ID caught: " + paperID + ".")
                continue

            paperID = wrap_string(paperID)
            
            title = replace_special_char(str(jsonLine["title"]))
            titleText = title
            title = wrap_string(title)
            
            year = ""
            try:
                year = wrap_string(str(jsonLine["year"]))
            except KeyError:
                pass
            
            publisher = ""
            try:
                publisher = wrap_string(replace_special_char(str(jsonLine["publisher"])))
            except KeyError:
                pass
            
            doi = ""
            try:
                doi = wrap_string(replace_special_char(str(jsonLine["doi"])))
            except KeyError:
                pass
            
            references = ""
            try:
                # Split list and add to string seperated by commas
                for index, ref in enumerate(jsonLine["references"]):
                    if index > 0:
                        references += ","
                    references += str(ref)
                references = wrap_string(references)
            except KeyError:
                pass
                
            authorsName = ""
            authorsID = ""
            try:
                for index, auth in enumerate(jsonLine["authors"]):
                    if index > 0:
                        authorsName += ","
                        authorsID += ","
                    authorsName += str(auth["name"])
                    authorsID += str(auth["id"])
                
                authorsName = wrap_string(replace_special_char(authorsName))
                authorsID = wrap_string(authorsID)
            except KeyError:
                pass
            
            venueName = ""
            venueID = ""
            try:
                venueName = wrap_string(replace_special_char(str(jsonLine["venue"]["raw"])))
                if jsonLine["venue"]["id"]:
                    venueID = wrap_string(str(jsonLine["venue"]["id"]))
            except KeyError:
                pass
            
            fosName = ""
            fosNameText = ""
            fosWeight = ""
            try:
                for index, fos in enumerate(jsonLine["fos"]):
                    if index > 0:
                        fosName += ","
                        fosWeight += ","
                    fosName += str(fos["name"])
                    fosWeight += str(fos["w"])
                fosName = replace_special_char(fosName)
                fosNameText = fosName
                fosName = wrap_string(fosName)
                fosWeight = wrap_string(fosWeight)
            except KeyError:
                pass
            
            n_citation = ""
            try:
                n_citation = wrap_string(str(jsonLine["n_citation"]))
            except KeyError:
                pass
            
            abstract = ""
            try:
                iA = jsonLine["indexed_abstract"]["InvertedIndex"]
                # Add every word to the abstract variable as many times as it appears in the inverted abstract
                for word in iA:
                    for x in range(len(iA[word])):
                        abstract += str(word) + " "
            except KeyError:
                pass

            textDict = {
                "paperID": paperID,
                "title": title,
                "fosNames": fosNameText,
                "abstract": abstract
            }
            
            # Attach details to split files
            if count == 0:
                # Add header to each csv file
                rdOutFile = rdPrefix + str(fileNo) + rdSuffix
                textOutFile = textPrefix + str(fileNo) + textSuffix
                
                with open(rdOutFile, "w", encoding="utf-8") as oFile:
                    oFile.write(rdHeader)
                    oFile.write("\n")
                    oFile.write(paperID+","+title+","+year+","+publisher+","+doi+","+authorsName+","+authorsID+","+venueName+","+venueID+","+fosName+","+fosWeight+","+references+","+n_citation)
                    oFile.write("\n")
                    
                with open(textOutFile, "w", encoding="utf-8") as oFile:
                    json.dump(textDict, oFile)
                    oFile.write("\n")
                
            else:
                with open(rdOutFile, "a", encoding="utf-8") as oFile:
                    oFile.write(paperID+","+title+","+year+","+publisher+","+doi+","+authorsName+","+authorsID+","+venueName+","+venueID+","+fosName+","+fosWeight+","+references+","+n_citation)
                    oFile.write("\n")
                    
                with open(textOutFile, "a", encoding="utf-8") as oFile:
                    json.dump(textDict, oFile)
                    oFile.write("\n")

            count += 1
                    
            if count == splitLimit:
                count = 0
                fileNo += 1
                print(str(datetime.datetime.now()) + ": Split " + str(fileNo - 1) + " complete.")

    print(str(datetime.datetime.now()) + ": Split " + str(fileNo) + " complete.")
    
    print(str(datetime.datetime.now()) + ": Dataset split.")