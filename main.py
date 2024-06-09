from myhttp import HTTPServer
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CGI Multi-thread HTTP Server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host IP')
    parser.add_argument('--port', type=int, default=8888, help='Port number')
    parser.add_argument('--max_conn', type=int, default=10, help='Max connections')
    parser.add_argument('--work_dir', type=str, default='./', help='Document root')
    parser.add_argument('--version', type=str, default='HTTP/1.1', help='HTTP version')
    args = parser.parse_args()

    HTTPServer(
        args.host,
        args.port,
        args.max_conn,
        args.work_dir,
        args.version
    ).run()