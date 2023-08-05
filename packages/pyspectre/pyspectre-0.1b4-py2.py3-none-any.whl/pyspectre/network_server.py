import waverunner
import pyspectre
import cPickle as pickle
import tarfile
import tempfile
import cStringIO as StringIO
import signal


def load_circuit(circuit_ser, dirzip_bin):
    global circuit, spectre

    circuit = pyspectre.Circuit(pickle.loads(circuit_ser))

    rundir = tempfile.mkdtemp()
    tf = StringIO.StringIO()
    open(tf, mode='wb').write(dirzip_bin)
    tarfile.TarFile(fileobj=tf).extractall(path=rundir)
    del tf

    if spectre.spectre:
        spectre.close()

    spectre = pyspectre.Pyspectre(circuit, 'simdir')


def run_stimuli(stimuli_list):
    if spectre not in locals():
        return 'no circuit loaded'

    stimuli_list = pickle.loads(stimuli_list)
    t, w = spectre.run_stimuli(stimuli_list)

    return pickle.dumps((t, w))


if __name__ == '__main__':

    server = waverunner.Server()
    server.register_function(load_circuit)
    server.register_function(run_stimuli)

    try:
        server.serve_forever()
    except:
        server.shutdown.set()
    finally:
        server.exit_gracefully()
