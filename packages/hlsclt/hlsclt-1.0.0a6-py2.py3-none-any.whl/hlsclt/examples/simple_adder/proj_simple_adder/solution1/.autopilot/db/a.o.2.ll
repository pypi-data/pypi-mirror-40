; ModuleID = '/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder/proj_simple_adder/solution1/.autopilot/db/a.o.2.bc'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@simple_adder.str = internal unnamed_addr constant [13 x i8] c"simple_adder\00" ; [#uses=1 type=[13 x i8]*]
@.str = private unnamed_addr constant [1 x i8] zeroinitializer, align 1 ; [#uses=1 type=[1 x i8]*]

; [#uses=0]
define i32 @simple_adder(i32 %a, i32 %b) nounwind uwtable readnone {
  call void (...)* @_ssdm_op_SpecBitsMap(i32 %a) nounwind, !map !19
  call void (...)* @_ssdm_op_SpecBitsMap(i32 %b) nounwind, !map !25
  call void (...)* @_ssdm_op_SpecBitsMap(i32 0) nounwind, !map !29
  call void (...)* @_ssdm_op_SpecTopModule([13 x i8]* @simple_adder.str) nounwind
  call void @llvm.dbg.value(metadata !{i32 %a}, i64 0, metadata !35), !dbg !36 ; [debug line = 1:22] [debug variable = a]
  call void @llvm.dbg.value(metadata !{i32 %b}, i64 0, metadata !37), !dbg !38 ; [debug line = 1:29] [debug variable = b]
  call void (...)* @_ssdm_op_SpecPipeline(i32 -1, i32 1, i32 1, i32 0, [1 x i8]* @.str) nounwind, !dbg !39 ; [debug line = 2:1]
  %c = add nsw i32 %a, %b, !dbg !41               ; [#uses=1 type=i32] [debug line = 4:2]
  call void @llvm.dbg.value(metadata !{i32 %c}, i64 0, metadata !42), !dbg !41 ; [debug line = 4:2] [debug variable = c]
  ret i32 %c, !dbg !43                            ; [debug line = 5:2]
}

; [#uses=3]
declare void @llvm.dbg.value(metadata, i64, metadata) nounwind readnone

; [#uses=1]
declare void @_ssdm_op_SpecTopModule(...)

; [#uses=1]
declare void @_ssdm_op_SpecPipeline(...) nounwind

; [#uses=3]
declare void @_ssdm_op_SpecBitsMap(...)

!llvm.dbg.cu = !{!0}
!opencl.kernels = !{!12}
!hls.encrypted.func = !{}
!llvm.map.gv = !{}

!0 = metadata !{i32 786449, i32 0, i32 4, metadata !"/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder/proj_simple_adder/solution1/.autopilot/db/dut.pragma.2.cpp", metadata !"/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder", metadata !"clang version 3.1 ", i1 true, i1 false, metadata !"", i32 0, metadata !1, metadata !1, metadata !3, metadata !1} ; [ DW_TAG_compile_unit ]
!1 = metadata !{metadata !2}
!2 = metadata !{i32 0}
!3 = metadata !{metadata !4}
!4 = metadata !{metadata !5}
!5 = metadata !{i32 786478, i32 0, metadata !6, metadata !"simple_adder", metadata !"simple_adder", metadata !"_Z12simple_adderii", metadata !6, i32 1, metadata !7, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32, i32)* @simple_adder, null, null, metadata !10, i32 1} ; [ DW_TAG_subprogram ]
!6 = metadata !{i32 786473, metadata !"src/dut.cpp", metadata !"/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder", null} ; [ DW_TAG_file_type ]
!7 = metadata !{i32 786453, i32 0, metadata !"", i32 0, i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !8, i32 0, i32 0} ; [ DW_TAG_subroutine_type ]
!8 = metadata !{metadata !9, metadata !9, metadata !9}
!9 = metadata !{i32 786468, null, metadata !"int", null, i32 0, i64 32, i64 32, i64 0, i32 0, i32 5} ; [ DW_TAG_base_type ]
!10 = metadata !{metadata !11}
!11 = metadata !{i32 786468}                      ; [ DW_TAG_base_type ]
!12 = metadata !{i32 (i32, i32)* @simple_adder, metadata !13, metadata !14, metadata !15, metadata !16, metadata !17, metadata !18}
!13 = metadata !{metadata !"kernel_arg_addr_space", i32 0, i32 0}
!14 = metadata !{metadata !"kernel_arg_access_qual", metadata !"none", metadata !"none"}
!15 = metadata !{metadata !"kernel_arg_type", metadata !"int", metadata !"int"}
!16 = metadata !{metadata !"kernel_arg_type_qual", metadata !"", metadata !""}
!17 = metadata !{metadata !"kernel_arg_name", metadata !"a", metadata !"b"}
!18 = metadata !{metadata !"reqd_work_group_size", i32 1, i32 1, i32 1}
!19 = metadata !{metadata !20}
!20 = metadata !{i32 0, i32 31, metadata !21}
!21 = metadata !{metadata !22}
!22 = metadata !{metadata !"a", metadata !23, metadata !"int", i32 0, i32 31}
!23 = metadata !{metadata !24}
!24 = metadata !{i32 0, i32 0, i32 0}
!25 = metadata !{metadata !26}
!26 = metadata !{i32 0, i32 31, metadata !27}
!27 = metadata !{metadata !28}
!28 = metadata !{metadata !"b", metadata !23, metadata !"int", i32 0, i32 31}
!29 = metadata !{metadata !30}
!30 = metadata !{i32 0, i32 31, metadata !31}
!31 = metadata !{metadata !32}
!32 = metadata !{metadata !"return", metadata !33, metadata !"int", i32 0, i32 31}
!33 = metadata !{metadata !34}
!34 = metadata !{i32 0, i32 1, i32 0}
!35 = metadata !{i32 786689, metadata !5, metadata !"a", metadata !6, i32 16777217, metadata !9, i32 0, i32 0} ; [ DW_TAG_arg_variable ]
!36 = metadata !{i32 1, i32 22, metadata !5, null}
!37 = metadata !{i32 786689, metadata !5, metadata !"b", metadata !6, i32 33554433, metadata !9, i32 0, i32 0} ; [ DW_TAG_arg_variable ]
!38 = metadata !{i32 1, i32 29, metadata !5, null}
!39 = metadata !{i32 2, i32 1, metadata !40, null}
!40 = metadata !{i32 786443, metadata !5, i32 1, i32 32, metadata !6, i32 0} ; [ DW_TAG_lexical_block ]
!41 = metadata !{i32 4, i32 2, metadata !40, null}
!42 = metadata !{i32 786688, metadata !40, metadata !"c", metadata !6, i32 3, metadata !9, i32 0, i32 0} ; [ DW_TAG_auto_variable ]
!43 = metadata !{i32 5, i32 2, metadata !40, null}
