from myhttp import HTTPServer
import config

if __name__ == '__main__':
    HTTPServer( 
        config.HOST, 
        config.PORT, 
        config.MAX_CONN, 
        config.TIMEOUT, 
        config.DOCUMENT_ROOT, 
        config.VERSION
    ).run()
