; benchmark generated from python API
(set-info :status unknown)
;(declare-fun iv_int_state_arr__3 () Real)
;(declare-fun rv_int_state_arr__3 () Real)
;(declare-fun rv_output_arr__0 () Real)
;(declare-fun rv_int_state_arr__2 () Real)
;(declare-fun rv_int_state_arr__1 () Real)
;(declare-fun rv_int_state_arr__0 () Real)
;(declare-fun iv_int_state_arr__1 () Real)
;(declare-fun iv_x_arr__0 () Real)
(assert
(let (($x33 (= rv_int_state_arr__3 (+ iv_int_state_arr__3 1.0))))
(let (($x31 (= rv_output_arr__0 0.0)))
(let (($x30 (= rv_int_state_arr__2 0.0)))
(let (($x29 (= rv_int_state_arr__1 0.0)))
(let (($x28 (= rv_int_state_arr__0 1.0)))
(let (($x26 (and (distinct iv_int_state_arr__1 0.0) true)))
(let (($x56 (>= iv_int_state_arr__3 5.0)))
(let (($x21 (>= iv_x_arr__0 70.0)))
(let (($x19 (>= iv_x_arr__0 66.0)))
(and $x19 $x21 $x56 $x26 $x28 $x29 $x30 $x31 $x33)))))))))))
;(check-sat)
