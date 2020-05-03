<head>
    <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
            skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
            inlineMath: [['$','$']]
            }
        });
    </script>
</head>

# Data Quality Control based on Pulsar Ovservations and System Temperatue #
## Shufan Li ##

### Overview ###
A large amount of GBT observation data is stored at SETI Berkeley data center and hosted through Open Data Archive. But at the moment there are no reliable methods to track the quality of each piece of data. Thus, I find it necessary to privide an accessible approch for researchers to  know which pieces of data re corrupted and which are not. This project measures the observed SNRs of pulsars against the expected ones during an observation to determine the quality of observation data. It stores such information in the header of a hdf5 observation file.
### Proposed Algorithm ###
$$ Score = c_1 \frac{|SNR_{exp}-SNR_{observed}|}{\sigma_{SNR}}+c_2\frac{\sqrt{\int_{tstart}^{tend}|T_{measured}(t)-T_{expected}(t)|^2}dt}{ \sigma_{tsys}\sqrt{\Delta t}}$$
Where:
$c_1$ and $c_2$ are manually adjusted constants for normalization
$\sigma_{SNR}$ is calculated by comparing all identical observations of a particular pulsar against expectations
$\sigma_{tsys}$ is calculated by comparing expected tsys readings and measured ones in the database.

### Implementations ###


**Scheme**

Input: An filterbank file/hdf5 file
Output: a normalized data quality score which can then be writtern into the header of the corresponding file

**Find Observation Session**(Implemented)

The header of a hdf5 file or a filterbank file can imported using blimpy. Even though blimpy can only handle data less than 1 GB, it can still read headers of larger files. We extract observation starting time from the header in MJD form, and use it to find the corresponding observation session.

**Find corelated Plusar Observations**(Implemented)

There are many pulsar calibrations stored on SETI data center at `/mnt_blpd13/datax/cal_and_psrs/`. I have dumped all their headers into a csv file for quick look up. The script will located the closest pulsar observation to a given piece of data as a reference.

**Calculate Observed SNR and expected SNR**(Implemented)

As Vishal has implemented the SNR calculation script, so right now I just make a call to it and extract the expected and observed SNR from the output.  However this script is currently not working on the data center due to dependency issues.

It has many limitations which I'll attempt to improve in the future. First, it is reliant of PSRCHIVE which is not deployed on blpc0 (although I was told that it should be). What's more, it can only take a filterbank file as an input, but somehow I find some old pulsar observations stored as h5 file withouth corresponding filterbank file in the data center, so it might be a good idea to find a way to calculate SNR using pure python to utilize these h5 files and get rid of dependency issues altogether.

**Measure System Temperatue**(Not Implemented)
David has a script `bl_fil_tsys_onoff.rb` deployed at the data center which draw create plots of tsys from filterbank files. I intend to utilize it, and check the calculated tsys against the measured ones.

**Finalizing Algorithm** (Not Implemented)
For this project to truly work in production, we need first to finialize our algorithm by determine the following unknown parameters: $c_1,c_2,\sigma_{SNR},\sigma_{tsys}$
Where $\sigma_{SNR},\sigma_{tsys}$ will be obtained by running prototype script across a large amount of data.

### Conclusion ###
It was unfortunate that this project has not been finished due to assorted disruptions. Nevertheless, it is making considerable progress. I will continue my work on this project as giving up is never my character. I have a full-time summer job as a data mining engineer so I may have limited hours available during the summer. Still, I believe it will be ready for deploy no later than the start of Fall semester.
