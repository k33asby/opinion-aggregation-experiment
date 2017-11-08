require File.dirname(__FILE__) + '/Modeling'
require 'rbplotly'

PEOPELE_NUM = 199
POSSIBILITY_CORRECT = 0.7
LAMBDA_POISSON = 30
DELIMITER = 100

model = Modeling.new(PEOPELE_NUM, POSSIBILITY_CORRECT, LAMBDA_POISSON)

# 縦軸 => 効用utility, 横軸 => 人の正解する確率p
utility_possibility_x_axis = (DELIMITER / 2..DELIMITER).to_a
# 乱数を用いてるので10回分の平均をとる
temp_utility_possibility_y_axis_by_first_person = []
temp_utility_possibility_y_axis_by_majority_vote = []
temp_utility_possibility_y_axis_by_time_limit = []
10.times do
  temp_utility_possibility_y_axis_by_first_person << utility_possibility_x_axis.map { |e| model.baseline_method_deciding_by_first_person_with_poisson(e.to_f / DELIMITER) }
  temp_utility_possibility_y_axis_by_majority_vote << utility_possibility_x_axis.map { |e| model.baseline_method_deciding_by_majority_vote_with_poisson(e.to_f / DELIMITER, 5) }
  temp_utility_possibility_y_axis_by_time_limit << utility_possibility_x_axis.map { |e| model.baseline_method_deciding_by_time_limit_with_poisson(e.to_f / DELIMITER, 10) }
end
utility_possibility_y_axis_by_first_person = []
utility_possibility_y_axis_by_majority_vote = []
utility_possibility_y_axis_by_time_limit = []
utility_possibility_x_axis.length.times do |x_axis|
  average_y_first_person = 0
  average_y_majority_vote = 0
  average_y_time_limit = 0
  10.times do |t|
    average_y_first_person +=  temp_utility_possibility_y_axis_by_first_person[t][x_axis] / 10
    average_y_majority_vote +=  temp_utility_possibility_y_axis_by_majority_vote[t][x_axis] / 10
    average_y_time_limit +=  temp_utility_possibility_y_axis_by_time_limit[t][x_axis] / 10
  end
  utility_possibility_y_axis_by_first_person << average_y_first_person
  utility_possibility_y_axis_by_majority_vote << average_y_majority_vote
  utility_possibility_y_axis_by_time_limit << average_y_time_limit
end
utility_possibility_by_first_person_trace = [ {x: utility_possibility_x_axis, y: utility_possibility_y_axis_by_first_person}]
utility_possibility_by_majority_vote_trace = [ {x: utility_possibility_x_axis, y: utility_possibility_y_axis_by_majority_vote}]
utility_possibility_by_time_limit_trace = [ {x: utility_possibility_x_axis, y: utility_possibility_y_axis_by_time_limit}]

pl = Plotly::Plot.new(data: utility_possibility_by_first_person_trace + utility_possibility_by_majority_vote_trace + utility_possibility_by_time_limit_trace)
pl.layout.xaxis = { title: 'possibility_correct' }
pl.layout.yaxis = { title: 'utility' }
pl.show

utility_possibility_by_majority_vote_traces_arr = []
10.times do
  utility_possibility_by_majority_vote_traces_arr << { x: utility_possibility_x_axis, y: utility_possibility_x_axis.map { |e| model.baseline_method_deciding_by_majority_vote_with_poisson(e.to_f / DELIMITER) } }
end
pl_by_majority_vote = Plotly::Plot.new(data: utility_possibility_by_majority_vote_traces_arr)
pl_by_majority_vote.layout.xaxis = { title: 'possibility_correct' }
pl_by_majority_vote.layout.yaxis = { title: 'utility' }
pl_by_majority_vote.show


# 縦軸 => 誤差率ε, 横軸 => 人の正解する確率p
error_possibility_x_axis = (DELIMITER / 2..DELIMITER).to_a
y_axis1 = error_possibility_x_axis.map { |e| model.baseline_method1(e.to_f / DELIMITER) }
error_possibility_trace1 = { x: error_possibility_x_axis, y: y_axis1 }
y_axis2 = error_possibility_x_axis.map { |e| model.baseline_method2(e.to_f / DELIMITER) }
error_possibility_trace2 = { x: error_possibility_x_axis, y: y_axis2 }
error_possibility_traces = [error_possibility_trace1, error_possibility_trace2]

# 縦軸 => 必要な人数X(コスト), 横軸 => 誤差率ε
cost_error_x_axis = (1..DELIMITER).to_a
y_axis3 = cost_error_x_axis.map { |e| model.baseline_method3(e.to_f / DELIMITER) }
cost_error_trace1 = { x: cost_error_x_axis, y: y_axis3 }
y_axis4 = cost_error_x_axis.map { |e| model.baseline_method4(e.to_f / DELIMITER) }
cost_error_trace2 = { x: cost_error_x_axis, y: y_axis4 }
cost_error_traces = [cost_error_trace1, cost_error_trace2]

# 縦軸 => 誤差率ε, 横軸 => 人の正解する確率p, people_numを変動させたグラフを重ねる
error_possibility_model_arr = []
30.times do |t|
  error_possibility_model_arr << Modeling.new(1 + 5 * t, POSSIBILITY_CORRECT)
end
error_possibility_traces_arr = []
error_possibility_model_arr.each do |elem|
  error_possibility_traces_arr << { x: error_possibility_x_axis, y: error_possibility_x_axis.map { |e| elem.baseline_method1(e.to_f / DELIMITER) } }
end

# 縦軸 => 必要な人数X(コスト), 横軸 => 誤差率ε, possibility_correctを変動させたグラフを重ねる
cost_error_model_arr = []
9.times do |t|
  cost_error_model_arr << Modeling.new(PEOPELE_NUM, (55 + (5.to_f * t)) / 100)
end
cost_error_traces_arr = []
cost_error_model_arr.each do |elem|
  cost_error_traces_arr << { x: cost_error_x_axis, y: cost_error_x_axis.map { |e| elem.baseline_method3(e.to_f / DELIMITER) } }
end

# プロットする
pl1 = Plotly::Plot.new(data: error_possibility_traces)
pl1.layout.title = "PEOPELE_NUM = #{PEOPELE_NUM}"
pl1.layout.xaxis = { title: 'possibility_correct (%)' }
pl1.layout.yaxis = { title: 'relative_error (%)' }
pl1.show

pl2 = Plotly::Plot.new(data: cost_error_traces)
pl2.layout.title = "POSSIBILITY_CORRECT = #{POSSIBILITY_CORRECT} %"
pl2.layout.xaxis = { title: 'relative_error (%)' }
pl2.layout.yaxis = { title: 'people' }
pl2.show

pl3 = Plotly::Plot.new(data: error_possibility_traces_arr)
pl3.layout.xaxis = { title: 'possibility_correct (%)' }
pl3.layout.yaxis = { title: 'relative_error (%)' }
pl3.show

pl4 = Plotly::Plot.new(data: cost_error_traces_arr)
pl4.layout.xaxis = { title: 'relative_error (%)' }
pl4.layout.yaxis = { title: 'people' }
pl4.show
