from fmriprep.workflows.anatomical import init_anat_preproc_wf
wf = init_anat_preproc_wf(omp_nthreads=1,
                          reportlets_dir='.',
                          output_dir='.',
                          template='MNI152NLin2009cAsym',
                          output_spaces=['T1w', 'fsnative',
                                         'template', 'fsaverage5'],
                          output_resolution=1.25,
                          skull_strip_template='OASIS',
                          freesurfer=True,
                          longitudinal=False,
                          debug=False,
                          hires=True,
                          num_t1w=1)