"""
jdcpy模块
本模块是吉富数据中心的python版接口
提供下载基金相关信息的功能
大致使用方法如下:
from jdcpy import jdcpy
jdcpy.login('username','password')
jdcpy.info(基金list,基本信息list,投资分布信息list,业绩表现list)
jdcpy.nav(基金list,起始日期,最终日期,信息类别list)
"""
import os, sys
import io
import json
import struct
from datetime import date, datetime
from urllib.parse import urljoin
import pandas as P
from sqlalchemy import create_engine
import pandas as P
import requests
from paramConverter import *

jdcpyVersion = '1.0'

loginUrl = 'http://120.27.238.50:8084'
# jdcbackend_url = 'http://jdcbackend.thiztech.com'
jdcbackend_url = 'http://192.168.68.193:8080'
# jdcbackend_url = 'http://47.101.67.217:8080'


def transformToNew(sourceName, assetType, dataType, columnSet):
    sourceName = oldSourceNameConverter[sourceName]
    if oldDataTypeConverter.get(dataType):
        dataType = oldDataTypeConverter[dataType]
        newColumns = []
        for i in columnSet:
            if oldColumnsConverter[sourceName][assetType][dataType].get(i):
                newColumns.append(oldColumnsConverter[sourceName][assetType][dataType][i])
            else:
                newColumns.append(i)
        return sourceName, assetType, dataType, newColumns
    return sourceName, assetType, dataType, columnSet


def transformToOld(sourceName, assetType, dataType, columnSet):
    sourceName = newSourceNameConverter[sourceName]
    if newDataTypeConverter.get(dataType):
        dataType = newDataTypeConverter[dataType]
        newColumns = []
        for i in columnSet:
            if newColumnsConverter[sourceName][assetType][dataType].get(i):
                newColumns.append(newColumnsConverter[sourceName][assetType][dataType][i])
            else:
                newColumns.append(i)
        return sourceName, assetType, dataType, newColumns
    return sourceName, assetType, dataType, columnSet


