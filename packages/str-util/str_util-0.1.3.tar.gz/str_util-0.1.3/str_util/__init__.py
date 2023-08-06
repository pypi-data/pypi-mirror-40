import fnmatch  # used by the like function
import re  # used by the replace_substring function

name = "str_util"


def to_string(value):
    """
    Convert a value to a string. Same as ``str(value)``

    :param any value: the value to convert
    :return: the value converted to a string

    >>> to_string( 5 )
    '5'

    """
    return str(value)


def to_list(value):
    """
    Convert a value to a list. Similar to ``list(value)``, but also works on existing lists

    :param any value: the value to convert
    :return: the value converted to a string

    >>> to_list( "Hello")
    ['Hello']

    >>> to_list(["Hello"])
    ['Hello']

    """
    if is_list(value):
        return value
    return [value]


def is_string(value):
    """
    Tests the value to determine whether it is a string.

    :param any value:
    :return: True of the value is a string (an instance of the str class)

    >>> is_string( 'Hello' )
    True

    >>> is_string( ['Hello'] )
    False

    """
    return isinstance(value, str)


def is_list(value):
    """
    Tests the value to determine whether it is a list.

    :param any value:
    :return: True of the value is a list (an instance of the list class)

    >>> is_list( 'Hello' )
    False

    >>> is_list( ['Hello'] )
    True

    """
    return isinstance(value, list)


def trim(value):
    """
    Removes leading, trailing, and redundant spaces/whitespace from a text string, or from each element of a text list.

    :param str,list value: text or text list
    :return: The value, with extra spaces and empty elements removed.
    :rtype: str,list

    Remove all redundant whitespace from string
    >>> trim('A  B C   ')
    'A B C'

    Trim all entries in list and remove empty entries
    >>> trim(['Hello   ', '  ', '   World'])
    ['Hello', 'World']

    >>> trim( [''])
    []

    """
    if is_list(value):
        trimmed = list(map(trim, value))  # trim all entries in list
        return list(filter(lambda entry: entry != '', trimmed))  # remove empty entries
    return " ".join(value.split())  # trim string


def unique(source_list, ignore_case=False):
    """
    Removes duplicate values from a list of strings by returning only the first occurrence of each member of the list.
    :param list source_list: Any text list
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: List with unique members
    :rtype: list

    >>> unique( ['A','B','C','B','A'])
    ['A', 'B', 'C']

    >>> unique( ['red','green','Red','green'])
    ['red', 'green', 'Red']

    >>> unique( ['red','green','Red','green'], True)
    ['red', 'green']

    """
    if ignore_case:
        unique_list = []
        for entry in source_list:
            if not is_member(entry, unique_list, ignore_case=True):
                unique_list.append(entry)
        return unique_list
    return list(dict.fromkeys(source_list))


def is_empty(value):
    """
    Return true is value is empty or only contains whitespace

    >>> is_empty( "   " )
    True

    >>> is_empty( None )
    True

    >>> is_empty(['  '])
    True

    """
    if value is None:
        return True
    if is_list(value):
        return trim(value) == []
    return value.strip() == ''


def contains(value, substrings, ignore_case=False):
    """
    Determine if a string contains any of the substrings

    :param value: (str or list) The string you want to search in
    :param substrings: (str or list) The string(s) you want to search for in string.
    :param bool ignore_case: Optional. Specify True to perform a case-insensitive search (default False)

    >>> contains( "Hello World", "world")
    False

    >>> contains( "Hello World", "wORLd", True)
    True

    >>> contains( "Red Blue Yellow Green", ['Black', 'Low'], ignore_case=True)
    True

    >>> contains( ['ABC', 'DEF'], ['B'])
    True

    A blank string is always contained
    >>> contains( "Red Blue Yellow Green", ['Rubbish', ''])
    True

    """
    if is_list(value):
        return any([contains(entry, substrings, ignore_case) for entry in value])

    substrings = to_list(substrings)
    if ignore_case:
        return any([entry.casefold() in value.casefold() for entry in substrings])
    return any([entry in value for entry in substrings])


