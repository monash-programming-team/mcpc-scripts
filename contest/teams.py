#!/usr/bin/env python3
import sys
import random
import string

random.seed()

def format_teamid(tid):
    if tid == "None":
        return tid
    else:
        while len(tid) < 3:
            tid = '0' + tid
        return tid

def gen_passwd(l=6):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(l))

class Room:
    capacity = 0
    num = "None"
    assigned = 0

    def __init__(self, c, num):
        self.capacity = c
        self.num = num
        self.assigned = 0
        self.free_desks = [True] * self.capacity
        self.contestants = []

    def find_desk(self, r=1):
        for i in range(self.capacity):
            if i % 2 == r and self.free_desks[i]:
                return i
        return -1

    def available(self):
        res = []
        for i in range(self.capacity):
            if i % 2 == 0 and self.free_desks[i]:
                res.append("%s-%d" % (self.num, i))
        for i in range(self.capacity):
            if i % 2 == 1 and self.free_desks[i]:
                res.append("%s-%d" % (self.num, i))
        return res

    def save_info(self):
        lines = ["|%20s|%10s|" % ("Name", "Desk")]
        breaker = "|%s|%s|" % ('-'*20, '-'*10)
        lines.append(breaker)
        lines.extend(["|%20s|%10s|" % (i.fname + ' ' + i.lname, i.location) for i in self.contestants])
        with open("room-info/%s.table" % self.num, "w") as f:
            f.write('\n'.join(lines))


class participant:
    tid = "None" 
    gid = "None"
    passwd = "None"
    location = "None"

    def __init__(self, line):
        self.email, self.fname, self.lname, self.sid, self.tname, self.veteran = line.strip().split(',')
        self.gid = 6 if self.veteran == "Yes" else 7
        self.passwd = gen_passwd()

    def to_team(self):
        return "%s\t%s\t%s\t%s\tMonash University\tMonash\tAUS" % (self.tid, self.sid, self.gid, self.tname)

    def to_account(self):
        return "team\t%s %s\tteam-%s\t%s" % (self.fname, self.lname, format_teamid(self.tid), self.passwd)

    def get_group(self):
        return "Veteran" if self.gid == 6 else "Newbie"

    def to_all(self):
        return ",".join([self.email, self.fname + " " + self.lname, self.sid, self.tname, self.get_group(), self.location])

    def assign_room(self, room, r):
        desknum = room.find_desk(r)
        self.location = "%s-%d" % (room.num, desknum)
        room.free_desks[desknum] = False
        room.assigned += 1
        room.contestants.append(self)
        print ("assign %s to %s" % (self.fname + " " + self.lname, self.location))
        assert(room.assigned <= room.capacity)

    def to_print(self):
        return "# %s\n## location: %s\n%s\n## login name: %s\n## password: `%s`" % (
            self.fname + ' ' + self.lname,
            self.location,
            "***",
            "team-" + format_teamid(self.tid),
            self.passwd
        )

def load(fpath):
    with open(fpath, "r") as f:
        lines = f.readlines()
    ps = [participant(i) for i in reversed(lines[1:])]
    cnt = 150
    for i in ps:
        i.tid = str(cnt)
        cnt += 1
    return ps


def init_password(ps):
    for i in ps:
        i.gen_passwd()


def assign_room(ps):
    r142 = Room(16, "142")
    r143 = Room(20, "143")
    r146 = Room(20, "146")
    r147 = Room(20, "147")
    G11A = Room(24, "G11A")
    G11B = Room(24, "G11B")

    # pre allocate
    for i in ps:
        # Harsil Patel
        if i.sid == '28334825':
            i.assign_room(r147, 1)

    for i in ps:
        if i.location != "None":
            continue
        # is veteran
        if i.gid != 6:
            continue

        if r147.find_desk(0) != -1:
            i.assign_room(r147, 0)

        elif r146.find_desk(0) != -1:
            i.assign_room(r146, 0)

        elif r143.find_desk(0) != -1:
            i.assign_room(r143, 0)

        elif r142.find_desk(0) != -1:
            i.assign_room(r142, 0)

        elif r147.find_desk(1) != -1:
            i.assign_room(r147, 1)

        elif r146.find_desk(1) != -1:
            i.assign_room(r146, 1)

        elif r143.find_desk(1) != -1:
            i.assign_room(r143, 1)

        elif r142.find_desk(1) != -1:
            i.assign_room(r142, 1)

        elif G11A.find_desk(0) != -1:
            i.assign_room(G11A, 0)
    
        elif G11A.find_desk(1) != -1:
            i.assign_room(G11A, 1)

        elif G11B.find_desk(0) != -1:
            i.assign_room(G11B, 0)
    
        elif G11B.find_desk(1) != -1:
            i.assign_room(G11B, 1)
        else:
            assert(False)

    for i in ps:
        if i.location != "None":
            continue
        # is newbie
        if i.gid != 7:
            continue

        if G11B.find_desk(0) != -1:
            i.assign_room(G11B, 0)

        elif G11A.find_desk(0) != -1:
            i.assign_room(G11A, 0)

        elif r142.find_desk(0) != -1:
            i.assign_room(r142, 0)

        elif r143.find_desk(0) != -1:
            i.assign_room(r143, 0)

        elif r146.find_desk(0) != -1:
            i.assign_room(r146, 0)

        elif r147.find_desk(0) != -1:
            i.assign_room(r147, 0)

        elif G11B.find_desk(1) != -1:
            i.assign_room(G11B, 1)

        elif G11A.find_desk(1) != -1:
            i.assign_room(G11A, 1)

        elif r142.find_desk(1) != -1:
            i.assign_room(r142, 1)
    
        elif r143.find_desk(1) != -1:
            i.assign_room(r143, 1)

        elif r146.find_desk(1) != -1:
            i.assign_room(r146, 1)
    
        elif r147.find_desk(1) != -1:
            i.assign_room(r147, 1)
        else:
            assert(False)

    desks = set()
    for i in ps:
        assert(i.location != "None")
        assert(i.location not in desks)
        desks.add(i.location)

    r142.save_info()
    r143.save_info()
    r146.save_info()
    r147.save_info()
    G11A.save_info()
    G11B.save_info()

    free = []
    free.extend(G11A.available())
    free.extend(G11B.available())
    free.extend(r142.available())
    free.extend(r143.available())
    free.extend(r146.available())
    free.extend(r147.available())
    with open("available.txt", "w") as f:
        f.write('\n'.join(free))

def export_team_tsv(ps):
    lines = ["teams\t1"]
    for i in ps:
        lines.append(i.to_team())
    with open("teams.tsv", "w") as f:
        f.write("\n".join(lines))


def export_account_tsv(ps):
    lines = ["accounts\t1"]
    for i in ps:
        lines.append(i.to_account())
    with open("accounts.tsv", "w") as f:
        f.write("\n".join(lines))

def export_all_csv(ps):
    lines = ["email, name, student id, team name, group, location"]
    for i in ps:
        lines.append(i.to_all())

    with open("team-assigned-info.csv", "w") as f:
        f.write("\n".join(lines))

def export_printed(ps):
    lines = [i.to_print() for i in ps]
    breaker = "\n<div style=\"page-break-after: always;\"></div>\n\n"

    with open("teams-print.md", "w") as f:
        f.write(breaker.join(lines))

if __name__ == "__main__":
    ps = load(sys.argv[1])
    assign_room(ps)
    export_team_tsv(ps)
    export_account_tsv(ps)
    export_all_csv(ps)
    export_printed(ps)
