import atexit
import concurrent
import concurrent.futures as futures
import duolingo
import grpc
import json
import logging
import os
import typing
from typing import Dict
from typing import List

import server_pb2
import server_pb2_grpc


name: str = 'Get HTTP Service'

duolingo_username: str = None
duolingo_password: str = None
port: str = None

sessfile: str = os.path.abspath('./.duo.sess')
lingo = None


def init_env() -> None:
    global port
    port = os.environ['PORT']
    logging.info('Found PORT at %s', port)

    global duolingo_username
    duolingo_username = os.environ['USER']
    logging.info('Found USER at %s', duolingo_username)

    global duolingo_password
    duolingo_password = os.environ['PASS']
    logging.info('Found PASS at %s', duolingo_password)


def init_loggin(j) -> None:
    global lingo
    username = duolingo_uesrname
    password = duolingo_password
    lingo = duolingo.Duolingo(username=username, password=password)


def init_atexit() -> None:
    def end():
        logging.info('bye')

    atexit.register(end)


def init_logging() -> None:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('hi')


def init_server() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    server_pb2_grpc.add_ReadyServicer_to_server(Server(), server)
    server.add_insecure_port(f'localhost:{port}')

    server.start()
    logging.info('Started server at %s', port)
    server.wait_for_termination()

    logging.info('Ending server')


class Server(server_pb2_grpc.ReadyServicer):
    @staticmethod
    def get_http_request(name: str) -> List[str]:
        friends_resp = lingo.get_friends()
        friends: List[str] = []

        for fob in friends_resp:
            fob: str = fob['username']
            friends.append(fob)

        return friends

    def Submit(self, request, context):
        name: str = request.name
        logging.info('Registering service %s', service)

        return server_pb2.ReadyStatus(ready=False)


def init() -> None:
    init_logging()
    init_atexit()
    init_env()
    init_logging()
    init_server()


def main() -> None:
    init()


if __name__ == '__main__':
    main()