class jdcupload:
    def __init__(self):
        self.sess = requests.Session()
        self.token = ''
        self.lastErrorMsg = ""
        self.lastErrorCode = 0

    def login(self, username, password):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return: 返回True则登录成功,否则None表示没登录成功,lastErrorMsg里储存错误信息.
        """
        try:
            postMap = {'userAccount': username, 'password': password}
            # respData = self.sess.post(urljoin(loginUrl, '/QuantSystem/api/v1/user/login'), json=postMap)
            respData = self.sess.post(urljoin(loginUrl, '/QuantSystem/api/v1/manager/login'), json=postMap)
            respMap = respData.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode != 0:
                raise Exception(self.lastErrorMsg)
            self.token = respMap['token']
            self.sess.headers['Authorization'] = self.token
            return True
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def snapshot(self, sourceName, assetType, dataType, columnSet, idSet, startDate=None, endDate=None):
        sourceName, assetType, dataType, columnSet = transformToNew(sourceName, assetType, dataType, columnSet)
        # print(columnSet)
        try:
            postMap = {'sourceName': sourceName,
                       "assetType" : assetType,
                       "dataType"  : dataType,
                       "columnSet" : json.dumps(columnSet),
                       "idSet"     : json.dumps(idSet),
                       }
            if startDate:
                postMap['startDate'] = str(int(startDate.timestamp() * 1000))
            if endDate:
                postMap['endDate'] = str(int(endDate.timestamp() * 1000))
            resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/read'), json=postMap)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode == 0:
                data = respMap['data']
                ret = P.DataFrame(data, columns=columnSet)
                return ret
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def upload(self, sourceName, assetType, dataType, data):
        """
        :param sourceName:
        :param dataType:
        :param data:
        :return:
        """
        # try:
        #     data.iloc[:, 1] = P.to_datetime(data.iloc[:, 1]).apply(lambda x: x.strftime('%Y%m%d'))
        # except:
        #     pass
        # print(data)
        sourceName, assetType, dataType, columnSet = transformToNew(sourceName, assetType, dataType, list(data.columns))
        try:
            dataBulk = ''
            for i in data.index:
                dataBulk += data.loc[i].to_json(orient='values', force_ascii=False) + '\n'
            param = [
                ('clientAppName', (None, os.path.abspath(__file__))),
                ('clientAppVersion', (None, jdcpyVersion)),
                ('sourceName', (None, sourceName)),
                ('assetType', (None, assetType)),
                ('dataType', (None, dataType)),
                # ('sourceDataRowType', (None, 'csv')),
                ('sourceDataRowType', (None, 'json_array')),
                # ('sourceDataRowType', (None, 'json_object')),
                # ('columnSet', (None, json.dumps(columnSet))),
                ('columnSet', (None, json.dumps(list(data.columns)))),  # upload 不需要做列名转换
                # ('dataBulk', ('filename', data.to_csv(header=None, index=None), 'text/plain')),
                ('dataBulk', ('filename', dataBulk)),
                # ('dataBulk', ('filename', data.to_json(orient='values', lines=True ,force_ascii=False))),
                # ('dataBulk', ('filename', data.to_json(orient='records', force_ascii=False), 'text/plain')),
            ]
            # print(json.dumps(columnSet))
            # print(dataBulk)
            # print(data.to_json(orient='values', force_ascii=False))
            resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/upload'), files=param)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode == 0:
                return respMap['jobId']
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e


class jdcsdk:
    def __init__(self):
        self.sess = requests.Session()
        self.token = ''
        self.lastErrorMsg = ""
        self.lastErrorCode = 0

    def login(self, username, password):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return: 返回True则登录成功,否则None表示没登录成功,lastErrorMsg里储存错误信息.
        """
        try:
            postMap = {'userAccount': username, 'password': password}
            resp = self.sess.post(urljoin(loginUrl, '/QuantSystem/api/v1/manager/login'), json=postMap)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode != 0:
                raise Exception(self.lastErrorMsg)
            self.token = respMap['token']
            self.sess.headers['Authorization'] = self.token
            return True
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def readId(self, sourceName, idlist):
        sourceName, assetType, dataType, columnSet = transformToNew(sourceName, None, None, None)
        try:
            jpost = json.dumps({'sourceName': sourceName, "idSet": json.dumps(list(idlist))})
            resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/upload'), data=jpost)
            jdata = resp.json()
            self.lastErrorCode = jdata['errorCode']
            self.lastErrorMsg = jdata['errorMsg']
            if self.lastErrorCode == 0:
                ret = P.read_json(jdata['data'], orient='values')
                ret.columns = eval(jdata['sourceNameSet'])
                return ret
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def read(self, sourceName, assetType, dataType, columnSet, idSet, startDate=None, endDate=None):
        if sourceName == 'blp' and assetType == 'fund' and dataType == 'nav':
            pass
            columns1 = columns2 = columnSet[:2]
            for i in columnSet:
                if i in ['av_p', 'div_p', 'split']:
                    columns1.append(i)
                else:
                    columns2.append(i)
            sourceName, assetType, dataType, columns1 = transformToNew(sourceName, assetType, dataType, columnSet)
            # print(columnSet)
            try:
                postMap = {'sourceName': sourceName,
                           "assetType" : assetType,
                           "dataType"  : dataType,
                           "columnSet" : json.dumps(columns1),
                           "idSet"     : json.dumps(idSet),
                           }
                if startDate:
                    postMap['startDate'] = str(int(startDate.timestamp() * 1000))
                if endDate:
                    postMap['endDate'] = str(int(endDate.timestamp() * 1000))
                resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/read'), json=postMap)
                respMap = resp.json()
                self.lastErrorCode = respMap['errorCode']
                self.lastErrorMsg = respMap['errorMsg']
                if self.lastErrorCode == 0:
                    data = respMap['data']
                    data1 = P.DataFrame(data, columns=columnSet)
                else:
                    raise Exception(self.lastErrorMsg)
            except Exception as e:
                self.lastErrorCode = -1
                self.lastErrorMsg = str(e)
                raise e
            dataType = 'calculated_nav'
            sourceName, assetType, dataType, columns2 = transformToNew(sourceName, assetType, dataType, columnSet)
            # print(columnSet)
            try:
                postMap = {'sourceName': sourceName,
                           "assetType" : assetType,
                           "dataType"  : dataType,
                           "columnSet" : json.dumps(columns2),
                           "idSet"     : json.dumps(idSet),
                           }
                if startDate:
                    postMap['startDate'] = str(int(startDate.timestamp() * 1000))
                if endDate:
                    postMap['endDate'] = str(int(endDate.timestamp() * 1000))
                resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/read'), json=postMap)
                respMap = resp.json()
                self.lastErrorCode = respMap['errorCode']
                self.lastErrorMsg = respMap['errorMsg']
                if self.lastErrorCode == 0:
                    data = respMap['data']
                    data2 = P.DataFrame(data, columns=columnSet)
                else:
                    raise Exception(self.lastErrorMsg)
            except Exception as e:
                self.lastErrorCode = -1
                self.lastErrorMsg = str(e)
                raise e
            ret = data1.merge(data2, on=columns1[:2], left_on=True)
            sourceName, assetType, dataType, columnSet = transformToOld(sourceName, assetType, dataType, ret.columns)
            ret.columns = columnSet
            return ret
        sourceName, assetType, dataType, columnSet = transformToNew(sourceName, assetType, dataType, columnSet)
        # print(columnSet)
        try:
            postMap = {'sourceName': sourceName,
                       "assetType" : assetType,
                       "dataType"  : dataType,
                       "columnSet" : json.dumps(columnSet),
                       "idSet"     : json.dumps(idSet),
                       }
            if startDate:
                postMap['startDate'] = str(int(startDate.timestamp() * 1000))
            if endDate:
                postMap['endDate'] = str(int(endDate.timestamp() * 1000))
            resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/read'), json=postMap)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode == 0:
                data = respMap['data']
                ret = P.DataFrame(data, columns=columnSet)
                return ret
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def update(self, sourceName, assetType, dataType, data):  # data的index必须为id列
        sourceName, assetType, dataType, columnSet = transformToNew(sourceName, assetType, dataType, list(data.columns))
        # try:
        #     data.iloc[:, 1] = P.to_datetime(data.iloc[:, 1]).apply(lambda x: x.strftime('%Y%m%d'))
        # except:
        #     pass
        dataBulk = ''
        for i in data.index:
            dataBulk += data.loc[i].to_json(orient='values', force_ascii=False) + '\n'
        try:
            param = [
                ('sourceName', (None, sourceName)),
                ('assetType', (None, assetType)),
                ('dataType', (None, dataType)),
                # ('sourceDataRowType', (None, 'csv')),
                # ('sourceDataRowType', (None, 'json_object')),
                # ('sourceDataRowType', (None, 'json_array')),
                ('columnSet', (None, json.dumps(columnSet))),
                # ('columnSet', (None, json.dumps(list(data.columns)))),  # update不需要做列名转换
                # ('dataBulk', ('filename', data.to_csv(header=None, index=None), 'text/plain')),
                # ('dataBulk', ('filename', data.to_json(orient='records', force_ascii=False), 'text/plain')),
                # ('dataBulk', ('filename', data.to_json(orient='values', force_ascii=False))),
                ('dataBulk', ('filename', dataBulk)),
            ]
            # print(json.dumps(columnSet))
            # print(dataBulk)
            resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/update'), files=param)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode == 0:
                return respMap['taskId']
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def rollback(self, taskId):
        try:
            postMap = {'taskId': taskId}
            resp = self.sess.post(url=urljoin(jdcbackend_url, 'api/v1/read'), json=postMap)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode == 0:
                return True
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e


