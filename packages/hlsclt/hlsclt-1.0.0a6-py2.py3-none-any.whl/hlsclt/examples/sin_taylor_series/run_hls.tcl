open_project proj_sin_taylor_series
set_top sin_taylor_series
add_files src/dut.h
add_files src/dut.cpp
add_files -tb tb/testbench.cpp
open_solution "solution1"
set_part xc7z020clg484-1
create_clock -period 4 -name default
csim_design -clean
exit
