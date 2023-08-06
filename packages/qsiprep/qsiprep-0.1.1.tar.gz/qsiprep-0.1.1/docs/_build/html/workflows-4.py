from qsiprep.workflows.dwi.hmc import init_dwi_hmc_wf
wf = init_dwi_hmc_wf(hmc_transform="Affine",
                     hmc_model="3dSHORE",
                     hmc_align_to="iterative",
                     mem_gb=3,
                     omp_nthreads=1,
                     write_report=False)