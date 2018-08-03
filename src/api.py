import json
import socket
class VndbConnection():

    def __init__():
        endpoint = ("api.vndb.org", 19534)
        self.s = socket.socket()
        self.s.connect(endpoint)
        q = {"protocol":1,"client":"vn recommender","clientver":0.1}
        qe = json.dumps(q)
        cmd = bytes("{} {}\x04".format('login', qe), "utf-8")
        self.s.sendall(cmd)
        self.rtn = self.s.recv(1024)

    def is_valid():
        """
        only to be run after init
        """
        return self.rtn == b'ok\x04'

    def get_user_votes(uid):
        """
        input: user id
        output: [(userid, vnid, vote),...]
        """
        #the 'more' flag in the json refers to whether there are more results or not. I set my results at 50 to minimize this (since there is a limit on api requests).
        page_number = 1
        votelist_json = self.get_votelist_json(page_number)
        first = [tuple([elements[1] for elements in sorted(row.items(),key=lambda row: row[0])][1:]) for row in votelist_json['items']]
        while votelist_json['more']:
            page_number += 1
            votelist_json = self.get_votelist_json(page_number)
            first += [tuple([elements[1] for elements in sorted(row.items(),key=lambda row: row[0])][1:]) for row in votelist_json['items']]
        return first 

    def get_votelist_json(page=1):
        """
        you should only call get_user_votes
        input: int page
        output: json object of votes
        """
        json_flag = json.dumps({"results":50, "page":page})
        self.s.sendall(bytes('get votelist basic (uid={}) {} \x04'.format(uid, json_flag),"utf-8")) 
        rtn = s.recv(1024)
        string = rtn.decode('utf-8')[8:-1]
        return json.loads(string)

