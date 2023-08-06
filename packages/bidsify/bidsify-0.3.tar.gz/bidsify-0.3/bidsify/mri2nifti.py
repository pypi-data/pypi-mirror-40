from __future__ import print_function, division
import os
import os.path as op
from glob import glob
from .utils import check_executable, _compress, _run_cmd
from shutil import rmtree

PIGZ = check_executable('pigz')


def convert_mri(directory, cfg):

    compress = not cfg['options']['debug']
    mri_ext = cfg['options']['mri_ext']

    base_cmd = "dcm2niix -ba y"
    if compress:
        base_cmd += " -z y" if PIGZ else " -z i"
    else:
        base_cmd += " -z n"

    if mri_ext in ['PAR', 'dcm']:
        mri_files = glob(op.join(directory, '*.%s' % mri_ext))
        for f in mri_files:
            basename, ext = op.splitext(op.basename(f))
            par_cmd = base_cmd + " -f %s %s" % (basename, f)
            # if debug, print dcm2niix output
            _run_cmd(par_cmd.split(' '), verbose=cfg['options']['debug'])
            os.remove(f)
            if mri_ext == 'PAR':
                os.remove(f.replace('.%s' % mri_ext, '.REC'))

    elif mri_ext == 'DICOM':
        # Experimental enh DICOM conversion
        dcm_cmd = base_cmd + " -f %n_%p " + directory
        _run_cmd(dcm_cmd.split(' '))

        if op.isdir(op.join(directory, 'DICOM')):
            rmtree(op.join(directory, 'DICOM'))
        
        if op.isfile(op.join(directory, 'DICOMDIR')):
            os.remove(op.join(directory, 'DICOMDIR'))

        im_files = glob(op.join(directory, 'IM_????'))
        _ = [os.remove(f) for f in im_files]

        ps_files = glob(op.join(directory, 'PS_????'))
        _ = [os.remove(f) for f in ps_files]

        xx_files = glob(op.join(directory, 'XX_????'))
        _ = [os.remove(f) for f in xx_files]
    else:
        raise ValueError('Please select either PAR or DICOM for mri_ext!')

    niis = glob(op.join(directory, '*.nii'))
    if compress:
        for nii in niis:
            _compress(nii)
            os.remove(nii)

    _rename_phasediff_files(directory, idf='phasediff')


def _rename_phasediff_files(directory, idf='phasediff'):
    """ Renames Philips "B0" files (1 phasediff / 1 magnitude) because dcm2niix
    appends (or sometimes prepends) '_ph' to the filename after conversion.
    """

    b0_files = glob(op.join(directory, '*%s*' % idf))

    for f in b0_files:
        # Old version of dcm2niix
        new_name = f.replace('_phMag.json', '_phasediff.json')
        new_name = new_name.replace('_phMag_1', '_phasediff')
        new_name = new_name.replace('_phMag_2', '_magnitude1')

        # New version of dcm2niix
        new_name = new_name.replace('e1', 'magnitude1')
        new_name = new_name.replace('e2', 'phasediff')

        os.rename(f, new_name)

    # Hack for latest dcm2niix version
    real_f = [f for f in b0_files if 'real' in f]
    if len(real_f) > 2:
        msg = "Found %i B0-files with 'real' in its filename: %s" % (len(real_f), real_f,)
        raise ValueError(msg)
    elif len(real_f) == 2:
        json_file = [f for f in real_f if '.json' in f][0]
        phasediff_file = [f for f in real_f if '.json' not in f][0]
        magn_file = [f for f in b0_files if 'real' not in f and '.json' not in f][0]
        magn_json_f = [f for f in b0_files if 'real' not in f and 'json' in f][0]
        
        os.remove(magn_json_f)
        os.rename(magn_file, magn_file.replace('phasediff', 'magnitude1'))
        os.rename(phasediff_file, phasediff_file.replace('_real', ''))
    else:
        pass  # just skip it
