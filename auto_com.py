from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pprint import pprint
# import psycopg2
import os
from opsch import OpSch2
import re
import unicodedata


class AutoComplete:
    def __init__(self, opsch_conn_info):        
        self.opsch_conn_info = opsch_conn_info
        self.opsch_conn = None        
        self.index_name = "test_acom1"
    
    
    
    
    def __make_corr_body(self,keyword):
        body={
            "id" : "suggest",
            "params": {
                "keyword" : f"{keyword}"
            }
        }
        return body
    
    def __parse_corr_keyword(self,result:list):                
        corr_keywords = []
        results = result['suggest']['my-suggestion']
        for res in results:
            if len(res['options'])>0 and res['options'][0]['score'] > 0.70:
                corr_word = unicodedata.normalize('NFC',res['options'][0]['text'])
                corr_keywords.append(corr_word)
            else:
                corr_keywords.append(unicodedata.normalize('NFC',res['text']))
        corr_keyword = ' '.join(corr_keywords)
        return corr_keyword

    def __acom_body(self,keyword):
        body_list=[]
        body_list.append({"index":"luxury_panda_auto_complete"})
        body_list.append({"id":"luxury_panda_auto_complete","params":{"view" : 1,"keyword":f"{keyword}","is_brand" : 1}})
        body_list.append({"index":"luxury_panda_auto_complete"})
        body_list.append({"id":"luxury_panda_auto_complete","params":{"view" : 10,"keyword":f"{keyword}","is_brand" : 0}})
        return body_list
    
    def __get_corr_keyword(self,results):
        # try:
        if len(results['suggest']['my-suggestion']) > 0:
            corr_res = results['suggest']['my-suggestion'][0]['options'][0]['text']
            return corr_res
        else:
            corr_res = results['suggest']['my-suggestion'][0]['text']
            return corr_res
        # except:
        #     corr_res = ""
        #     return corr_res
            
    
    def __search_term(self,body,index):
        results = self.opsch_conn.search_template(
                    index=index,
                    body=body
                )
        return results

    def __msesarch_tem(self,body,index):
        results = self.opsch_conn.msearch_template(
            body=body,
            index=index
        )
        return results
    
    def run(self,q):
        self.opsch_conn = OpSch2(self.opsch_conn_info)
        body = self.__make_corr_body(keyword=q)
        result = self.__search_term(body=body,index="test_acom1")
        corr_keyword = self.__parse_corr_keyword(result=result)        
        acom_body = self.__acom_body(keyword=corr_keyword)
        results = self.__msesarch_tem(body=acom_body,index="luxury_panda_auto_complete")
        return results
        

