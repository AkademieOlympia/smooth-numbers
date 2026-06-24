// Lean compiler output
// Module: CatalanNormalform.CatalanNumbers
// Imports: public import Init public meta import Init public import Mathlib.Data.Nat.Basic public import Mathlib.Data.Nat.Factorial.Basic public import Mathlib.Data.Nat.Choose.Basic public import Mathlib.Tactic.Ring public import Mathlib.Tactic.Linarith public import CatalanNormalform.CTree
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* lp_mathlib_Nat_fast__choose(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* lean_nat_div(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan__rec(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan__rec___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan(lean_object* v_n_1_){
_start:
{
lean_object* v___x_2_; lean_object* v___x_3_; lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; 
v___x_2_ = lean_unsigned_to_nat(2u);
v___x_3_ = lean_nat_mul(v___x_2_, v_n_1_);
v___x_4_ = lp_mathlib_Nat_fast__choose(v___x_3_, v_n_1_);
lean_dec(v___x_3_);
v___x_5_ = lean_unsigned_to_nat(1u);
v___x_6_ = lean_nat_add(v_n_1_, v___x_5_);
v___x_7_ = lean_nat_div(v___x_4_, v___x_6_);
lean_dec(v___x_6_);
lean_dec(v___x_4_);
return v___x_7_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan___boxed(lean_object* v_n_8_){
_start:
{
lean_object* v_res_9_; 
v_res_9_ = lp_catalan_x2dnormalform_CatalanNumbers_catalan(v_n_8_);
lean_dec(v_n_8_);
return v_res_9_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan__rec(lean_object* v_x_10_){
_start:
{
lean_object* v_zero_11_; uint8_t v_isZero_12_; 
v_zero_11_ = lean_unsigned_to_nat(0u);
v_isZero_12_ = lean_nat_dec_eq(v_x_10_, v_zero_11_);
if (v_isZero_12_ == 1)
{
lean_object* v___x_13_; 
v___x_13_ = lean_unsigned_to_nat(1u);
return v___x_13_;
}
else
{
lean_object* v_one_14_; lean_object* v_n_15_; uint8_t v_isZero_16_; 
v_one_14_ = lean_unsigned_to_nat(1u);
v_n_15_ = lean_nat_sub(v_x_10_, v_one_14_);
v_isZero_16_ = lean_nat_dec_eq(v_n_15_, v_zero_11_);
if (v_isZero_16_ == 1)
{
lean_dec(v_n_15_);
return v_one_14_;
}
else
{
lean_object* v_n_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; lean_object* v___x_22_; lean_object* v___x_23_; lean_object* v___x_24_; lean_object* v___x_25_; lean_object* v___x_26_; lean_object* v___x_27_; 
v_n_17_ = lean_nat_sub(v_n_15_, v_one_14_);
lean_dec(v_n_15_);
v___x_18_ = lean_unsigned_to_nat(4u);
v___x_19_ = lean_nat_add(v_n_17_, v_one_14_);
v___x_20_ = lean_nat_mul(v___x_18_, v___x_19_);
v___x_21_ = lean_unsigned_to_nat(2u);
v___x_22_ = lean_nat_add(v___x_20_, v___x_21_);
lean_dec(v___x_20_);
v___x_23_ = lp_catalan_x2dnormalform_CatalanNumbers_catalan__rec(v___x_19_);
lean_dec(v___x_19_);
v___x_24_ = lean_nat_mul(v___x_22_, v___x_23_);
lean_dec(v___x_23_);
lean_dec(v___x_22_);
v___x_25_ = lean_unsigned_to_nat(3u);
v___x_26_ = lean_nat_add(v_n_17_, v___x_25_);
lean_dec(v_n_17_);
v___x_27_ = lean_nat_div(v___x_24_, v___x_26_);
lean_dec(v___x_26_);
lean_dec(v___x_24_);
return v___x_27_;
}
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CatalanNumbers_catalan__rec___boxed(lean_object* v_x_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_catalan_x2dnormalform_CatalanNumbers_catalan__rec(v_x_28_);
lean_dec(v_x_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter___redArg(lean_object* v_x_30_, lean_object* v_h__1_31_, lean_object* v_h__2_32_, lean_object* v_h__3_33_){
_start:
{
lean_object* v_zero_34_; uint8_t v_isZero_35_; 
v_zero_34_ = lean_unsigned_to_nat(0u);
v_isZero_35_ = lean_nat_dec_eq(v_x_30_, v_zero_34_);
if (v_isZero_35_ == 1)
{
lean_object* v___x_36_; lean_object* v___x_37_; 
lean_dec(v_h__3_33_);
lean_dec(v_h__2_32_);
v___x_36_ = lean_box(0);
v___x_37_ = lean_apply_1(v_h__1_31_, v___x_36_);
return v___x_37_;
}
else
{
lean_object* v_one_38_; lean_object* v_n_39_; uint8_t v_isZero_40_; 
lean_dec(v_h__1_31_);
v_one_38_ = lean_unsigned_to_nat(1u);
v_n_39_ = lean_nat_sub(v_x_30_, v_one_38_);
v_isZero_40_ = lean_nat_dec_eq(v_n_39_, v_zero_34_);
if (v_isZero_40_ == 1)
{
lean_object* v___x_41_; lean_object* v___x_42_; 
lean_dec(v_n_39_);
lean_dec(v_h__3_33_);
v___x_41_ = lean_box(0);
v___x_42_ = lean_apply_1(v_h__2_32_, v___x_41_);
return v___x_42_;
}
else
{
lean_object* v_n_43_; lean_object* v___x_44_; 
lean_dec(v_h__2_32_);
v_n_43_ = lean_nat_sub(v_n_39_, v_one_38_);
lean_dec(v_n_39_);
v___x_44_ = lean_apply_1(v_h__3_33_, v_n_43_);
return v___x_44_;
}
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter___redArg___boxed(lean_object* v_x_45_, lean_object* v_h__1_46_, lean_object* v_h__2_47_, lean_object* v_h__3_48_){
_start:
{
lean_object* v_res_49_; 
v_res_49_ = lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter___redArg(v_x_45_, v_h__1_46_, v_h__2_47_, v_h__3_48_);
lean_dec(v_x_45_);
return v_res_49_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter(lean_object* v_motive_50_, lean_object* v_x_51_, lean_object* v_h__1_52_, lean_object* v_h__2_53_, lean_object* v_h__3_54_){
_start:
{
lean_object* v_zero_55_; uint8_t v_isZero_56_; 
v_zero_55_ = lean_unsigned_to_nat(0u);
v_isZero_56_ = lean_nat_dec_eq(v_x_51_, v_zero_55_);
if (v_isZero_56_ == 1)
{
lean_object* v___x_57_; lean_object* v___x_58_; 
lean_dec(v_h__3_54_);
lean_dec(v_h__2_53_);
v___x_57_ = lean_box(0);
v___x_58_ = lean_apply_1(v_h__1_52_, v___x_57_);
return v___x_58_;
}
else
{
lean_object* v_one_59_; lean_object* v_n_60_; uint8_t v_isZero_61_; 
lean_dec(v_h__1_52_);
v_one_59_ = lean_unsigned_to_nat(1u);
v_n_60_ = lean_nat_sub(v_x_51_, v_one_59_);
v_isZero_61_ = lean_nat_dec_eq(v_n_60_, v_zero_55_);
if (v_isZero_61_ == 1)
{
lean_object* v___x_62_; lean_object* v___x_63_; 
lean_dec(v_n_60_);
lean_dec(v_h__3_54_);
v___x_62_ = lean_box(0);
v___x_63_ = lean_apply_1(v_h__2_53_, v___x_62_);
return v___x_63_;
}
else
{
lean_object* v_n_64_; lean_object* v___x_65_; 
lean_dec(v_h__2_53_);
v_n_64_ = lean_nat_sub(v_n_60_, v_one_59_);
lean_dec(v_n_60_);
v___x_65_ = lean_apply_1(v_h__3_54_, v_n_64_);
return v___x_65_;
}
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter___boxed(lean_object* v_motive_66_, lean_object* v_x_67_, lean_object* v_h__1_68_, lean_object* v_h__2_69_, lean_object* v_h__3_70_){
_start:
{
lean_object* v_res_71_; 
v_res_71_ = lp_catalan_x2dnormalform___private_CatalanNormalform_CatalanNumbers_0__CatalanNumbers_catalan__rec_match__1_splitter(v_motive_66_, v_x_67_, v_h__1_68_, v_h__2_69_, v_h__3_70_);
lean_dec(v_x_67_);
return v_res_71_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Nat_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Nat_Factorial_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Nat_Choose_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_Ring(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_Linarith(uint8_t builtin);
lean_object* initialize_catalan_x2dnormalform_CatalanNormalform_CTree(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_catalan_x2dnormalform_CatalanNormalform_CatalanNumbers(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Nat_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Nat_Factorial_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Nat_Choose_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic_Ring(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic_Linarith(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_catalan_x2dnormalform_CatalanNormalform_CTree(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