def contains_all(value, substrings, ignore_case=False):
    """
    Determine if a string contains all of the substring substrings

    :param value: (str or list) The string you want to search in
    :param substrings: (str or list) The string(s) you want to search for in string.
    :param bool ignore_case: Optional. Specify True to perform a case-insensitive search (default False)

    >>> contains_all( "Hello World", "Wo")
    True

    >>> contains_all( "Hello World", "world", True)
    True

    >>> contains_all( "Red Blue Yellow Green", ['Black', 'Red'])
    False

    >>> contains_all( "Red Blue Yellow Green", ['LUE', 'red'], True)
    True

    >>> contains_all( ["Red Blue", "Yellow Green"], ['Blue', 'red'], True)
    True

    """
    if is_list(value):
        return any([contains_all(entry, substrings, ignore_case) for entry in value])

    substrings = to_list(substrings)
    if ignore_case:
        return all([entry.casefold() in value.casefold() for entry in substrings])
    return all([entry in value for entry in substrings])


def index_of(value, substring, ignore_case=False, reverse=False):
    """
    Find the first occurrence of the substring and return the position, If not found, return -1
    First character in the string(first element in list has position = 0

    :param str,list value: the source to search in
    :param str substring: the substring to search for in the source value
    :param bool ignore_case: Optional. Specify True to perform a case-insensitive search (default False)
    :param bool reverse: Optional. Specify True to search backwards (default False)
    :return: Position of the first occurrence of the substring in the string or list. Returns 0 if not found
    :rtype: str,list

    >>> index_of( 'Jakob','a')
    1

    >>> index_of( 'Jakob','K')
    -1

    >>> index_of( 'Jakob','K', ignore_case=True)
    2

    >>> index_of( ['Red', 'Green','Blue'], 'green', ignore_case=True)
    1

    >>> index_of( "This is key: FIS", "is", reverse=True)
    5

    >>> index_of( "This is key: FIS", "is")
    2

    >>> index_of( "This is key: FIS", "is", reverse=True, ignore_case=True)
    14

    """
    if is_list(value):
        for i, entry in enumerate(value):
            if is_equal(entry, substring, ignore_case):
                return i
        return -1

    if ignore_case:
        value = value.casefold()
        substring = substring.casefold()
    if reverse:
        return value.rfind(substring)
    return value.find(substring)


def implode(strings, separator=''):
    """
    Concatenate all member of a list into a single string by a separating delimiter.
    Similar to ``separator.join(strings)`` but doesn't treat a single string as a list

    :param list strings: strings to concatenate
    :param str separator: Optional. The delimiter (default='')
    :return: String

    >>> implode( ['a','b','c'])
    'abc'

    >>> implode( ['Hello','World'], ' ')
    'Hello World'

    >>> implode( 'Hi', '.' )
    'Hi'
    """
    if is_list(strings):
        return separator.join(strings)
    return strings


def propercase(value):
    """
    Converts the words in a string to proper­name capitalization: the first letter of each word becomes uppercase,
    the rest become lowercase.

    :param str,list value: The string you want to convert.

    >>> propercase('hELLO wORLD')
    'Hello World'

    >>> propercase(['blue','RED','very grEEn'])
    ['Blue', 'Red', 'Very Green']

    """
    if is_list(value):
        return [propercase(entry) for entry in value]
    return implode([entry.capitalize() for entry in value.split()], ' ')


