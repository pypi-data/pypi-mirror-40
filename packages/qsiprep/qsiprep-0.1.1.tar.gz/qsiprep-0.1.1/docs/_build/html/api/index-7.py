from qsiprep.workflows.fieldmap.syn import init_syn_sdc_wf
wf = init_syn_sdc_wf(
    bold_pe='j',
    omp_nthreads=8)