# Withheld provenance files

Ten run-of-record files are held back during blind review because they record absolute
paths of the machine the study ran on, which include a user name. They are unchanged and
will be published in this directory after review. Their sha256 values are listed below so
the released files can be checked against this commitment.

The design lock (`full/development/design_lock.json`) is among them. It records the
scientific core hash `0959a70c7605b8fe…`, which is the hash the notebook in
`results/models/public_statsbomb_causal_study.ipynb` still produces
(`PublicCausal.notebook_runtime.export_notebook_core`).

```
e06ca48540909aa200ff2d363afab6da1a06220591e2a53f1b0da71e4de880c6  full/confirmation/config.json
b8eb13f844bd1f7513aabbfef62be11d6ba77d61e9a47f50e11f632e50867581  full/confirmation/environment.json
34599e66b27ff695999e467d622212bb36958ab022beda12995334685b6f8281  full/confirmation/phase_result.json
7570cca47ad1a19cb0f4586bbc195182c0d29c42e085e38b9ae9ac8b078c567e  full/confirmation/provenance.json
bd5d6f773eab35d19e09967b72406992327c27670945680a7d4104af05ccc40f  full/development/design_lock.json
fd2a41621faf17402da230f8b8b766c7de2f2e4a4dc3eb4313624a25dd72f210  full/development/phase_result.json
d06c8cb7563c4d6dbb88d5193f9b0a6de9ee6f8d9bca96f2e7c8f0ddece36ab6  full/execution_provenance.json
711b61277fc57cf1b5ca3922feeab65b12b0b3a956e4ad0604ce7bfe46ab1867  full/run_config.json
6dbd6004114e4eabe84d58edd3b82374fff9a7c02f94c495140c6fddbc52ca62  integrity_manifest.json
9e80a6ac72117d3e014a38fcf0802eb12e45f5ca4537cf59c3d1582cf3cd228a  manifests/implementation_tests.json
```
