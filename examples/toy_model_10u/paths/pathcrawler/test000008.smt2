; benchmark generated from python API
(set-info :status unknown)
;(declare-fun iv_x_arr__2 () Real)
;(declare-fun rv_output_arr__0 () Real)
;(declare-fun iv_input_arr__1 () Real)
;(declare-fun iv_input_arr__0 () Real)
(assert
(let (($x22 (= rv_output_arr__0 iv_x_arr__2)))
(let (($x24 (>= iv_input_arr__0 90.0)))
(and $x24 (> iv_input_arr__1 10.0) $x22))))
;(check-sat)