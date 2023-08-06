from qsiprep.workflows.dwi.registration import init_b0_to_anat_registration_wf
wf = init_b0_to_anat_registration_wf(
                                     mem_gb=3,
                                     omp_nthreads=1,
                                     transform_type="Rigid",
                                     write_report=False)