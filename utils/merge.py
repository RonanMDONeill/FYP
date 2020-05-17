import datetime

def merge_csvs(inputDir, outputDir, prefix, outputFileName, splits, headers=True):
    """
    Merge the split CSV files for final use.
    
    inputDir (string): Location of the split data
    outputDir (string): Location for the output file
    prefix (string): Prefix which points towards the correct data type
    outputFileName (string): Name of the outputted file
    splits (integer): Number of files the input data has been split into
    headers (boolean): Whether the split files have headers or not (default is True)
    """
    
    # Define file structures
    inputPrefix = inputDir + prefix
    inputSuffix = ".csv"
    outputFile = outputDir + outputFileName + ".csv"
    
    print(str(datetime.datetime.now()) + ": Merge initiated.")
    
    if headers:
        with open(outputFile, "w", encoding="utf-8") as oFile:
            for x in range(splits):
                inputFile = inputPrefix + str(x+1) + inputSuffix
                with open(inputFile, encoding="utf-8") as iFile:
                    # Take headers from first file only
                    if x == 0:
                        oFile.write(iFile.read())   
                    else:
                        next(iFile)
                        for line in iFile:
                            oFile.write(line)
                
                print(str(datetime.datetime.now()) + ": " + inputFile + " merged.")
    else:
        with open(outputFile, "w", encoding="utf-8") as oFile:
            for x in range(splits):
                inputFile = inputPrefix + str(x+1) + inputSuffix
                with open(inputFile, encoding="utf-8") as iFile:
                    oFile.write(iFile.read())
                
                print(str(datetime.datetime.now()) + ": " + inputFile + " merged.")
            
    print(str(datetime.datetime.now()) + ": " + outputFileName + ".csv successfully merged.")