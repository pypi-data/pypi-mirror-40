from qsiprep.workflows.dwi.resampling import init_dwi_trans_wf
wf = init_dwi_trans_wf(template="ACPC",
                       use_fieldwarp=True,
                       use_compression=True,
                       to_mni=False,
                       write_local_bvecs=True,
                       mem_gb=3,
                       omp_nthreads=1)