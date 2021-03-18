import atexit
import grpc
import logging
import os

import server_pb2
import server_pb2_grpc


port: str = None


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


def init_client() -> None:
    addr: str = f'localhost:{port}'
    logging.info('Calling %s', addr)

    channel = grpc.insecure_channel(addr)
    stub = server_pb2_grpc.ReadyStub(channel)

    user: str = 'its_me_sguzman'
    logging.info('Submitting name "%s"', user)
    resp = stub.Submit(server_pb2.User(name=user))

    logging.info('Retrieved:')
    friends: List[str] = resp.names
    logging.info(friends)


def init() -> None:
    init_logging()
    init_atexit()
    init_env()
    init_client()


def main() -> None:
    init()


if __name__ == '__main__':
    main()
