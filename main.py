import logging
import json
import socketClient as sc
import socketServer as sv
import multiprocessing as mp

# config
data = json.load(open('config.json'))

def main():
    parent_conn, child_conn = mp.Pipe()
    p1 = mp.Process(target=sv.run, args=(parent_conn,))
    p2 = mp.Process(target=sc.run, args=(child_conn,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()


if __name__ == '__main__':
    main()

