require File.dirname(__FILE__) + '/Modeling'
require 'rbplotly'

PEOPELE_NUM = 199
POSSIBILITY_CORRECT = 0.7
DELIMITER = 100

model = Modeling.new(PEOPELE_NUM, POSSIBILITY_CORRECT)

# 縦軸 => 誤差率ε, 横軸 => 人の正解する確率p
error_possibility_x_axis = (DELIMITER/2..DELIMITER).to_a
y_axis1 = error_possibility_x_axis.map{ |e| model.baseline_method1(e.to_f / DELIMITER) }
error_possibility_trace1 = {x: error_possibility_x_axis, y: y_axis1}
y_axis2 = error_possibility_x_axis.map{ |e| model.baseline_method2(e.to_f / DELIMITER) }
error_possibility_trace2 = {x: error_possibility_x_axis, y: y_axis2}
error_possibility_traces = [error_possibility_trace1, error_possibility_trace2]

# 縦軸 => 必要な人数X(コスト), 横軸 => 誤差率ε
cost_error_x_axis = (1..DELIMITER).to_a
y_axis3 = cost_error_x_axis.map{ |e| model.baseline_method3(e.to_f / DELIMITER) }
cost_error_trace1 = {x: cost_error_x_axis, y: y_axis3}
y_axis4 = cost_error_x_axis.map{ |e| model.baseline_method4(e.to_f / DELIMITER) }
cost_error_trace2 = {x: cost_error_x_axis, y: y_axis4}
cost_error_traces = [cost_error_trace1, cost_error_trace2]

# 縦軸 => 誤差率ε, 横軸 => 人の正解する確率p, people_numを変動させたグラフを重ねる
error_possibility_model_arr = []
30.times do |t|
  error_possibility_model_arr << Modeling.new(1 + 5 * t, POSSIBILITY_CORRECT)
end
error_possibility_traces_arr = []
error_possibility_model_arr.each do |elem|
  error_possibility_traces_arr << {x: error_possibility_x_axis, y: error_possibility_x_axis.map{ |e| elem.baseline_method1(e.to_f / DELIMITER)}}
end

# 縦軸 => 必要な人数X(コスト), 横軸 => 誤差率ε, possibility_correctを変動させたグラフを重ねる
cost_error_model_arr = []
9.times do |t|
  cost_error_model_arr << Modeling.new(PEOPELE_NUM, (55 + (5.to_f * t)) / 100)
end
cost_error_traces_arr = []
cost_error_model_arr.each do |elem|
  cost_error_traces_arr << {x: cost_error_x_axis, y: cost_error_x_axis.map{ |e| elem.baseline_method3(e.to_f / DELIMITER)}}
end

# プロットする
pl1 = Plotly::Plot.new(data: error_possibility_traces)
pl1.layout.title = "PEOPELE_NUM = #{PEOPELE_NUM}"
pl1.layout.xaxis = {title: 'possibility_correct (%)'}
pl1.layout.yaxis = {title: 'relative_error (%)'}
pl1.show

pl2 = Plotly::Plot.new(data: cost_error_traces)
pl2.layout.title = "POSSIBILITY_CORRECT = #{POSSIBILITY_CORRECT} %"
pl2.layout.xaxis = {title: 'relative_error (%)'}
pl2.layout.yaxis = {title: 'people'}
pl2.show

pl3 = Plotly::Plot.new(data: error_possibility_traces_arr)
pl3.layout.xaxis = {title: 'possibility_correct (%)'}
pl3.layout.yaxis = {title: 'relative_error (%)'}
pl3.show

pl4 = Plotly::Plot.new(data: cost_error_traces_arr)
pl4.layout.xaxis = {title: 'relative_error (%)'}
pl4.layout.yaxis = {title: 'people'}
pl4.show
