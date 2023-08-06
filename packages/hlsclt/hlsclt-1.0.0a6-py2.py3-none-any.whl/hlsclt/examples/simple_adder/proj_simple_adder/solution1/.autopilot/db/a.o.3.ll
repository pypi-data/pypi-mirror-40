; ModuleID = '/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder/proj_simple_adder/solution1/.autopilot/db/a.o.3.bc'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@simple_adder_str = internal unnamed_addr constant [13 x i8] c"simple_adder\00" ; [#uses=1 type=[13 x i8]*]
@p_str = private unnamed_addr constant [1 x i8] zeroinitializer, align 1 ; [#uses=1 type=[1 x i8]*]

; [#uses=0]
define i32 @simple_adder(i32 %a, i32 %b) nounwind uwtable readnone {
  call void (...)* @_ssdm_op_SpecBitsMap(i32 %a) nounwind, !map !7
  call void (...)* @_ssdm_op_SpecBitsMap(i32 %b) nounwind, !map !13
  call void (...)* @_ssdm_op_SpecBitsMap(i32 0) nounwind, !map !17
  call void (...)* @_ssdm_op_SpecTopModule([13 x i8]* @simple_adder_str) nounwind
  %b_read = call i32 @_ssdm_op_Read.ap_auto.i32(i32 %b) nounwind ; [#uses=1 type=i32]
  call void @llvm.dbg.value(metadata !{i32 %b_read}, i64 0, metadata !23), !dbg !31 ; [debug line = 1:29] [debug variable = b]
  %a_read = call i32 @_ssdm_op_Read.ap_auto.i32(i32 %a) nounwind ; [#uses=1 type=i32]
  call void @llvm.dbg.value(metadata !{i32 %a_read}, i64 0, metadata !32), !dbg !33 ; [debug line = 1:22] [debug variable = a]
  call void @llvm.dbg.value(metadata !{i32 %a}, i64 0, metadata !32), !dbg !33 ; [debug line = 1:22] [debug variable = a]
  call void @llvm.dbg.value(metadata !{i32 %b}, i64 0, metadata !23), !dbg !31 ; [debug line = 1:29] [debug variable = b]
  call void (...)* @_ssdm_op_SpecPipeline(i32 -1, i32 1, i32 1, i32 0, [1 x i8]* @p_str) nounwind, !dbg !34 ; [debug line = 2:1]
  %c = add nsw i32 %b_read, %a_read, !dbg !36     ; [#uses=1 type=i32] [debug line = 4:2]
  call void @llvm.dbg.value(metadata !{i32 %c}, i64 0, metadata !37), !dbg !36 ; [debug line = 4:2] [debug variable = c]
  ret i32 %c, !dbg !38                            ; [debug line = 5:2]
}

; [#uses=5]
declare void @llvm.dbg.value(metadata, i64, metadata) nounwind readnone

; [#uses=1]
define weak void @_ssdm_op_SpecTopModule(...) {
entry:
  ret void
}

; [#uses=1]
define weak void @_ssdm_op_SpecPipeline(...) nounwind {
entry:
  ret void
}

; [#uses=3]
define weak void @_ssdm_op_SpecBitsMap(...) {
entry:
  ret void
}

; [#uses=2]
define weak i32 @_ssdm_op_Read.ap_auto.i32(i32) {
entry:
  ret i32 %0
}

!opencl.kernels = !{!0}
!hls.encrypted.func = !{}
!llvm.map.gv = !{}

!0 = metadata !{i32 (i32, i32)* @simple_adder, metadata !1, metadata !2, metadata !3, metadata !4, metadata !5, metadata !6}
!1 = metadata !{metadata !"kernel_arg_addr_space", i32 0, i32 0}
!2 = metadata !{metadata !"kernel_arg_access_qual", metadata !"none", metadata !"none"}
!3 = metadata !{metadata !"kernel_arg_type", metadata !"int", metadata !"int"}
!4 = metadata !{metadata !"kernel_arg_type_qual", metadata !"", metadata !""}
!5 = metadata !{metadata !"kernel_arg_name", metadata !"a", metadata !"b"}
!6 = metadata !{metadata !"reqd_work_group_size", i32 1, i32 1, i32 1}
!7 = metadata !{metadata !8}
!8 = metadata !{i32 0, i32 31, metadata !9}
!9 = metadata !{metadata !10}
!10 = metadata !{metadata !"a", metadata !11, metadata !"int", i32 0, i32 31}
!11 = metadata !{metadata !12}
!12 = metadata !{i32 0, i32 0, i32 0}
!13 = metadata !{metadata !14}
!14 = metadata !{i32 0, i32 31, metadata !15}
!15 = metadata !{metadata !16}
!16 = metadata !{metadata !"b", metadata !11, metadata !"int", i32 0, i32 31}
!17 = metadata !{metadata !18}
!18 = metadata !{i32 0, i32 31, metadata !19}
!19 = metadata !{metadata !20}
!20 = metadata !{metadata !"return", metadata !21, metadata !"int", i32 0, i32 31}
!21 = metadata !{metadata !22}
!22 = metadata !{i32 0, i32 1, i32 0}
!23 = metadata !{i32 786689, metadata !24, metadata !"b", metadata !25, i32 33554433, metadata !28, i32 0, i32 0} ; [ DW_TAG_arg_variable ]
!24 = metadata !{i32 786478, i32 0, metadata !25, metadata !"simple_adder", metadata !"simple_adder", metadata !"_Z12simple_adderii", metadata !25, i32 1, metadata !26, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32, i32)* @simple_adder, null, null, metadata !29, i32 1} ; [ DW_TAG_subprogram ]
!25 = metadata !{i32 786473, metadata !"src/dut.cpp", metadata !"/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder", null} ; [ DW_TAG_file_type ]
!26 = metadata !{i32 786453, i32 0, metadata !"", i32 0, i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !27, i32 0, i32 0} ; [ DW_TAG_subroutine_type ]
!27 = metadata !{metadata !28, metadata !28, metadata !28}
!28 = metadata !{i32 786468, null, metadata !"int", null, i32 0, i64 32, i64 32, i64 0, i32 0, i32 5} ; [ DW_TAG_base_type ]
!29 = metadata !{metadata !30}
!30 = metadata !{i32 786468}                      ; [ DW_TAG_base_type ]
!31 = metadata !{i32 1, i32 29, metadata !24, null}
!32 = metadata !{i32 786689, metadata !24, metadata !"a", metadata !25, i32 16777217, metadata !28, i32 0, i32 0} ; [ DW_TAG_arg_variable ]
!33 = metadata !{i32 1, i32 22, metadata !24, null}
!34 = metadata !{i32 2, i32 1, metadata !35, null}
!35 = metadata !{i32 786443, metadata !24, i32 1, i32 32, metadata !25, i32 0} ; [ DW_TAG_lexical_block ]
!36 = metadata !{i32 4, i32 2, metadata !35, null}
!37 = metadata !{i32 786688, metadata !35, metadata !"c", metadata !25, i32 3, metadata !28, i32 0, i32 0} ; [ DW_TAG_auto_variable ]
!38 = metadata !{i32 5, i32 2, metadata !35, null}
