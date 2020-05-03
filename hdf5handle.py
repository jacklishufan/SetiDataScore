import h5py

def writedatascore(filename,score):
    f = h5py.File(filename)
    f['data'].attrs['quality']=score
    f.close()

def readdatascore(filename):
    f = h5py.File(filename)
    result = f['data'].attrs.get('quality')
    f.close()
