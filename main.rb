require File.dirname(__FILE__) + '/Modeling'
require 'rbplotly'

PEOPELE_NUM = 200
POSSIBILITY_CORRECT = 0.6
DELIMITER = 100

model = Modeling.new(PEOPELE_NUM, POSSIBILITY_CORRECT)

# 結果をコンソールに表示
# DELIMITER.times do |t|
#   puts model.baseline_method(t.to_f / DELIMITER)
# end


# 縦軸 => 誤差率ε, 横軸 => 人の正解する確率p
x_axis1 = (DELIMITER/2..DELIMITER).to_a
y_axis1 = x_axis1.map{ |e| model.baseline_method1(e.to_f / DELIMITER) }
error_possibility_trace = [{x: x_axis1, y: y_axis1}]

# 縦軸 => 必要な人数X(コスト), 横軸 => 誤差率ε
x_axis2 = (1..DELIMITER).to_a
y_axis2 = x_axis2.map{ |e| model.baseline_method2(e.to_f / DELIMITER) }
cost_error_trace = [{x: x_axis2, y: y_axis2}]

# プロットする
pl1 = Plotly::Plot.new(data: error_possibility_trace)
pl1.layout.title = "PEOPELE_NUM = #{PEOPELE_NUM}"
pl1.layout.xaxis = {title: 'possibility_correct (%)'}
pl1.layout.yaxis = {title: 'relative_error (%)'}
pl1.show
pl2 = Plotly::Plot.new(data: cost_error_trace)
pl2.layout.title = "POSSIBILITY_CORRECT = #{POSSIBILITY_CORRECT} %"
pl2.layout.xaxis = {title: 'relative_error (%)'}
pl2.layout.yaxis = {title: 'people'}
pl2.show
