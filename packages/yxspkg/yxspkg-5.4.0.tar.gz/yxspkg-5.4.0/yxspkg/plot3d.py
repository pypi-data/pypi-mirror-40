import numpy as np
from pathlib import Path
import re

def read_plot3d_fmt(filename,sep=None):
    fp = open(filename)
    n_block = fp.readline().strip()
    if n_block.isdigit():
        n_block = int(n_block)
        if sep is None:
            blocks = [fp.readline().strip().split() for _ in range(n_block)]
        else:
            blocks = [fp.readline().replace(sep,' ').strip().split() for _ in range(n_block)]
    else:
        if sep is None:
            blocks = [n_block.split(),]
        else:
            blocks = [n_block.replace(sep,' ').split(),]
        n_block = 1
    blocks = np.array(blocks,dtype='int')

    def multi_replace(pa):
        n,s = pa.group(0).split('*')
        f = (s+' ')*int(n)
        return f
    data = fp.read()
    if sep is not None:
        data = data.replace(sep,' ')
    if data.find(',')!=-1:
        data = data.replace(',',' ')
    if data.find('*')!=-1:
        data = re.sub('\d+\*\S+',multi_replace,data)
        n = data.find('*')
    data = np.array(data.split(),dtype='float64')
    a = 0
    for i,j,k in blocks:
        a+=i*j*k
    dimension = len(blocks[0])
    np_dim = data.size // a
    assert a*np_dim == data.size
    size0=0
    result = []
    for shape in blocks:
        if dimension==3:
            imax,jmax,kmax = shape
            size = imax*jmax*kmax*np_dim
        else:
            imax,jmax = shape
            size = imax*jmax*np_dim

        bl_data = data[size0:size0+size]
        size0 += size 
        if dimension == 3:
            bl_data.shape = (np_dim,kmax,jmax,imax)
            bl_data = bl_data.transpose((0,3,2,1))
            t = dict(zip('XYZ',bl_data))
        else:
            bl_data.shape = (np_dim,jmax,imax)
            bl_data = bl_data.swapaxes(2,1)
            t = dict(zip('XY',bl_data))
        if dimension != np_dim:
            # exists IBLANK
            t['IBLANK'] = bl_data[-1]
        result.append(t)
    return result
def write_plot3d_fmt(data,filename,fmt='%.15e'):
    '''
    data:list-like,element is a dict like {'X':...,'Y':...,'Z':...,'IBLANK':...}
    Z and IBLANK are optional
    '''
    fp = open(filename,'w')

    IBLANK =False if not data[0].get('IBLANK',False) else True
    dimension =2 if data[0].get('Z',False) is False else 3

    if len(data) > 1:
        fp.write('{:5d}\n'.format(len(data)))
    for i in data:
        shape = i['X'].shape
        if dimension == 3:
            s_format = '  {} {} {}\n'
        else:
            s_format = '  {} {}\n'
        fp.write(s_format.format(*shape))

    for i in data:
        if IBLANK is not False:
            if dimension == 3:
                t = (i['X'],i['Y'],i['Z'],i['IBLANK'])
            else:
                t = (i['X'],i['Y'],i['IBLANK'])
        else:
            if dimension == 3:
                t = (i['X'],i['Y'],i['Z'])
            else:
                t = (i['X'],i['Y']) 
        t = np.stack(t)
        if dimension == 3:
            t_shape = (0,3,2,1)
        else:
            t_shape = (0,2,1)
        array = t.transpose(t_shape).reshape(-1,i['X'].shape[0])
        np.savetxt(fp,array,fmt = fmt)

    fp.close()
    return
def read_plot3d_unfmt(filename):
    float_type = {4:'float32',8:'float64'}
    fp = open(filename,'rb')
    n_blocks = np.frombuffer(fp.read(12), dtype = 'int32')[1]

    k = np.frombuffer(fp.read(4), dtype= 'int32' )[0]
    blocks = np.frombuffer(fp.read(k), dtype = 'int32').reshape(n_blocks,-1)
    fp.read(4)
    dimension = (k // 4) // n_blocks

    result = []
    precision=None
    for shape in blocks:
        k = np.frombuffer(fp.read(4), dtype= 'int32' )[0]
        
        if dimension==3:
            imax,jmax,kmax = shape
            size = imax*jmax*kmax
        else:
            imax,jmax = shape
            size = imax*jmax
        if precision is None:
            precision = k //(size) //dimension 
            if precision ==4 or precision == 8:
                IBLANK = False 
                np_dim = dimension
            else:
                np_dim = dimension + 1
                precision = k //(size) //np_dim
                IBLANK = True
        bl_data = np.frombuffer(fp.read(k),dtype = float_type[precision])
        fp.read(4)
        if dimension == 3:
            bl_data.shape = (np_dim,kmax,jmax,imax)
            bl_data = bl_data.transpose((0,3,2,1))
            t = dict(zip('XYZ',bl_data))
        else:
            bl_data.shape = (np_dim,jmax,imax)
            bl_data = bl_data.swapaxes(2,1)
            t = dict(zip('XY',bl_data))
        if IBLANK:
            t['IBLANK'] = bl_data[-1]
        result.append(t)
    return result

def write_plot3d_unfmt(data,filename):
    '''
    data:list-like,element is a dict like {'X':...,'Y':...,'Z':...,'IBLANK':...}
    Z and IBLANK are optional
    '''
    fp = open(filename,'wb')
    k_array = np.array([4],dtype = 'int32')
    if len(data) > 1:
        k_array.tofile(fp)
        k_array[0] = len(data)
        k_array.tofile(fp)
        k_array[0]=4
        k_array.tofile(fp)
    shapes = [i['X'].shape for i in data]
    t = np.array(shapes,dtype='int32').flatten()
    k_array[0]=t.size*4
    k_array.tofile(fp)
    t.tofile(fp)
    k_array.tofile(fp)

    IBLANK = data[0].get('IBLANK',False)
    dimension = data[0].get('Z',False)
    if dimension is False:
        dimension = 2
    else:
        dimension = 3

    for i in data:
        if IBLANK is not False:
            if dimension == 3:
                t = (i['X'],i['Y'],i['Z'],i['IBLANK'])
            else:
                t = (i['X'],i['Y'],i['IBLANK'])
        else:
            if dimension == 3:
                t = (i['X'],i['Y'],i['Z'])
            else:
                t = (i['X'],i['Y']) 
        t = np.stack(t)
        if dimension == 3:
            t_shape = (0,3,2,1)
        else:
            t_shape = (0,2,1)
        array = t.transpose(t_shape).flatten()
        
        k_array[0] = array.size*array.itemsize
        k_array.tofile(fp)
        array.tofile(fp)
        k_array.tofile(fp)
    fp.close()
    return
def read(filename):
    p = Path(filename)
    if p.suffix.lower() in ['.fmt']:
        return read_plot3d_fmt(filename)
    else:
        return read_plot3d_unfmt(filename)
def write(data,filename):
    p = Path(filename)
    if p.suffix.lower() in ['.fmt']:
        return write_plot3d_fmt(data,filename)
    else:
        return write_plot3d_unfmt(data,filename)
if __name__=='__main__':
    t = read('rotstat.fmt')
    write('plot3d_unfmt.g',t)
    write('plot3d_fmt.fmt',t)
    t = read('plot3d_fmt.fmt')
    write('plot3d_unfmt2.g',t)