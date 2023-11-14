import json
import pprint
import random
import traceback
from abc import *
from datetime import datetime as dt

from opensearchpy import OpenSearch, helpers
from opensearchpy.exceptions import NotFoundError, TransportError, RequestError
from requests import Session


class OpSch(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, kwargs):
        raise NotImplemented

class OpSchDummyTrue(OpSch):

    def __init__(self, kwargs):
        #print(kwargs)
        self.conn = True

class OpSch2(OpSch):
    def __init__(self, kwargs):
        # es 접속
        try:
            self.hosts = kwargs.get('hosts','localhost')
            self.verify_certs = kwargs.get('verify_certs',False)
            self.ssl_show_warn = kwargs.get('ssl_show_warn',False)
            self.timeout = kwargs.get('timeout',1000000)
            self.requestimeout = kwargs.get('requestimeout',1000000)
            self.opsch_id = kwargs.get('id','')
            self.opsch_pwd = kwargs.get('pwd','')

            self.conn = OpenSearch(hosts=self.hosts,
                                   http_auth=(self.opsch_id, self.opsch_pwd),                     
                                   verify_certs=self.verify_certs, 
                                   timeout=self.timeout,
                                   requestimeout=self.requestimeout, 
                                   ssl_show_warn=self.ssl_show_warn)

            if not self.conn.ping():
               raise TransportError('OpenSearch ping false')
        except TransportError as e:
            raise TransportError(str(e))
        
    def close(self):
        self.conn.close()

       
       
    def search(self,body,index):
            try:
                search_results = self.conn.search(
                    body=body,
                    index=index            
                )
            except Exception as err:
                err_obj = pprint.pformat(err.errors)            
                raise Exception(str(err_obj))
            else:
                return search_results
            
    def search_template(self,body,index):
        try:
            search_results = self.conn.search_template(
                body=body,
                index=index
            )
        except Exception as err:
            err_obj = pprint.pformat(err.errors)            
            raise Exception(str(err_obj))
        else:
            return search_results
        
    def msearch_template(self,body,index):
        try:
            search_results = self.conn.msearch_template(
                body=body,
                index=index
            )
        except Exception as err:
            err_obj = pprint.pformat(err.errors)            
            raise Exception(str(err_obj))
        else:
            return search_results
        
        
    def exist(self,index,id):
        return self.conn.exists(index=index,id=id) 
        
    