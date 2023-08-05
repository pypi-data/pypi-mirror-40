import waverunner
import pyspectre
import argparse


def start_server(port=None, remote_ips=None, polling_interval=0):

    server = waverunner.Waverunner(port=port, remote_ips=remote_ips, polling_interval=polling_interval)
    server.register_secure_method(pyspectre.run_batch)

    try:
        server.serve_forever()

    except:
        server.stop_service()

    finally:
        server.exit_gracefully()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', action='store')
    parser.add_argument('--remote_ips', '-r', action='store')
    parser.add_argument('--polling-interval', '-i', action='store')

    args, unknown_args = parser.parse_known_args()
    start_server(port=args.port, remote_ips=args.remote_ips, polling_interval=args.polling_interval)


if __name__ == '__main__':
    main()