def left(value, find, ignore_case=False):
    """
    Searches a string from left to right and returns the leftmost characters of the string.

    :type value: str or list
    :param value: The string where you want to find the leftmost characters.
    :type find: str or int
    :param find:
        * [str] a substring to search for.
          Function returns all characters to the left of *find*
        * [int] number of leftmost chars to return.

    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: the leftmost characters of string
    :rtype: str or list

    Return the first two characters

    >>> left( "Hello World", 2 )
    'He'

    If number if greater then the length of the string, then the whole string is returned

    >>> left( "Hello", 10 )
    'Hello'

    Use a negative number to count from the back, just like the :func:`~left_back` function

    >>> left( "Hello World", -3 )
    'Hello Wo'

    If the *find* string is not found, then an empty string is returned

    >>> left( "Happy Birthday", "XYZ")
    ''

    Return everything until the letter 'l'

    >>> left( "Hello World", "l")
    'He'

    Also works on list's

    >>> left( ["Jakob","Majkilde"], 2)
    ['Ja', 'Ma']

    """
    if is_list(value):
        return [left(entry, find) for entry in value]

    if isinstance(find, int):
        if find > 0:
            return value[:find]
        return value[:find]

    pos = index_of(value, find, ignore_case)
    if pos > 0:
        return left(value, pos)
    return ""


def left_back(value, find, ignore_case=False):
    """
    As :func:`~left` but counts/searches from the back

    :type value: str or list
    :param value: The string where you want to find the leftmost characters.
    :type find: str or int
    :param find:
        * [str] a substring to search for. Left return all character to the left of *find*
        * [int] return the leftmost characters from the string, skipping the *find* leftmost
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: the leftmost characters of string
    :rtype: str or list

    Skip the last 3 characters

    >>> left_back( "Hello World", 3 )
    'Hello Wo'

    If *count* is greater than the length of the string, then return an empty string

    >>> left_back( "Hello", 10 )
    ''

    if *count* is negative, then return the whole string

    >>> left_back( "Hello World", -2 )
    'Hello World'

    return an empty string if the search string is not found

    >>> left_back( "Happy Birthday", "XYZ")
    ''

    Return leftmost characters until the last occurrence of the letter 'l'

    >>> left_back( "Hello World", "l")
    'Hello Wor'

    """
    if is_list(value):
        return [left_back(entry, find) for entry in value]

    if isinstance(find, int):
        if find > 0:
            if find > len(value):
                return ''
            return value[:len(value) - find]
        return value
    pos = index_of(value, find, ignore_case, reverse=True)
    if pos >= 0:
        return left(value, pos)
    return ""


def is_member(source_list, search_list, ignore_case=False):
    """
    Check if the source_list is a subset of the search_list

    :type source_list: list or str
    :param source_list:
    :type search_list: list or str
    :param search_list:
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: True if all members of the source_list can be found in the search_list


    >>> is_member('Admin', ['Owner', 'Admin', 'Reader'])
    True

    >>> is_member( ['Jakob','Maiken'], ['Maiken','Amalie','Jakob','Ida'])
    True

    """
    search_list = to_list(search_list)
    if is_list(source_list):
        return all([is_member(entry, search_list, ignore_case) for entry in source_list])
    if ignore_case:
        return is_member(lowercase(source_list), lowercase(search_list))
    return source_list in search_list


def lowercase(value):
    """
    Converts a string or list of strings to lowercase.
    Like the `casefold <https://www.programiz.com/python-programming/methods/string/casefold>`_ function, but also works on lists.

    :type value: str or list
    :param value: the string to convert to lowercase
    :return: the source string converted to lowercase
    :rtype: str or list

    >>> lowercase("Der Fluß")
    'der fluss'

    >>> lowercase( ['Green','RED','bluE'])
    ['green', 'red', 'blue']

    """
    if is_list(value):
        return [entry.casefold() for entry in value]
    return value.casefold()


def right(value, find, ignore_case=False):
    """
    Searches a string from left to right and returns the rightmost characters of the string.

    :type value: str or list
    :param value: The string where you want to find the rightmost characters.
    :type find: str or int
    :param find:
        * [str] a substring to search for.
          Function returns all characters to the right of *find*
        * [int] skip the first *count* characters and returns the rest.

    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: the rightmost characters of string
    :rtype: str or list

    Skip the first three characters and return the rest

    >>> right( "Hello World", 3 )
    'lo World'

    If *count* is greater then the length of the string, then return a blank

    >>> right( "Hello", 10 )
    ''

    If *count* is negative the count from the back - just like :func:`right_back`

    >>> right( "Hello World", -2 )
    'ld'

    if the search string is not found, a blank is returned
    >>> right( "Happy Birthday", "XYZ")
    ''

    Return all characters to the right of the first occurrence of the letter 'l'

    >>> right( "Hello World", "l")
    'lo World'

    Also works on list's

    >>> right( ["Jakob","Majkilde"], 'j')
    ['', 'kilde']

    """
    if is_list(value):
        return [right(entry, find) for entry in value]

    if isinstance(find, int):
        if find > len(value):
            return ''
        if find > 0:
            return value[find:]
        return value[find:]
    pos = index_of(value, find, ignore_case)
    if pos >= 0:
        return right(value, pos + len(find))
    return ""


