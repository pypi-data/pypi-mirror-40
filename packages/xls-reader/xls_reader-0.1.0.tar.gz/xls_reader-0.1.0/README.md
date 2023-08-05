[![Build Status](https://travis-ci.org/i2biz/xls-reader.svg?branch=master)](https://travis-ci.org/i2biz/xls-reader)

Description
===========

Sometimes you need to parse XLS files created by messy humans. 

This small tool is designed to do just that, it has following 
features: 

* It doesn't care about column order, it parses XLS header
  (essentially: first not empty row). 
* It tries to handle common errors such as: integer passed 
  as a string (in excel they are different types). 
* It handles empty rows inside the table. 
* If column is marked as not required, default can be returned. 
* If column is marked as not required it might be missing 
  altogether. 
* We try to report error precisely --- pinpointing the row and 
  column that caused it. 
  
Example
-------


See ``example_bindings`` folder.

Following code should parse 

    class DataColumns(Column):
    
      # A string column
      NAME = ColumnDescription(
        regex="Name", # Name is the column header
        reader=StringReader(attr_name="name")
      )
      PRICE_CENTS = ColumnDescription(
        regex="Price",
        reader=DecimalReader(attr_name="price")
      )
      
      
    class ExampleDataImporter(DataImporter):
      @classmethod
      def get_column_enum(cls) -> Column:
        return DataColumns
        
    importer = ExampleDataImporter()
    print(self.importer.read_file(file_path, sheet_name))
    
Should parse following simple example:

![Example](doc/example_xls.png)


Please see `xls_reader_test/*` for more. 

