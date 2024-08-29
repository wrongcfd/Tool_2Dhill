This is branch for SEM inlet BC files when using pure LBM
## Tools for hdf5 file
1. `xmidslice.py` Slice plane along Z direction
2. `slice.py` Slice plane along X direction
3. `RXX.py` Slice middle line for inlet and middle lines
4. `output_yplus.py` Need further change
## Tools for SEM inlet
1. `SEMLBboundaries.py` coords
2. `SEM_R_LOGINLET.py`  vel, etc.
3. `hill2D.py` generate hill geometry

## Tools for velocity inlet
`VEL_LOGINLETv2g.py` vel inlet

## Tools for post-processing
`CAO_hill_Ux_location.py` Ux validation, read hill location

`CAO_hill_Rxx_location.py` Rii

`CAO_ABL_RXX_zdir.py` Plot middling line and ave line at the same axis

`legend.py` Generate legend label

`Cao_probe_twop.py`  Convergence validation
