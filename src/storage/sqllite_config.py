from enum import Enum

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

DB_PATH_NT = "C:/Users/appli/repos/greek-helper/src/storage/greek_nt.db3"

class SQLliteStatus(Enum):
    # /* 
    #  * Behavior handling errors
    #  */
    # // 0x1? Informational Responses
    # // 0x2? Successful Responses
    SQLLITE_STATUS_OK = 0x20                #//!< No error occurred when handling request
    # // 0x3? Redirection Messages
    # // 0x4? Database Error Responses
    SQLLITE_ERROR_NOT_FOUND = 0x40         #//!< Error: query returned none
    SQLLITE_ERROR_UNKNOWN = 0x41           #//!< Error: query threw an exception
    # // 0x5? Peripheral Error Responses


## NT Greek Database Tables
greek_inflected_table_create_info = "inflected(id INTEGER PRIMARY KEY, inflection TEXT, lemma TEXT, uncontracted_form TEXT, parsing TEXT, translation TEXT, verse TEXT)"
greek_inflected_table_insert_info = "inflected(id, inflection, lemma, uncontracted_form, parsing, translation, verse)"