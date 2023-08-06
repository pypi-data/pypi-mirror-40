; ModuleID = '/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder/proj_simple_adder/solution2/.autopilot/db/a.o.bc'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@.str = private unnamed_addr constant [1 x i8] zeroinitializer, align 1 ; [#uses=1 type=[1 x i8]*]

; [#uses=0]
define i32 @_Z12simple_adderii(i32 %a, i32 %b) nounwind uwtable {
  %1 = alloca i32, align 4                        ; [#uses=2 type=i32*]
  %2 = alloca i32, align 4                        ; [#uses=2 type=i32*]
  %c = alloca i32, align 4                        ; [#uses=2 type=i32*]
  store i32 %a, i32* %1, align 4
  call void @llvm.dbg.declare(metadata !{i32* %1}, metadata !19), !dbg !20 ; [debug line = 1:22] [debug variable = a]
  store i32 %b, i32* %2, align 4
  call void @llvm.dbg.declare(metadata !{i32* %2}, metadata !21), !dbg !22 ; [debug line = 1:29] [debug variable = b]
  call void (...)* @_ssdm_op_SpecPipeline(i32 -1, i32 1, i32 1, i32 0, i8* getelementptr inbounds ([1 x i8]* @.str, i32 0, i32 0)) nounwind, !dbg !23 ; [debug line = 2:1]
  call void @llvm.dbg.declare(metadata !{i32* %c}, metadata !25), !dbg !26 ; [debug line = 3:6] [debug variable = c]
  %3 = load i32* %1, align 4, !dbg !27            ; [#uses=1 type=i32] [debug line = 4:2]
  %4 = load i32* %2, align 4, !dbg !27            ; [#uses=1 type=i32] [debug line = 4:2]
  %5 = add nsw i32 %3, %4, !dbg !27               ; [#uses=1 type=i32] [debug line = 4:2]
  store i32 %5, i32* %c, align 4, !dbg !27        ; [debug line = 4:2]
  %6 = load i32* %c, align 4, !dbg !28            ; [#uses=1 type=i32] [debug line = 5:2]
  ret i32 %6, !dbg !28                            ; [debug line = 5:2]
}

; [#uses=3]
declare void @llvm.dbg.declare(metadata, metadata) nounwind readnone

; [#uses=1]
declare void @_ssdm_op_SpecPipeline(...) nounwind

!llvm.dbg.cu = !{!0}
!opencl.kernels = !{!12}
!hls.encrypted.func = !{}

!0 = metadata !{i32 786449, i32 0, i32 4, metadata !"/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder/proj_simple_adder/solution2/.autopilot/db/dut.pragma.2.cpp", metadata !"/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder", metadata !"clang version 3.1 ", i1 true, i1 false, metadata !"", i32 0, metadata !1, metadata !1, metadata !3, metadata !1} ; [ DW_TAG_compile_unit ]
!1 = metadata !{metadata !2}
!2 = metadata !{i32 0}
!3 = metadata !{metadata !4}
!4 = metadata !{metadata !5}
!5 = metadata !{i32 786478, i32 0, metadata !6, metadata !"simple_adder", metadata !"simple_adder", metadata !"_Z12simple_adderii", metadata !6, i32 1, metadata !7, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32, i32)* @_Z12simple_adderii, null, null, metadata !10, i32 1} ; [ DW_TAG_subprogram ]
!6 = metadata !{i32 786473, metadata !"src/dut.cpp", metadata !"/mnt/centos_share/Vivado_Projects/hlsclt/hlsclt/examples/simple_adder", null} ; [ DW_TAG_file_type ]
!7 = metadata !{i32 786453, i32 0, metadata !"", i32 0, i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !8, i32 0, i32 0} ; [ DW_TAG_subroutine_type ]
!8 = metadata !{metadata !9, metadata !9, metadata !9}
!9 = metadata !{i32 786468, null, metadata !"int", null, i32 0, i64 32, i64 32, i64 0, i32 0, i32 5} ; [ DW_TAG_base_type ]
!10 = metadata !{metadata !11}
!11 = metadata !{i32 786468}                      ; [ DW_TAG_base_type ]
!12 = metadata !{i32 (i32, i32)* @_Z12simple_adderii, metadata !13, metadata !14, metadata !15, metadata !16, metadata !17, metadata !18}
!13 = metadata !{metadata !"kernel_arg_addr_space", i32 0, i32 0}
!14 = metadata !{metadata !"kernel_arg_access_qual", metadata !"none", metadata !"none"}
!15 = metadata !{metadata !"kernel_arg_type", metadata !"int", metadata !"int"}
!16 = metadata !{metadata !"kernel_arg_type_qual", metadata !"", metadata !""}
!17 = metadata !{metadata !"kernel_arg_name", metadata !"a", metadata !"b"}
!18 = metadata !{metadata !"reqd_work_group_size", i32 1, i32 1, i32 1}
!19 = metadata !{i32 786689, metadata !5, metadata !"a", metadata !6, i32 16777217, metadata !9, i32 0, i32 0} ; [ DW_TAG_arg_variable ]
!20 = metadata !{i32 1, i32 22, metadata !5, null}
!21 = metadata !{i32 786689, metadata !5, metadata !"b", metadata !6, i32 33554433, metadata !9, i32 0, i32 0} ; [ DW_TAG_arg_variable ]
!22 = metadata !{i32 1, i32 29, metadata !5, null}
!23 = metadata !{i32 2, i32 1, metadata !24, null}
!24 = metadata !{i32 786443, metadata !5, i32 1, i32 32, metadata !6, i32 0} ; [ DW_TAG_lexical_block ]
!25 = metadata !{i32 786688, metadata !24, metadata !"c", metadata !6, i32 3, metadata !9, i32 0, i32 0} ; [ DW_TAG_auto_variable ]
!26 = metadata !{i32 3, i32 6, metadata !24, null}
!27 = metadata !{i32 4, i32 2, metadata !24, null}
!28 = metadata !{i32 5, i32 2, metadata !24, null}
