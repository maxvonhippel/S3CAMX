; benchmark generated from python API
(set-info :status unknown)
;(declare-fun rv_int_state_arr__3 () Real)
;(declare-fun rv_output_arr__0 () Real)
;(declare-fun iv_int_state_arr__2 () Real)
;(declare-fun rv_int_state_arr__2 () Real)
;(declare-fun rv_int_state_arr__1 () Real)
;(declare-fun rv_int_state_arr__0 () Real)
;(declare-fun iv_int_state_arr__1 () Real)
;(declare-fun iv_int_state_arr__3 () Real)
;(declare-fun iv_x_arr__0 () Real)
(assert
(let (($x49 (= rv_int_state_arr__3 0.0)))
(let (($x62 (= rv_output_arr__0 2.0)))
(let (($x47 (= rv_int_state_arr__2 (+ iv_int_state_arr__2 1.0))))
(let (($x61 (= rv_int_state_arr__1 2.0)))
(let (($x28 (= rv_int_state_arr__0 1.0)))
(let (($x60 (and (distinct iv_int_state_arr__1 2.0) true)))
(let (($x56 (>= iv_int_state_arr__3 5.0)))
(let (($x59 (< iv_x_arr__0 70.0)))
(let (($x19 (>= iv_x_arr__0 66.0)))
(and $x19 $x59 $x56 $x60 $x28 $x61 $x47 $x62 $x49)))))))))))
;(check-sat)