def right_back(value, find, ignore_case=False):
    """
    Searches a string from the back (right to left) and returns the rightmost characters.

    :type value: str or list
    :param value: The string where you want to find the rightmost characters.
    :type find: str or int
    :param find:
        * [str] a substring to search for.
          Function returns all characters to the right of the last occurrence of *find*
        * [int] return the *count* characters of the string.

    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: the rightmost characters of string
    :rtype: str or list


    Return the last 3 characters of the string

    >>> right_back( "Hello World", 3 )
    'rld'

    If *count* is greater than the length of the return, then the whole string is returned

    >>> right_back( "Hello", 10 )
    'Hello'

    if *count* is negative, then return an empty string

    >>> right_back( "Hello World", -2 )
    'Hello World'


    Return everything to the right of the last occurrence of the letter 'l'

    >>> right_back( "Hello World", "l")
    'd'

    Also works on list's

    >>> right_back( ["Jakob","Majkilde"], 2)
    ['ob', 'de']


    """
    if is_list(value):
        return [right_back(entry, find) for entry in value]

    if isinstance(find, int):
        if find > len(value):
            return value
        if find > 0:
            return value[-find:]
        return value
    pos = index_of(value, find, ignore_case, reverse=True)
    if pos >= 0:
        return right(value, pos + len(find))
    return ""


def word(value, number, separator=None):
    """
    Returns a specified word from a text string. Words are by default separated by whitespace.
    First word in a sentence is number 1

    :type value: str or list
    :param value: the sentence to be scanned
    :param number:  A position indicating which word you want returned from string. 1 is the first word in the sentence
        and -1 is the last word
    :param separator: Optional (default is any whitespace)
    :return: the selected word
    :rtype: str or list


    Get the second word in a sentence

    >>> word( "Some text here", 2)
    'text'

    Get the fifth word in a senctence with only three words

    >>> word( "Some text here", 5)
    ''

    Return the last word from a sentence, e.g. the lastname of the username

    >>> word( "Jakob Majkilde", -1)
    'Majkilde'

    Get the second word in a sentence, using a custom separator

    >>> word( "North, West, East", 2, ", ")
    'West'

    Also works on list's 

    >>> word( ["North, West, East", 'Scandinavia, UK, China'], 2, ", ")
    ['West', 'UK']

    """
    if is_list(value):
        return [word(entry, number, separator) for entry in value]
    tokens = value.split(separator)
    index = number - 1 if number > 0 else number
    if index >= len(tokens):
        return ''
    return tokens[index]


def is_equal(value1, value2, ignore_case=False):
    """
    Compare two values and returns trues if they are equal

    :type value1: list or str
    :param value1: first list
    :type value2: list or str
    :param value2: second list
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)

    :return: true if the two values is equal
    :rtype: bool


    Match with ignore case

    >>> is_equal("Der Fluß", "DER fluss", ignore_case=True )
    True

    List in random order is still euqal

    >>> is_equal(['a','b','c'], ['c','b','a'])
    True

    Both list must contain all elements

    >>> is_equal(['b','c'], ['c','b','a'])
    False


    """
    list1 = to_list(value1)
    list2 = to_list(value2)
    cmp = intersection(list1, list2, ignore_case)
    return len(cmp) == len(list1) == len(list2)


