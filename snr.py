#!/bin/python
import os, sys
import pandas as pd

# ----- Config ----- #
Np = 2
Ttime = 5 * 60  # In seconds
Wfrac = 5  # Assuming 5% pulse width


# csvfile = "/home/obs/target_logs/PULSARS"
#
# ------------------ #

def process(filfile):
    fname = filfile.split('/')[-1].strip('.fil')

    # Get Session ID
    SessionID = '*'
    tmp = "_".join(fname.split("_")[1:4])
    if tmp[:4] == "AGBT": SessionID = tmp

    # print SessionID

    # Read CSV file

    cmd = "echo %s | sed 's/Psr/PSR/' | sed 's/psr/PSR/' | awk -F_PSR_ '{print $2}' | awk -F_ '{print $1}' | sed 's/j/J/' | sed 's/b/B/'" % (
        filfile)
    PSRNAME = os.popen(cmd).readline().strip()
    print(PSRNAME)
    # print PSRNAME

    cmd = "psrcat -e %s > tmp.par" % (PSRNAME)
    os.system(cmd)

    cmd = "dspsr -E tmp.par %s -O %s" % (filfile, fname)
    print(cmd)
    c = os.system(cmd)

    cmd = "paz -r -L -b -d -m %s.ar" % (fname)
    os.system(cmd)

    cmd = "psrstat -jDF -c 'snr=modular:{on=minimum:{find_min=0,smooth:width=0.05}}' -c snr %s.ar " % (fname)
    print(cmd)
    SNR = float(os.popen(cmd).readline().strip().split("=")[1])

    # Off pulse rms
    cmd = "psrstat -jDF -c 'snr=modular:{on=minimum:{find_min=0,smooth:width=0.05}}' -c off:rms %s.ar" % (fname)
    RMS = float(os.popen(cmd).readline().strip().split("=")[1])

    # Center frequency
    # FREQ = pfdfl.lofreq - 0.5*pfdfl.chan_wid + pfdfl.chan_wid*(pfdfl.numchan/2)
    cmd = "psredit -c freq %s.ar" % (fname)
    FREQ = float(os.popen(cmd).readline().strip().split("=")[1])

    cmd = "psredit -c bw %s.ar" % (fname)
    BW = float(os.popen(cmd).readline().strip().split("=")[1])
    BWMHz = BW
    BW = abs(BW * pow(10, 6))  # In Hz

    # Get MJD
    # cmd = "header %s -tstart" % (filfile)
    # MJD = os.popen(cmd).readline().strip()
    # print(SNR)

    BWfact = 0.9

    # SEFD
    if FREQ < 2000:
        SEFD = 10  # For GBT-L band
        BWfact = 0.6  # For GBT-BL only uses about 60% of the band
    if FREQ > 2000 and FREQ < 3000: SEFD = 12  # GBT-S band
    if FREQ > 3000 and FREQ < 8000: SEFD = 10  # GBT-C band
    if FREQ > 8000 and FREQ < 12000: SEFD = 15  # GBT-X band
    if FREQ > 1200D0 and FREQ < 18000: SEFD = 15  # GBT Ku-band
    if FREQ > 18000 and FREQ < 26000: SEFD = 25  # GBT KFPA-band
    if FREQ > 26000: raise ValueError('Need SEFD value for FREQ>26 GHz.')

    # Only for 80% of the band, we have sufficient sensitivity.
    BW = BWfact * BW

    # Get spectral index
    cmd = "psrcat -c 'SPINDX' -o short -nohead -nonumber " + str(PSRNAME) + " 2>&1 "
    SPINDEX = os.popen(cmd).readline().strip()

    # If not in the catalogue, then assume -1.4 (Bates et al. 2013)
    if SPINDEX == "*":
        SPINDEX = -1.4
    else:
        SPINDEX = float(SPINDEX)

    # Flux at 1400 MHz
    cmd = "psrcat -c 'S1400' -o short -nohead -nonumber " + str(PSRNAME) + " 2>&1 "
    S1400 = float(os.popen(cmd).readline().strip())

    # Flux at the observing frequency
    FLUX = S1400 * pow((FREQ / 1400.0), SPINDEX)

    # Expected average profile SNR
    expSNR = FLUX * pow(10, -3) * pow(Np * Ttime * BW, 0.5) / (1.16 * SEFD)
    print(SNR)
    print(expSNR)
    return {"SNR": SNR, "expSNR": expSNR}
