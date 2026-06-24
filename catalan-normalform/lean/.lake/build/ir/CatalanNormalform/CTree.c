// Lean compiler output
// Module: CatalanNormalform.CTree
// Imports: public import Init public meta import Init public import Mathlib.Data.Nat.Basic public import Mathlib.Tactic.Basic
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
lean_object* l_Lean_Name_str___override(lean_object*, lean_object*);
lean_object* l_Lean_Name_num___override(lean_object*, lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* lean_sorry(uint8_t);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorElim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorElim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_leaf_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_leaf_elim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_leaf_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_node_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_node_elim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_node_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_string_object lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "CTree.leaf"};
static const lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__0_value;
static const lean_ctor_object lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__0_value)}};
static const lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__1 = (const lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__1_value;
static lean_once_cell_t lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2;
static lean_once_cell_t lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3;
static const lean_string_object lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "CTree.node"};
static const lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__4 = (const lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__4_value;
static const lean_ctor_object lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__4_value)}};
static const lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__5 = (const lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__5_value;
static const lean_ctor_object lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__5_value),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__6 = (const lean_object*)&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__6_value;
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree(lean_object*);
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_two__leaves___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*4 + 0, .m_other = 4, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_catalan_x2dnormalform_CTree_two__leaves___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_two__leaves___closed__0_value;
LEAN_EXPORT const lean_object* lp_catalan_x2dnormalform_CTree_two__leaves = (const lean_object*)&lp_catalan_x2dnormalform_CTree_two__leaves___closed__0_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_three__left___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*4 + 0, .m_other = 4, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_catalan_x2dnormalform_CTree_two__leaves___closed__0_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_catalan_x2dnormalform_CTree_three__left___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_three__left___closed__0_value;
LEAN_EXPORT const lean_object* lp_catalan_x2dnormalform_CTree_three__left = (const lean_object*)&lp_catalan_x2dnormalform_CTree_three__left___closed__0_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_three__right___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*4 + 0, .m_other = 4, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_catalan_x2dnormalform_CTree_two__leaves___closed__0_value)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_three__right___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_three__right___closed__0_value;
LEAN_EXPORT const lean_object* lp_catalan_x2dnormalform_CTree_three__right = (const lean_object*)&lp_catalan_x2dnormalform_CTree_three__right___closed__0_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_four__balanced___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*4 + 0, .m_other = 4, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_catalan_x2dnormalform_CTree_two__leaves___closed__0_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_two__leaves___closed__0_value)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_four__balanced___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_four__balanced___closed__0_value;
LEAN_EXPORT const lean_object* lp_catalan_x2dnormalform_CTree_four__balanced = (const lean_object*)&lp_catalan_x2dnormalform_CTree_four__balanced___closed__0_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_four__left___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*4 + 0, .m_other = 4, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_catalan_x2dnormalform_CTree_three__left___closed__0_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_catalan_x2dnormalform_CTree_four__left___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_four__left___closed__0_value;
LEAN_EXPORT const lean_object* lp_catalan_x2dnormalform_CTree_four__left = (const lean_object*)&lp_catalan_x2dnormalform_CTree_four__left___closed__0_value;
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height___boxed(lean_object*, lean_object*);
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_left__tree___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_catalan_x2dnormalform_CTree_left__tree___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_left__tree___closed__0_value;
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_left__tree(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_left__tree___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_right__tree(lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_right__tree___boxed(lean_object*);
static const lean_string_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 18, .m_capacity = 18, .m_length = 17, .m_data = "CatalanNormalform"};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__0 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__0_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__0_value),LEAN_SCALAR_PTR_LITERAL(160, 58, 128, 51, 3, 32, 31, 185)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__1 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__1_value;
static const lean_string_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "CTree"};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__2 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__2_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__1_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__2_value),LEAN_SCALAR_PTR_LITERAL(246, 76, 173, 100, 154, 79, 47, 144)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__3 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__3_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__3_value),((lean_object*)(((size_t)(122) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(166, 176, 240, 56, 6, 44, 15, 30)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__4 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__4_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__4_value),((lean_object*)(((size_t)(2) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(231, 163, 156, 217, 177, 25, 66, 219)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__5 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__5_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__5_value),((lean_object*)(((size_t)(122) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(139, 14, 158, 3, 140, 116, 154, 12)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__6 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__6_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__6_value),((lean_object*)(((size_t)(7) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(252, 191, 229, 248, 35, 71, 154, 69)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__7 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__7_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__7_value),((lean_object*)(((size_t)(2) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(165, 61, 193, 215, 225, 64, 244, 41)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__8 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__8_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__8_value),((lean_object*)(((size_t)(7) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(202, 183, 73, 28, 81, 232, 223, 43)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__9 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__9_value;
static const lean_string_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "_sorry"};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__10 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__10_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__9_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__10_value),LEAN_SCALAR_PTR_LITERAL(251, 106, 242, 191, 221, 46, 180, 167)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__11 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__11_value;
static const lean_string_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "_@"};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__12 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__12_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__11_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__12_value),LEAN_SCALAR_PTR_LITERAL(222, 58, 181, 234, 44, 234, 141, 252)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__13 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__13_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__13_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__0_value),LEAN_SCALAR_PTR_LITERAL(41, 89, 72, 58, 39, 203, 230, 95)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__14 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__14_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__14_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__2_value),LEAN_SCALAR_PTR_LITERAL(99, 192, 243, 10, 184, 235, 74, 16)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__15 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__15_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__15_value),((lean_object*)(((size_t)(1506705427) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(130, 223, 152, 161, 37, 113, 58, 75)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__16 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__16_value;
static const lean_string_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "_hygCtx"};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__17 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__17_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__16_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__17_value),LEAN_SCALAR_PTR_LITERAL(45, 7, 193, 102, 93, 163, 14, 23)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__18 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__18_value;
static const lean_string_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "_hyg"};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__19 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__19_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__18_value),((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__19_value),LEAN_SCALAR_PTR_LITERAL(109, 101, 91, 175, 194, 37, 103, 136)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__20 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__20_value;
static const lean_ctor_object lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 2}, .m_objs = {((lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__20_value),((lean_object*)(((size_t)(14) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(12, 108, 165, 221, 239, 194, 11, 152)}};
static const lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__21 = (const lean_object*)&lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__21_value;
LEAN_EXPORT uint8_t lp_catalan_x2dnormalform_CTree_decEqCTree___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_catalan_x2dnormalform_CTree_decEqCTree(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx___redArg(lean_object* v_x_1_){
_start:
{
if (lean_obj_tag(v_x_1_) == 0)
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
else
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(1u);
return v___x_3_;
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx___redArg___boxed(lean_object* v_x_4_){
_start:
{
lean_object* v_res_5_; 
v_res_5_ = lp_catalan_x2dnormalform_CTree_ctorIdx___redArg(v_x_4_);
lean_dec(v_x_4_);
return v_res_5_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx(lean_object* v_a_6_, lean_object* v_x_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_catalan_x2dnormalform_CTree_ctorIdx___redArg(v_x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorIdx___boxed(lean_object* v_a_9_, lean_object* v_x_10_){
_start:
{
lean_object* v_res_11_; 
v_res_11_ = lp_catalan_x2dnormalform_CTree_ctorIdx(v_a_9_, v_x_10_);
lean_dec(v_x_10_);
lean_dec(v_a_9_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorElim___redArg(lean_object* v_t_12_, lean_object* v_k_13_){
_start:
{
if (lean_obj_tag(v_t_12_) == 0)
{
return v_k_13_;
}
else
{
lean_object* v_m_14_; lean_object* v_n_15_; lean_object* v_a_16_; lean_object* v_a_17_; lean_object* v___x_18_; 
v_m_14_ = lean_ctor_get(v_t_12_, 0);
lean_inc(v_m_14_);
v_n_15_ = lean_ctor_get(v_t_12_, 1);
lean_inc(v_n_15_);
v_a_16_ = lean_ctor_get(v_t_12_, 2);
lean_inc(v_a_16_);
v_a_17_ = lean_ctor_get(v_t_12_, 3);
lean_inc(v_a_17_);
lean_dec_ref_known(v_t_12_, 4);
v___x_18_ = lean_apply_4(v_k_13_, v_m_14_, v_n_15_, v_a_16_, v_a_17_);
return v___x_18_;
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorElim(lean_object* v_motive_19_, lean_object* v_ctorIdx_20_, lean_object* v_a_21_, lean_object* v_t_22_, lean_object* v_h_23_, lean_object* v_k_24_){
_start:
{
lean_object* v___x_25_; 
v___x_25_ = lp_catalan_x2dnormalform_CTree_ctorElim___redArg(v_t_22_, v_k_24_);
return v___x_25_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_ctorElim___boxed(lean_object* v_motive_26_, lean_object* v_ctorIdx_27_, lean_object* v_a_28_, lean_object* v_t_29_, lean_object* v_h_30_, lean_object* v_k_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_catalan_x2dnormalform_CTree_ctorElim(v_motive_26_, v_ctorIdx_27_, v_a_28_, v_t_29_, v_h_30_, v_k_31_);
lean_dec(v_a_28_);
lean_dec(v_ctorIdx_27_);
return v_res_32_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_leaf_elim___redArg(lean_object* v_t_33_, lean_object* v_leaf_34_){
_start:
{
lean_object* v___x_35_; 
v___x_35_ = lp_catalan_x2dnormalform_CTree_ctorElim___redArg(v_t_33_, v_leaf_34_);
return v___x_35_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_leaf_elim(lean_object* v_motive_36_, lean_object* v_a_37_, lean_object* v_t_38_, lean_object* v_h_39_, lean_object* v_leaf_40_){
_start:
{
lean_object* v___x_41_; 
v___x_41_ = lp_catalan_x2dnormalform_CTree_ctorElim___redArg(v_t_38_, v_leaf_40_);
return v___x_41_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_leaf_elim___boxed(lean_object* v_motive_42_, lean_object* v_a_43_, lean_object* v_t_44_, lean_object* v_h_45_, lean_object* v_leaf_46_){
_start:
{
lean_object* v_res_47_; 
v_res_47_ = lp_catalan_x2dnormalform_CTree_leaf_elim(v_motive_42_, v_a_43_, v_t_44_, v_h_45_, v_leaf_46_);
lean_dec(v_a_43_);
return v_res_47_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_node_elim___redArg(lean_object* v_t_48_, lean_object* v_node_49_){
_start:
{
lean_object* v___x_50_; 
v___x_50_ = lp_catalan_x2dnormalform_CTree_ctorElim___redArg(v_t_48_, v_node_49_);
return v___x_50_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_node_elim(lean_object* v_motive_51_, lean_object* v_a_52_, lean_object* v_t_53_, lean_object* v_h_54_, lean_object* v_node_55_){
_start:
{
lean_object* v___x_56_; 
v___x_56_ = lp_catalan_x2dnormalform_CTree_ctorElim___redArg(v_t_53_, v_node_55_);
return v___x_56_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_node_elim___boxed(lean_object* v_motive_57_, lean_object* v_a_58_, lean_object* v_t_59_, lean_object* v_h_60_, lean_object* v_node_61_){
_start:
{
lean_object* v_res_62_; 
v_res_62_ = lp_catalan_x2dnormalform_CTree_node_elim(v_motive_57_, v_a_58_, v_t_59_, v_h_60_, v_node_61_);
lean_dec(v_a_58_);
return v_res_62_;
}
}
static lean_object* _init_lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2(void){
_start:
{
lean_object* v___x_66_; lean_object* v___x_67_; 
v___x_66_ = lean_unsigned_to_nat(2u);
v___x_67_ = lean_nat_to_int(v___x_66_);
return v___x_67_;
}
}
static lean_object* _init_lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3(void){
_start:
{
lean_object* v___x_68_; lean_object* v___x_69_; 
v___x_68_ = lean_unsigned_to_nat(1u);
v___x_69_ = lean_nat_to_int(v___x_68_);
return v___x_69_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg(lean_object* v_x_76_, lean_object* v_prec_77_){
_start:
{
lean_object* v___y_79_; 
if (lean_obj_tag(v_x_76_) == 0)
{
lean_object* v___x_85_; uint8_t v___x_86_; 
v___x_85_ = lean_unsigned_to_nat(1024u);
v___x_86_ = lean_nat_dec_le(v___x_85_, v_prec_77_);
if (v___x_86_ == 0)
{
lean_object* v___x_87_; 
v___x_87_ = lean_obj_once(&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2, &lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2_once, _init_lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2);
v___y_79_ = v___x_87_;
goto v___jp_78_;
}
else
{
lean_object* v___x_88_; 
v___x_88_ = lean_obj_once(&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3, &lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3_once, _init_lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3);
v___y_79_ = v___x_88_;
goto v___jp_78_;
}
}
else
{
lean_object* v_a_89_; lean_object* v_a_90_; lean_object* v___x_91_; lean_object* v___y_93_; uint8_t v___x_105_; 
v_a_89_ = lean_ctor_get(v_x_76_, 2);
v_a_90_ = lean_ctor_get(v_x_76_, 3);
v___x_91_ = lean_unsigned_to_nat(1024u);
v___x_105_ = lean_nat_dec_le(v___x_91_, v_prec_77_);
if (v___x_105_ == 0)
{
lean_object* v___x_106_; 
v___x_106_ = lean_obj_once(&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2, &lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2_once, _init_lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__2);
v___y_93_ = v___x_106_;
goto v___jp_92_;
}
else
{
lean_object* v___x_107_; 
v___x_107_ = lean_obj_once(&lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3, &lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3_once, _init_lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__3);
v___y_93_ = v___x_107_;
goto v___jp_92_;
}
v___jp_92_:
{
lean_object* v___x_94_; lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; lean_object* v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_101_; uint8_t v___x_102_; lean_object* v___x_103_; lean_object* v___x_104_; 
v___x_94_ = lean_box(1);
v___x_95_ = ((lean_object*)(lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__6));
v___x_96_ = lp_catalan_x2dnormalform_instReprCTree_repr___redArg(v_a_89_, v___x_91_);
v___x_97_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_97_, 0, v___x_95_);
lean_ctor_set(v___x_97_, 1, v___x_96_);
v___x_98_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_98_, 0, v___x_97_);
lean_ctor_set(v___x_98_, 1, v___x_94_);
v___x_99_ = lp_catalan_x2dnormalform_instReprCTree_repr___redArg(v_a_90_, v___x_91_);
v___x_100_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_100_, 0, v___x_98_);
lean_ctor_set(v___x_100_, 1, v___x_99_);
lean_inc(v___y_93_);
v___x_101_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_101_, 0, v___y_93_);
lean_ctor_set(v___x_101_, 1, v___x_100_);
v___x_102_ = 0;
v___x_103_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_103_, 0, v___x_101_);
lean_ctor_set_uint8(v___x_103_, sizeof(void*)*1, v___x_102_);
v___x_104_ = l_Repr_addAppParen(v___x_103_, v_prec_77_);
return v___x_104_;
}
}
v___jp_78_:
{
lean_object* v___x_80_; lean_object* v___x_81_; uint8_t v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; 
v___x_80_ = ((lean_object*)(lp_catalan_x2dnormalform_instReprCTree_repr___redArg___closed__1));
lean_inc(v___y_79_);
v___x_81_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_81_, 0, v___y_79_);
lean_ctor_set(v___x_81_, 1, v___x_80_);
v___x_82_ = 0;
v___x_83_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_83_, 0, v___x_81_);
lean_ctor_set_uint8(v___x_83_, sizeof(void*)*1, v___x_82_);
v___x_84_ = l_Repr_addAppParen(v___x_83_, v_prec_77_);
return v___x_84_;
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___redArg___boxed(lean_object* v_x_108_, lean_object* v_prec_109_){
_start:
{
lean_object* v_res_110_; 
v_res_110_ = lp_catalan_x2dnormalform_instReprCTree_repr___redArg(v_x_108_, v_prec_109_);
lean_dec(v_prec_109_);
lean_dec(v_x_108_);
return v_res_110_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr(lean_object* v_a_111_, lean_object* v_x_112_, lean_object* v_prec_113_){
_start:
{
lean_object* v___x_114_; 
v___x_114_ = lp_catalan_x2dnormalform_instReprCTree_repr___redArg(v_x_112_, v_prec_113_);
return v___x_114_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree_repr___boxed(lean_object* v_a_115_, lean_object* v_x_116_, lean_object* v_prec_117_){
_start:
{
lean_object* v_res_118_; 
v_res_118_ = lp_catalan_x2dnormalform_instReprCTree_repr(v_a_115_, v_x_116_, v_prec_117_);
lean_dec(v_prec_117_);
lean_dec(v_x_116_);
lean_dec(v_a_115_);
return v_res_118_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_instReprCTree(lean_object* v_a_119_){
_start:
{
lean_object* v___x_120_; 
v___x_120_ = lean_alloc_closure((void*)(lp_catalan_x2dnormalform_instReprCTree_repr___boxed), 3, 1);
lean_closure_set(v___x_120_, 0, v_a_119_);
return v___x_120_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves___redArg(lean_object* v_k_147_){
_start:
{
lean_inc(v_k_147_);
return v_k_147_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves___redArg___boxed(lean_object* v_k_148_){
_start:
{
lean_object* v_res_149_; 
v_res_149_ = lp_catalan_x2dnormalform_CTree_num__leaves___redArg(v_k_148_);
lean_dec(v_k_148_);
return v_res_149_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves(lean_object* v_k_150_, lean_object* v_x_151_){
_start:
{
lean_inc(v_k_150_);
return v_k_150_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__leaves___boxed(lean_object* v_k_152_, lean_object* v_x_153_){
_start:
{
lean_object* v_res_154_; 
v_res_154_ = lp_catalan_x2dnormalform_CTree_num__leaves(v_k_152_, v_x_153_);
lean_dec(v_x_153_);
lean_dec(v_k_152_);
return v_res_154_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg(lean_object* v_x_155_){
_start:
{
if (lean_obj_tag(v_x_155_) == 0)
{
lean_object* v___x_156_; 
v___x_156_ = lean_unsigned_to_nat(0u);
return v___x_156_;
}
else
{
lean_object* v_a_157_; lean_object* v_a_158_; lean_object* v___x_159_; lean_object* v___x_160_; lean_object* v___x_161_; lean_object* v___x_162_; lean_object* v___x_163_; 
v_a_157_ = lean_ctor_get(v_x_155_, 2);
v_a_158_ = lean_ctor_get(v_x_155_, 3);
v___x_159_ = lean_unsigned_to_nat(1u);
v___x_160_ = lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg(v_a_157_);
v___x_161_ = lean_nat_add(v___x_159_, v___x_160_);
lean_dec(v___x_160_);
v___x_162_ = lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg(v_a_158_);
v___x_163_ = lean_nat_add(v___x_161_, v___x_162_);
lean_dec(v___x_162_);
lean_dec(v___x_161_);
return v___x_163_;
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg___boxed(lean_object* v_x_164_){
_start:
{
lean_object* v_res_165_; 
v_res_165_ = lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg(v_x_164_);
lean_dec(v_x_164_);
return v_res_165_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes(lean_object* v_x_166_, lean_object* v_x_167_){
_start:
{
lean_object* v___x_168_; 
v___x_168_ = lp_catalan_x2dnormalform_CTree_num__internal__nodes___redArg(v_x_167_);
return v___x_168_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_num__internal__nodes___boxed(lean_object* v_x_169_, lean_object* v_x_170_){
_start:
{
lean_object* v_res_171_; 
v_res_171_ = lp_catalan_x2dnormalform_CTree_num__internal__nodes(v_x_169_, v_x_170_);
lean_dec(v_x_170_);
lean_dec(v_x_169_);
return v_res_171_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height___redArg(lean_object* v_x_172_){
_start:
{
if (lean_obj_tag(v_x_172_) == 0)
{
lean_object* v___x_173_; 
v___x_173_ = lean_unsigned_to_nat(0u);
return v___x_173_;
}
else
{
lean_object* v_a_174_; lean_object* v_a_175_; lean_object* v___x_176_; lean_object* v___x_177_; lean_object* v___x_178_; uint8_t v___x_179_; 
v_a_174_ = lean_ctor_get(v_x_172_, 2);
v_a_175_ = lean_ctor_get(v_x_172_, 3);
v___x_176_ = lean_unsigned_to_nat(1u);
v___x_177_ = lp_catalan_x2dnormalform_CTree_height___redArg(v_a_174_);
v___x_178_ = lp_catalan_x2dnormalform_CTree_height___redArg(v_a_175_);
v___x_179_ = lean_nat_dec_le(v___x_177_, v___x_178_);
if (v___x_179_ == 0)
{
lean_object* v___x_180_; 
lean_dec(v___x_178_);
v___x_180_ = lean_nat_add(v___x_176_, v___x_177_);
lean_dec(v___x_177_);
return v___x_180_;
}
else
{
lean_object* v___x_181_; 
lean_dec(v___x_177_);
v___x_181_ = lean_nat_add(v___x_176_, v___x_178_);
lean_dec(v___x_178_);
return v___x_181_;
}
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height___redArg___boxed(lean_object* v_x_182_){
_start:
{
lean_object* v_res_183_; 
v_res_183_ = lp_catalan_x2dnormalform_CTree_height___redArg(v_x_182_);
lean_dec(v_x_182_);
return v_res_183_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height(lean_object* v_x_184_, lean_object* v_x_185_){
_start:
{
lean_object* v___x_186_; 
v___x_186_ = lp_catalan_x2dnormalform_CTree_height___redArg(v_x_185_);
return v___x_186_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_height___boxed(lean_object* v_x_187_, lean_object* v_x_188_){
_start:
{
lean_object* v_res_189_; 
v_res_189_ = lp_catalan_x2dnormalform_CTree_height(v_x_187_, v_x_188_);
lean_dec(v_x_188_);
lean_dec(v_x_187_);
return v_res_189_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_left__tree(lean_object* v_x_192_){
_start:
{
lean_object* v_zero_193_; uint8_t v_isZero_194_; 
v_zero_193_ = lean_unsigned_to_nat(0u);
v_isZero_194_ = lean_nat_dec_eq(v_x_192_, v_zero_193_);
if (v_isZero_194_ == 0)
{
lean_object* v_one_195_; lean_object* v_n_196_; uint8_t v_isZero_197_; 
v_one_195_ = lean_unsigned_to_nat(1u);
v_n_196_ = lean_nat_sub(v_x_192_, v_one_195_);
v_isZero_197_ = lean_nat_dec_eq(v_n_196_, v_zero_193_);
if (v_isZero_197_ == 1)
{
lean_object* v___x_198_; 
lean_dec(v_n_196_);
v___x_198_ = ((lean_object*)(lp_catalan_x2dnormalform_CTree_left__tree___closed__0));
return v___x_198_;
}
else
{
lean_object* v_n_199_; lean_object* v___x_200_; lean_object* v___x_201_; 
v_n_199_ = lean_nat_sub(v_n_196_, v_one_195_);
lean_dec(v_n_196_);
v___x_200_ = lean_nat_add(v_n_199_, v_one_195_);
lean_dec(v_n_199_);
v___x_201_ = lp_catalan_x2dnormalform_CTree_left__tree(v___x_200_);
if (lean_obj_tag(v___x_201_) == 0)
{
lean_dec(v___x_200_);
return v___x_201_;
}
else
{
lean_object* v_val_202_; lean_object* v___x_204_; uint8_t v_isShared_205_; uint8_t v_isSharedCheck_211_; 
v_val_202_ = lean_ctor_get(v___x_201_, 0);
v_isSharedCheck_211_ = !lean_is_exclusive(v___x_201_);
if (v_isSharedCheck_211_ == 0)
{
v___x_204_ = v___x_201_;
v_isShared_205_ = v_isSharedCheck_211_;
goto v_resetjp_203_;
}
else
{
lean_inc(v_val_202_);
lean_dec(v___x_201_);
v___x_204_ = lean_box(0);
v_isShared_205_ = v_isSharedCheck_211_;
goto v_resetjp_203_;
}
v_resetjp_203_:
{
lean_object* v___x_206_; lean_object* v___x_207_; lean_object* v___x_209_; 
v___x_206_ = lean_box(0);
v___x_207_ = lean_alloc_ctor(1, 4, 0);
lean_ctor_set(v___x_207_, 0, v___x_200_);
lean_ctor_set(v___x_207_, 1, v_one_195_);
lean_ctor_set(v___x_207_, 2, v_val_202_);
lean_ctor_set(v___x_207_, 3, v___x_206_);
if (v_isShared_205_ == 0)
{
lean_ctor_set(v___x_204_, 0, v___x_207_);
v___x_209_ = v___x_204_;
goto v_reusejp_208_;
}
else
{
lean_object* v_reuseFailAlloc_210_; 
v_reuseFailAlloc_210_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_210_, 0, v___x_207_);
v___x_209_ = v_reuseFailAlloc_210_;
goto v_reusejp_208_;
}
v_reusejp_208_:
{
return v___x_209_;
}
}
}
}
}
else
{
lean_object* v___x_212_; 
v___x_212_ = lean_box(0);
return v___x_212_;
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_left__tree___boxed(lean_object* v_x_213_){
_start:
{
lean_object* v_res_214_; 
v_res_214_ = lp_catalan_x2dnormalform_CTree_left__tree(v_x_213_);
lean_dec(v_x_213_);
return v_res_214_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_right__tree(lean_object* v_x_215_){
_start:
{
lean_object* v_zero_216_; uint8_t v_isZero_217_; 
v_zero_216_ = lean_unsigned_to_nat(0u);
v_isZero_217_ = lean_nat_dec_eq(v_x_215_, v_zero_216_);
if (v_isZero_217_ == 0)
{
lean_object* v_one_218_; lean_object* v_n_219_; uint8_t v_isZero_220_; 
v_one_218_ = lean_unsigned_to_nat(1u);
v_n_219_ = lean_nat_sub(v_x_215_, v_one_218_);
v_isZero_220_ = lean_nat_dec_eq(v_n_219_, v_zero_216_);
if (v_isZero_220_ == 1)
{
lean_object* v___x_221_; 
lean_dec(v_n_219_);
v___x_221_ = ((lean_object*)(lp_catalan_x2dnormalform_CTree_left__tree___closed__0));
return v___x_221_;
}
else
{
lean_object* v_n_222_; lean_object* v___x_223_; lean_object* v___x_224_; 
v_n_222_ = lean_nat_sub(v_n_219_, v_one_218_);
lean_dec(v_n_219_);
v___x_223_ = lean_nat_add(v_n_222_, v_one_218_);
lean_dec(v_n_222_);
v___x_224_ = lp_catalan_x2dnormalform_CTree_right__tree(v___x_223_);
if (lean_obj_tag(v___x_224_) == 0)
{
lean_dec(v___x_223_);
return v___x_224_;
}
else
{
lean_object* v_val_225_; lean_object* v___x_227_; uint8_t v_isShared_228_; uint8_t v_isSharedCheck_234_; 
v_val_225_ = lean_ctor_get(v___x_224_, 0);
v_isSharedCheck_234_ = !lean_is_exclusive(v___x_224_);
if (v_isSharedCheck_234_ == 0)
{
v___x_227_ = v___x_224_;
v_isShared_228_ = v_isSharedCheck_234_;
goto v_resetjp_226_;
}
else
{
lean_inc(v_val_225_);
lean_dec(v___x_224_);
v___x_227_ = lean_box(0);
v_isShared_228_ = v_isSharedCheck_234_;
goto v_resetjp_226_;
}
v_resetjp_226_:
{
lean_object* v___x_229_; lean_object* v___x_230_; lean_object* v___x_232_; 
v___x_229_ = lean_box(0);
v___x_230_ = lean_alloc_ctor(1, 4, 0);
lean_ctor_set(v___x_230_, 0, v_one_218_);
lean_ctor_set(v___x_230_, 1, v___x_223_);
lean_ctor_set(v___x_230_, 2, v___x_229_);
lean_ctor_set(v___x_230_, 3, v_val_225_);
if (v_isShared_228_ == 0)
{
lean_ctor_set(v___x_227_, 0, v___x_230_);
v___x_232_ = v___x_227_;
goto v_reusejp_231_;
}
else
{
lean_object* v_reuseFailAlloc_233_; 
v_reuseFailAlloc_233_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_233_, 0, v___x_230_);
v___x_232_ = v_reuseFailAlloc_233_;
goto v_reusejp_231_;
}
v_reusejp_231_:
{
return v___x_232_;
}
}
}
}
}
else
{
lean_object* v___x_235_; 
v___x_235_ = lean_box(0);
return v___x_235_;
}
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_right__tree___boxed(lean_object* v_x_236_){
_start:
{
lean_object* v_res_237_; 
v_res_237_ = lp_catalan_x2dnormalform_CTree_right__tree(v_x_236_);
lean_dec(v_x_236_);
return v_res_237_;
}
}
LEAN_EXPORT uint8_t lp_catalan_x2dnormalform_CTree_decEqCTree___redArg(lean_object* v_a_292_, lean_object* v_b_293_){
_start:
{
uint8_t v___x_294_; lean_object* v___x_295_; lean_object* v___x_40__overap_296_; lean_object* v___x_297_; uint8_t v___x_298_; 
v___x_294_ = 0;
v___x_295_ = ((lean_object*)(lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___closed__21));
v___x_40__overap_296_ = lean_sorry(v___x_294_);
v___x_297_ = lean_apply_3(v___x_40__overap_296_, v___x_295_, v_a_292_, v_b_293_);
v___x_298_ = lean_unbox(v___x_297_);
return v___x_298_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___redArg___boxed(lean_object* v_a_299_, lean_object* v_b_300_){
_start:
{
uint8_t v_res_301_; lean_object* v_r_302_; 
v_res_301_ = lp_catalan_x2dnormalform_CTree_decEqCTree___redArg(v_a_299_, v_b_300_);
v_r_302_ = lean_box(v_res_301_);
return v_r_302_;
}
}
LEAN_EXPORT uint8_t lp_catalan_x2dnormalform_CTree_decEqCTree(lean_object* v_k_303_, lean_object* v_a_304_, lean_object* v_b_305_){
_start:
{
uint8_t v___x_306_; 
v___x_306_ = lp_catalan_x2dnormalform_CTree_decEqCTree___redArg(v_a_304_, v_b_305_);
return v___x_306_;
}
}
LEAN_EXPORT lean_object* lp_catalan_x2dnormalform_CTree_decEqCTree___boxed(lean_object* v_k_307_, lean_object* v_a_308_, lean_object* v_b_309_){
_start:
{
uint8_t v_res_310_; lean_object* v_r_311_; 
v_res_310_ = lp_catalan_x2dnormalform_CTree_decEqCTree(v_k_307_, v_a_308_, v_b_309_);
lean_dec(v_k_307_);
v_r_311_ = lean_box(v_res_310_);
return v_r_311_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Nat_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_Basic(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_catalan_x2dnormalform_CatalanNormalform_CTree(uint8_t builtin) {
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
res = initialize_mathlib_Mathlib_Tactic_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
