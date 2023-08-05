import waverunner
import argparse
import xarray as xr
import numpy as np

from scipy.interpolate import interp1d

from .Pyspectre import batch_hashes


def run_batch(circuit, stimuli, time_vec, signal_names):
    return_type = 'float32'

    print('running_batch of {} simulations.'.format(len(stimuli)))

    times, signals = circuit.run_batch(stimuli, time_vec, signal_names)

    ids = batch_hashes(stimuli, time_vec)

    for i, (t, s) in enumerate(zip(times, signals)):
        signals[i] = interp1d(t, s)(time_vec)

    das = []
    for i, _ in enumerate(signal_names):
        das.append(xr.DataArray(data=np.stack([s[i] for s in signals]).astype(return_type),
                                coords=[ids, time_vec.astype(return_type)],
                                dims=['id', 'time'],
                                name=signal_names[i]
                                ))

    df = xr.Dataset({d.name: d for d in das}).astype(return_type)

    # result = []
    # for i, sigs in enumerate(signals):
    #     result.extend(
    #         [pd.Series(
    #             s,
    #             index=time_vec,
    #             name='{}_{}'.format(signames[ii], i),
    #             dtype=np.float16,
    #         ) for ii, s in enumerate(sigs)])
    # df = pd.DataFrame({s.name: s for s in result})
    # df = df.to_sparse()
    # df = pd.concat(result, axis=1)
    # df.columns = [s.name for s in result]
    return df


def start_server(port=None, remote_ips=None, polling_interval=0):

    server = waverunner.Waverunner(port=port, remote_ips=remote_ips, polling_interval=polling_interval)
    server.register_secure_method(run_batch)

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
