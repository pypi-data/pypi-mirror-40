from fmriprep.workflows.fieldmap.unwarp import init_sdc_unwarp_wf
wf = init_sdc_unwarp_wf(omp_nthreads=8,
                        fmap_demean=True,
                        debug=False)