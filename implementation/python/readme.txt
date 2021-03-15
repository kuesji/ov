
  ov.py - ov library in python

  functions:
    - load(data)
      takes a string with valid ov data and returns list or dict depending on data

		  returns list or dict depending on data on success 
      returns a tuple with first element is None and second element is error detail  dict on fail

    - save(data)
      takes dict,list and converts to valid ov string
      don't pass anything else than int, float, string, list, dict inside data

      returns valid ov string on success
      returns a tuple with first element is None and second element is error detail dict on fail


  warning: 
    - if you wanna thinking about passing weird data to load function
    ensure you wrapped in the try/catch . load can be raise index errors
      
    - tuple used for parsing internals, passing tuple to these functions
    will make things worse.
