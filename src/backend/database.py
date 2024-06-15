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
                case 972: new_c = chr(8057) # ό
                case 39:  new_c = "" # '
            
            word_converted += new_c
        
        return word_converted

    def parse_inflected(self, inflected:str)->dict:
        response_dict = {'value': None,
                         'error': SQLliteStatus.SQLLITE_STATUS_OK}

        try:
            db = SQL_Database(DB_PATH_NT)
            inflected_converted = self.convert_to_db_chars(inflected)

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

                response_dict['value'] = inflected_entry[0]
            else:
                response_dict['value'] = InflectedWord(inflection=inflected, lemma="NOT FOUND")

        except Exception as e:
            print(e)
            response_dict['error'] = SQLliteStatus.SQLLITE_ERROR_UNKNOWN
        
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
            db = SQL_Database(DB_PATH_NT)
            db.insert_table(greek_inflected_table_insert_info,inflected_word.getInsertParams())
            db.close()

        except Exception as e:
            return {'error': SQLliteStatus.SQLLITE_ERROR_UNKNOWN}
        
        return {'error': SQLliteStatus.SQLLITE_STATUS_OK}
    