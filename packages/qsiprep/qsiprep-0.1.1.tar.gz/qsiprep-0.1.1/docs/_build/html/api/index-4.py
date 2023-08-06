from qsiprep.workflows.fieldmap import init_sdc_wf
wf = init_sdc_wf(
    fmaps=[{
        'type': 'epi',
        'epi':                     'sub-03/ses-2/fmap/sub-03_ses-2_run-1_epi.nii.gz',
    }],
    dwi_meta={
        'PhaseEncodingDirection': 'j',
    },
)