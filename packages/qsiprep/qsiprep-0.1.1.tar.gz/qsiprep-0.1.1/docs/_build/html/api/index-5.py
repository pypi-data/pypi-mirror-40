from qsiprep.workflows.fieldmap.pepolar import init_pepolar_unwarp_wf
wf = init_pepolar_unwarp_wf(
    dwi_meta={'PhaseEncodingDirection': 'j'},
    epi_fmaps=[('/dataset/sub-01/fmap/sub-01_epi.nii.gz', 'j-')],
    omp_nthreads=8)