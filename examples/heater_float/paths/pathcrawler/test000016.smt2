; benchmark generated from python API
(set-info :status unknown)
(declare-fun iv_int_state_arr__3 () Int)
(declare-fun rv_int_state_arr__3 () Int)
(declare-fun rv_output_arr__0 () Real)
(declare-fun rv_int_state_arr__2 () Int)
(declare-fun rv_int_state_arr__1 () Int)
(declare-fun rv_int_state_arr__0 () Int)
(declare-fun iv_int_state_arr__1 () Int)
(declare-fun iv_int_state_arr__2 () Int)
(declare-fun iv_x_arr__0 () Real)
(assert
(let (($x57 (= rv_int_state_arr__3 (+ iv_int_state_arr__3 1))))
(let (($x55 (= rv_output_arr__0 0.0)))
(let (($x53 (= rv_int_state_arr__2 0)))
(let (($x52 (= rv_int_state_arr__1 0)))
(let (($x36 (= rv_int_state_arr__0 0)))
(let (($x51 (= iv_int_state_arr__1 0)))
(let (($x64 (>= iv_int_state_arr__2 5)))
(let (($x38 (< iv_int_state_arr__3 5)))
(let (($x68 (>= iv_x_arr__0 70.0)))
(let (($x67 (>= iv_x_arr__0 66.0)))
(and $x67 $x68 $x38 $x64 $x51 $x36 $x52 $x53 $x55 $x57))))))))))))
(check-sat)
