import json
import socket


class VndbConnection():

    def __init__(self):
        self.endpoint = ("api.vndb.org", 19534)
        q = {"protocol": 1, "client": "vn recommender", "clientver": 0.1}
        qe = json.dumps(q)
        self.cmd = bytes("{} {}\x04".format('login', qe), "utf-8")
        self.connect()

    def connect(self):
        self.s = socket.socket()
        self.s.connect(self.endpoint)
        self.s.sendall(self.cmd)
        self.rtn = self.s.recv(1024)

    def is_valid(self):
        """
        only to be run after connect
        if it's not valid it is made valid
        """
        if self.rtn != b'ok\x04':
            self.connect()
        return self.rtn == b'ok\x04'

    def get_user_votes(self, uid):
        """
        input: user id
        output: [(userid, vnid, vote),...]
        """
        # the 'more' flag in the json refers to whether there are more results or not. I set my results at 50 to minimize this (since there is a limit on api requests).
        if self.is_valid():
            page_number = 1
            votelist_json = self.get_votelist_json(uid, page_number)
            first = [tuple([elements[1] for elements in sorted(
                row.items(), key=lambda row: row[0])][1:]) for row in votelist_json['items']]
            while votelist_json['more']:
                page_number += 1
                votelist_json = self.get_votelist_json(uid, page_number)
                first += [tuple([elements[1] for elements in sorted(row.items(),
                                                                    key=lambda row: row[0])][1:]) for row in votelist_json['items']]
            return first
        return None

    def get_votelist_json(self, uid, page=1):
        """
        you should only call get_user_votes
        input: int page
        output: json object of votes
        """
        json_flag = json.dumps({"results": 20, "page": page})
        self.s.sendall(
            bytes('get votelist basic (uid={}) {} \x04'.format(uid, json_flag), "utf-8"))
        rtn = self.s.recv(2048)
        string = rtn.decode('utf-8')[8:-1]
        json_obj = json.loads(string)
        #try json.load(rtn)
        if not json_obj['more']:
            self.s.close()
            self.rtn = 'not connected'
        return json_obj

    def convert_to_name(self, list_ids):
        if self.is_valid():
            self.s.sendall(bytes('get vn basic (id={})\x04'.format(list_ids),"utf-8"))
            rtn = self.s.recv(2048)
            string = rtn.decode('utf-8')[8:-1]
            json_obj = json.loads(string)
            #should have abstracted this code already
            dic = {x['id']: x['title'] for x in jsons['items']}
            self.s.close()
            self.rtn = 'not connected'
            return [dic[x] for x in list_ids]


# in the future, i need to plan more around tests. adding tests for things like whether the page continuing works
