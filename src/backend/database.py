from interfaces.SQLLite import SQL_Database
from models.database_models import *
from storage.sqllite_config import *


class DatabaseInterface():
    def __init__(self) -> None:
        pass


    def convert_to_db_chars(self, word:str)->str:
        word_converted = ""
        for c in word:
            new_c = c
            match ord(c):
                case 940: new_c = chr(8049) # ά
                case 941: new_c = chr(8051) # έ
                case 942: new_c = chr(8053) # ή
                case 943: new_c = chr(8055) # ί
                case 972: new_c = chr(8057) # ό
                case 973: new_c = chr(8059) # ύ
                case 974: new_c = chr(8061) # ώ
                case 39:  new_c = "" # '
                case 183: new_c = "" # ·
                case 59:  new_c = "" # ;
            
            word_converted += new_c
        
        return word_converted

    def parse_inflected(self, book_name:str, chapter_num:int, inflected:str)->dict:
        response_dict = {'value': None,
                         'error': SQLliteStatus.SQLLITE_STATUS_OK}

        try:
            db = SQL_Database(DB_PATH_NT)
            inflected_converted = self.convert_to_db_chars(inflected)
            not_in_cache = False
            # Check the chapter cache first
            try:
                db_response = db.run_query_params(f"SELECT * FROM [c{book_name}{chapter_num}] WHERE inflection REGEXP ?",[f"{inflected_converted},?".encode("utf-8")])
                # print(f"Cache Response {len(db_response)}")
                if(len(db_response)>0):
                        # Make a list of all the matches (substrings match so this could be a lot)
                        inflected_list = []
                        for r in db_response:
                            word = InflectedWord()
                            word.parseQuery(r)
                            inflected_list.append(word)
                        # find the shortest inflection match and extract the lemma
                        min_inflected = min([x.inflection for x in inflected_list],key=len)
                        inflected_entry = [x for x in inflected_list if x.inflection == min_inflected]

                        response_dict['value'] = inflected_entry[0]
                else:
                    not_in_cache = True
            
            except Exception as e:
                if("no such table" in str(e)):
                    print(f"Table {book_name}{chapter_num} doesn't exist" )
                    tname = f'c{book_name}{chapter_num}{greek_chapter_table_create_info}'
                    print(tname)
                    print(greek_inflected_table_create_info)
                    db.create_table(tname)
                    not_in_cache = True

                else:
                    print(f"Cache Exception: {e}")
                

            # Last resort, check the ALL ENTRIES table to find the word
            if(not_in_cache):
                # print(f"Not in Cache: {inflected_converted}")
                db_response = db.run_query_params("SELECT * FROM [inflected] WHERE inflection REGEXP ?",[f"{inflected_converted},?".encode("utf-8")])
                if(len(db_response)>0):
                    # Make a list of all the matches (substrings match so this could be a lot)
                    inflected_list = []
                    for r in db_response:
                        word = InflectedWord()
                        word.parseQuery(r)
                        inflected_list.append(word)
                    # find the shortest inflection match and extract the lemma
                    min_inflected = min([x.inflection for x in inflected_list],key=len)
                    inflected_entry = [x for x in inflected_list if x.inflection == min_inflected]
                    # Return this entry for now
                    response_dict['value'] = inflected_entry[0]

                    entry_id = inflected_entry[0].id
                    
                    # Store a copy of this entry in the cache for future reference
                    entry_list = []
                    for r in db_response:
                        word = InflectedWord()
                        word.copyQuery(r) # this time don't alter the entry
                        entry_list.append(word)
                    # find the shortest inflection match and extract the lemma
                    entries = [x for x in entry_list if x.id == entry_id]

                    db.insert_table(f'c{book_name}{chapter_num}{greek_chapter_table_insert_info}', entries[0].getInsertParams())

                elif inflected[0] in ["Ἰ"]: # Likely a proper noun
                    response_dict['value'] = InflectedWord(inflection=inflected, lemma=inflected)
                else:
                    response_dict['value'] = InflectedWord(inflection=inflected, lemma="NOT FOUND")

        except Exception as e2:
            print(f"Meta Exception: {e2}")
            response_dict['error'] = SQLliteStatus.SQLLITE_ERROR_UNKNOWN
            db.close()

        return response_dict

    def already_has_lemma(self, lemma:str):
        response_dict = {'value': None,
                         'error': SQLliteStatus.SQLLITE_STATUS_OK}

        try:
            db = SQL_Database(DB_PATH_NT)
            db_response = db.run_query(f"SELECT * FROM [inflected] WHERE lemma LIKE '{lemma}' LIMIT 1")
            if(len(db_response)>0):
                response_dict['value'] = True
            else:
                response_dict['value'] = False

        except Exception as e:
            print(e)
            response_dict['error'] = SQLliteStatus.SQLLITE_ERROR_UNKNOWN
        
        return response_dict
        


    def insert_inflected(self, inflected_word:InflectedWord):
        try:
            print(f"Insert {inflected_word.inflection} ")
            # Convert to the greek character scheme of the database
            inflected_converted = self.convert_to_db_chars(inflected_word.inflection)
            inflected_word.inflection = inflected_converted
            db = SQL_Database(DB_PATH_NT)
            db.insert_table(greek_inflected_table_insert_info,inflected_word.getInsertParams())
            db.close()

        except Exception as e:
            return {'error': SQLliteStatus.SQLLITE_ERROR_UNKNOWN}
        
        return {'error': SQLliteStatus.SQLLITE_STATUS_OK}
    