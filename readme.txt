
  ov - data serialization format

  ov consist to five data type. name, number, string, array and object.
  your data must start with array or object at least.
  ov supports comments too. what you write in between /* and */ is ignored
  by parser. 

  types:
   - number:
     number type for all of kind of numbers.
     can consist of natural numbers and hexadecimal numbers and one minus 
     symbol and one plus symbol and one dot.

     valid numbers is [
            1  /* positive integer */
           -1  /* negative integer */
           +1  /* positive integer too but why someone want to use this? */
          1.5  /* positive float */
         -1.5  /* negative float */
       0b0001  /* binary */
       0xfeef  /* hexadecimal */
         0723  /* octal ( yes, it just start with zero ) */
     ]
     
  - string:
    everything between quotes is string 
    for example:
    	"kuesji koesnu"

    alias is name and kuesji koesnu is string in here.
    yes, we need a way to escape symbol if we want to use quote in string.
    you can use \" in this stiuation. only escape symbol is \" at the moment.
    if you want to \" in string too just use \\\", normally ov don't treat
    \\ is special in alone but if we use this before a quote it become special.
    so you get \ for every \\ before quote and if \ counts is odd it acts as
    escape for quote.

    so
      "hello\\\"" is escapes quote and string become hello"
    while
      "hello\\\\" is ends string and string become hello\\

  - array:
    it is just array of it contents. to declare array use [ and ].
    content must be valid types listed in this document.
    arrays not sorted by default.
    content is separated by space.

    for example:
      [ 1 2 3 4 5 ]
     or
      [ "house of red" "forest of green" "lake of blue" ]

  - object:
    it holds key-value pairs. key must be name or string.
    to declare object use { and }.
    object properties not sorted by default.
    everything ( between key-value and between pairs ) is separated by space.
    you must sure about every key has value and every value has key.

    for example:
      {
         "name" "kuesji koesnu"
         "username" "kuesji"
         "groups" [ 12 48 31 72 ]
      }