def compare(string1, string2, ignore_case=False):
    """
    Compares two strings

    :param str string1: first string
    :param str string2: second string
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return:
        * string1 is less than string2: return	  -1
        * string1 equals string2: return	   0
        * string1 is greater than string2: return	   1

    :rtype: int

    Compare two strings. Banana comes after Apple in the alphabeth and therefor :func:`compare` return 1 (for greater)

    >>> compare( 'Banana','Apple')
    1

    These two strings are equal when ignore_case is true

    >>> compare( "Der Fluß", "DER fluss", ignore_case=True)
    0

    """
    if ignore_case:
        string1 = lowercase(string1)
        string2 = lowercase(string2)
    if string1 < string2:
        return -1
    if string1 > string2:
        return 1
    return 0


def _replace_str(string, fromlist, tolist, ignore_case=False):
    """
    if string is found in fromlist then replace with the corresponding value in tolist

    :param string: the source string to be replaced
    :param fromlist: the list to search in
    :param tolist: the list of strings to replace with
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: replaced value
    :rtype: str

    >>> _replace_str( 'HELLO', ['Hej', 'Hi', 'Hello'], ['Greeting'], ignore_case=True)
    'Greeting'

    >>> _replace_str( 'Apple', 'Microsoft', 'IBM')
    'Apple'

    >>> _replace_str( 'Apple', 'Apple', 'IBM')
    'IBM'


    """
    fromlist = to_list(fromlist)
    tolist = to_list(tolist)
    idx = index_of(fromlist, string, ignore_case)
    if idx >= 0:
        if idx >= len(tolist):
            return tolist[-1]
        return tolist[idx]
    return string


def replace(source, fromlist, tolist, ignore_case=False):
    """
    Performs a search-and-replace operation on a list.

    :type source: list or str
    :param source: The list whose values you want to replace
    :type fromlist: list or str
    :param fromlist: Values to search for
    :type tolist: list or str
    :param tolist: Values to replace with

    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: new list with replaced values
    :rtype: list

    Replace Apple with Microsoft

    >>> replace( ['Lemon','Apple','Orange'], 'Apple','Microsoft')
    ['Lemon', 'Microsoft', 'Orange']

    >>> replace( ['red', 'yellow', 'green', 'blue'], ['red', 'green', 'blue'], ['purple', 'silver'] )
    ['purple', 'yellow', 'silver', 'silver']

    """
    source = to_list(source)

    return [_replace_str(entry, fromlist, tolist, ignore_case) for entry in source]


def _make_equal_length(list1, list2):
    """
    Returns two new lists, where len(list1)=length(list2)
    If a list is too short, then the last element is repeated until the length matches the other string

    :param list1: First list
    :param list2: Second list
    :return: tuple with the two new list's (list1, list2)
    :rtype: (list, list)

    >>> _make_equal_length( 'string', ['value1', 'value2'])
    (['string', 'string'], ['value1', 'value2'])

    >>> _make_equal_length(['_','&'], ' ')
    (['_', '&'], [' ', ' '])
    """
    list1 = to_list(list1)
    list2 = to_list(list2)

    while len(list1) < len(list2):
        list1.append(list1[-1])

    while len(list2) < len(list1):
        list2.append(list2[-1])

    return list1, list2


def replace_substring(source, fromlist, tolist, ignore_case=False):
    """
    Replaces specific words in a string or list with new words

    :type source: list or str
    :param source: Source to be updated with new words
    :type fromlist: list or str
    :param fromlist: Values to search for
    :type tolist: list or str
    :param tolist: Values to replace with
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: string/list where all value in *fromlist* is replaced with the corresponding values in *tolist*
    :rtype: list or str

    >>> replace_substring("Like: I like that you like me", "like", "love")
    'Like: I love that you love me'

    >>> replace_substring('I want a hIPpo for my birthday', 'hippo', 'giraffe', ignore_case=True)
    'I want a giraffe for my birthday'

    >>> replace_substring(['Hello World', 'a b c'], ' ', '_')
    ['Hello_World', 'a_b_c']

    >>> replace_substring('Odd_looking&text!', ['_','&'], ' ')
    'Odd looking text!'

    >>> replace_substring('Encode: &', [' ','&'], ['%20','&amp;'])
    'Encode:%20&amp;'

    >>> replace_substring( "I like apples", ["like", "apples"], ["hate", "peaches"])
    'I hate peaches'


    """
    if is_list(source):
        return [replace_substring(entry, fromlist, tolist, ignore_case) for entry in source]

    fromlist, tolist = _make_equal_length(fromlist, tolist)

    options = '(?i)' if ignore_case else ''

    for i, from_str in enumerate(fromlist):
        source = re.sub(options + re.escape(from_str), lambda m: tolist[i], source)
    return source


