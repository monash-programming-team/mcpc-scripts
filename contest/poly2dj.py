#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET
from shutil import copyfile

def main(pathfrom, pathto):
    prob_name = pathfrom.split("/")[-1]
    data_path = pathfrom.strip('/') + "/tests"
    example_path = pathfrom.strip('/') + '/statement-sections/english'
    sol_path = pathfrom.strip('/') + "/solutions"

    to_secret_path = pathto.strip('/') + "/%s" % prob_name + "/data/secret"
    to_sample_path = pathto.strip('/') + "/%s" % prob_name + "/data/sample"
    to_solution_path = pathto.strip('/') + "/%s" % prob_name + "/submissions/accepted"

    os.makedirs(to_secret_path, exist_ok=True)
    os.makedirs(to_sample_path, exist_ok=True)
    os.makedirs(to_solution_path, exist_ok=True)

    for i in os.listdir(data_path):
        fname = os.path.basename(i)
        if fname.endswith(".a"):
            fname = fname.replace(".a", ".ans")
        else:
            fname = fname + ".in"
        dest = to_secret_path + "/%s" % fname
        start = data_path + '/' + i
        print ("write %s to %s" % (start, dest))

        with open(start, "r") as f:
            lines = f.readlines()
        with open(dest, "w") as f:
            lines = [i.strip() + '\n' for i in lines]
            f.writelines(lines)

    for i in os.listdir(sol_path):
        fname = os.path.basename(i)
        if fname.endswith('.desc'):
            continue
        if fname.endswith(".py"):
            fname = fname.replace(".py", ".py3")
        dest = to_solution_path + "/%s" % fname
        start = sol_path + '/' + i
        print ("cp %s %s" % (start, dest))
        copyfile(start, dest)

    for i in os.listdir(example_path):
        if not i.startswith('example'):
            continue
        l = i.split('.')
        if len(l) == 3:
            fname = l[1] + ".ans"
        else:
            fname = l[1] + ".in"
        start = example_path + '/' + i
        dest = to_sample_path + '/' + fname

        print ("write %s to %s" % (start, dest))
        with open(start, "r") as f:
            lines = f.readlines()
        with open(dest, "w") as f:
            lines = [i.strip() + '\n' for i in lines]
            f.writelines(lines)



    tree = ET.parse("%s/problem.xml" % pathfrom.strip('/') )
    pname = tree.find("./names/name").get("value")
    with open("%s/%s/problem.yaml" % (pathto.strip('/'), prob_name), "w") as f:
        f.write("name: '%s'\n" % pname)


if __name__ == "__main__":
    polydir = sys.argv[1]
    djdir = sys.argv[2]
    for i in os.listdir(polydir):
        prob_dir = polydir.strip('/') + '/' + i
        if os.path.isdir(prob_dir):
            main(prob_dir, djdir)