class jdcpy:
    def __init__(self):
        self.sess = requests.Session()
        self.token = ''
        self.lastErrorMsg = ""
        self.lastErrorCode = 0

    def login(self, username, password):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return: 返回True则登录成功,否则None表示没登录成功,lastErrorMsg里储存错误信息.
        """
        try:
            postMap = {'userAccount': username, 'password': password}
            resp = self.sess.post(urljoin(loginUrl, '/QuantSystem/api/v1/user/login'), json=postMap)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            if self.lastErrorCode != 0:
                raise Exception(self.lastErrorMsg)
            self.token = respMap['token']
            self.sess.headers['Authorization'] = self.token
            return True
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def info(self, idList, basicInfo, classification, performance):
        """
        基金的基本信息
        :param idList:基金的标识列表,格式如list(string,string...)
        :param basicInfo:基金的基本信息列表,格式如list(string,string...)
        :param classification:投资分布信息列表,格式如list(string,string...)
        :param performance:业绩表现列表,格式如list(string,string...)
        :return: pandas.DataFrame
        """
        try:
            idList = list(idList)
            basicInfo = list(basicInfo)
            classification = list(classification)
            performance = list(performance)
            idList.sort()
            basicInfo.sort()
            classification.sort()
            performance.sort()
            idList = tuple(idList)
            basicInfo = tuple(basicInfo)
            classification = tuple(classification)
            performance = tuple(performance)
            postMap = {'idList': idList, 'basicInfo': basicInfo, 'classification': classification, 'performance': performance, 'token': self.token}
            resp = self.sess.post(urljoin(jdcbackend_url, 'apiData/fundInfo'), json=postMap)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            stream = io.StringIO(respMap['data'])
            if self.lastErrorCode == 0:
                return P.read_csv(stream, index_col=0)  # date_parser
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e

    def nav(self, idList, startDate, endDate, navList):
        """
        返回基金的历史表现
        :param idList:基金的标识列表,格式如list(string,string...)
        :param startDate:起始日期,可以为timestamp格式,或者date,或者datetime,也可以为string如1999-08-10或1990/08/10格式
        :param endDate:结束日期
        :param navList:所要查询的信息列表,格式如list(string,string...)
        :return: pandas.DataFrame
        """
        try:
            idList = list(idList)
            navList = list(navList)
            idList.sort()
            navList.sort()
            idList = tuple(idList)
            navList = tuple(navList)
            if type(startDate) == datetime:
                startDate = int(1000 * startDate.timestamp())
                endDate = int(1000 * endDate.timestamp())
            postMap = {'idList': idList, 'startDate': startDate, 'endDate': endDate, 'navList': navList, 'token': self.token}
            resp = self.sess.post(urljoin(jdcbackend_url, 'apiData/fundNav'), json=postMap)
            respMap = resp.json()
            self.lastErrorCode = respMap['errorCode']
            self.lastErrorMsg = respMap['errorMsg']
            stream = io.StringIO(respMap['data'])
            if self.lastErrorCode == 0:
                return P.read_csv(stream, index_col=0)  # date_parser
            else:
                raise Exception(self.lastErrorMsg)
        except Exception as e:
            self.lastErrorCode = -1
            self.lastErrorMsg = str(e)
            raise e