def diff(list1, list2, ignore_case=False):
    """
    Remove elements in list2 from list1

    :type list1: list or str
    :param list1: first list
    :type list2: list or str
    :param list2: second list
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)

    :return: copy of list1 without the elements found in list2
    :rtype: list


    >>> diff( ['A','B','C'], ['A','D', 'c'])
    ['B', 'C']

    >>> diff( ['A','B','C'], 'B')
    ['A', 'C']

    >>> diff( ['A','B','C'], ['A','D', 'c'], ignore_case=True)
    ['B']

    """
    list1 = to_list(list1)
    list2 = to_list(list2)
    return [entry for entry in list1 if not is_member(entry, list2, ignore_case)]


def union(list1, list2):
    """
    Adds two list

    :type list1: list or str
    :param list1: first list
    :type list2: list or str
    :param list2: second list
    :return: new list with all elements from both list1 and list2
    :rtype: list

    >>> union( ['A','B','C'], ['A','D','c'])
    ['A', 'B', 'C', 'A', 'D', 'c']

    >>> union( 'Hello', 'World')
    ['Hello', 'World']

    """
    final_list = to_list(list1) + to_list(list2)
    return final_list


def intersection(list1, list2, ignore_case=False):
    """
    Intersection of the two given list's is a list which consists of all the elements which are
    common to both list1 and list2.

    :type list1: list or str
    :param list1: first list
    :type list2: list or str
    :param list2: second list
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: list with common elements
    :rtype: list

    >>> intersection( ['A','B','C'], ['A','D', 'c'])
    ['A']

    >>> intersection( ['A','B','C'], ['A','D', 'c'], ignore_case=True)
    ['A', 'C']

    >>> intersection("Der Fluß", "DER fluss", ignore_case=True)
    ['Der Fluß']

    """
    list1 = to_list(list1)
    list2 = to_list(list2)
    return [entry for entry in list1 if is_member(entry, list2, ignore_case)]


def like(string, pattern, ignore_case=False):
    """
    Matches a string with a pattern

    :param str string: the value to be tested
    :param str pattern: the pattern. Use ? for any char or * for any sentence.
        More info: `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_

    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :return: True if the *pattern* matches the *string*
    :rtype: bool

    >>> like( 'Jakob', 'jakob')
    False

    >>> like( 'Jakob', 'ja?ob', ignore_case=True)
    True

    >>> like( ['Petersen','Pedersen','Peter', 'Olsen'],"Pe?er*" )
    [True, True, True, False]

    """
    if is_list(string):
        return [like(entry, pattern, ignore_case) for entry in string]
    if ignore_case:
        return fnmatch.fnmatch(string, pattern)
    return fnmatch.fnmatchcase(string, pattern)


def sort(source_list, ignore_case=False, reverse=False):
    """

    :param list source_list: The list to sort
    :param bool ignore_case: Optional. Specify true to ignore case (Default False)
    :param bool reverse: Optional. Specify True to sort the list in descending order (Default False)
    :return: The sorted list
    :rtype: list

    >>> sort( ['Bad','bored','abe','After'])
    ['After', 'Bad', 'abe', 'bored']

    >>> sort( ['Bad','bored','abe','After'], ignore_case=True)
    ['abe', 'After', 'Bad', 'bored']


    """
    sorted_list = source_list.copy()

    if ignore_case:
        sorted_list.sort(key=lambda s: s.casefold(), reverse=reverse)
    else:
        sorted_list.sort(reverse=reverse)

    return sorted_list
