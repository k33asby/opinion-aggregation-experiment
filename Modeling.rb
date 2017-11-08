require 'poisson'

class Modeling
  def initialize(people_num, possibility_correct, lambda_poisson)
    @people_num = people_num
    @people_half = half_num(@people_num) # 終了の値や半分の値に用いる
    @possibility_correct = possibility_correct
    @lambda_poisson = lambda_poisson # ポアソン分布の平均lambda
    @collecting_deadline = lambda_poisson * 2 # 意見収集の締め切り時刻を平均の二倍とする
    @poisson = Poisson.new(@lambda_poisson) # ポアソン分布を扱うクラスのインスタンス
  end

  WEIGHT = 0.5.to_f

  # 人がいつ来るか配列で表す EXAMPLE [1, 0, 1] => 時刻0と時刻2に人がくる
  def simulate_when_people_come(people_num)
    when_people_come = Array.new(@collecting_deadline)
    people_num.times do |t|
      when_people_come[t] = 1
    end
    when_people_come.shuffle
  end


  # 一人目の意見を採用するというアルゴリズム
  def baseline_method_deciding_by_first_person_with_poisson(possibility_correct)
    average_method_utility = 0
    # 0~@collecting_deadline人来るときのみを考慮する(平均の二倍以上の人が集まる確率は限りなく0なので0に近似)
    @collecting_deadline.times do |t_people|
      # t_people人来るとき
      when_people_come = simulate_when_people_come(t_people)
      temp_probability_by_poisson = @poisson.probability{ |x| x == t_people }
      method_utility = 0 # 効用 = 精度(正解率) - 重み * かかる時間(決定する時刻 / collecting_deadline)
      when_people_come.shuffle.each_with_index do |elem, index|
        next if elem.nil? # 人が来ないときは飛ばす
        method_utility += possibility_correct - WEIGHT * (index.to_f / @collecting_deadline)
        break # 一人目の意見しか必要ないのですぐBREAK
      end
      average_method_utility += temp_probability_by_poisson * method_utility
    end
    average_method_utility
  end

  # 引数majority_vote_people人で多数決して意見集約を行うというアルゴリズム
  def baseline_method_deciding_by_majority_vote_with_poisson(possibility_correct, majority_vote_people)
    average_method_utility = 0
    # 0~@collecting_deadline人来るときのみを考慮する(平均の二倍以上の人が集まる確率は限りなく0なので0に近似)
    @collecting_deadline.times do |t_people|
      # t_people人来るとき
      when_people_come = simulate_when_people_come(t_people)
      temp_probability_by_poisson = @poisson.probability{ |x| x == t_people }
      method_utility = 0 # 効用 = 精度(正解率) - 重み* かかる時間(決定する時刻 / collecting_deadline)
      people_count = 0 # 何人目か
      next if t_people < majority_vote_people # majority_vote_people人集まらない場合は、utility = 0
      when_people_come.shuffle.each_with_index do |elem, index|
        next if elem.nil? # 人が来ない時刻は飛ばす
        people_count += 1
        if people_count == majority_vote_people
          method_utility +=  (1 - relative_error_by_majority_vote(people_count, possibility_correct)) - WEIGHT * (index.to_f / @collecting_deadline)
          break
        end
      end
      average_method_utility += temp_probability_by_poisson * method_utility
    end
    average_method_utility
  end

  # 先にhalf_num(引数temp_people_num)人集まった方の意見を採用するアルゴリズム
  def baseline_method_deciding_by_half_opinion_with_poisson(possibility_correct, temp_people_num)
    average_method_utility = 0
    # 0~@collecting_deadline人来るときのみを考慮する(平均の二倍以上の人が集まる確率は限りなく0なので0に近似)
    @collecting_deadline.times do |t_people|
      # t_people人来るとき
      when_people_come = simulate_when_people_come(t_people)
      temp_probability_by_poisson = @poisson.probability{ |x| x == t_people }
      method_utility = 0 # 効用 = 精度(正解率) - 重み * かかる時間(決定する時刻 / collecting_deadline)
      people_count = 0 # 何人目か
      people_count_arr = [] # EXAMPLE [4, 9, 20, 40, 45] 一人目は時刻4にきた　二人目は時刻9にきた...
      next if t_people < temp_people_num # temp_people_num人集まらない場合は、utility = 0 TODO temp_people_num人あつまらなくてもその半数は集まることはあるので厳密ではない
      when_people_come.each_with_index do |elem, index|
        next if elem.nil? # 人が来ない時刻は飛ばす
        people_count_arr << index
        people_count += 1
        if people_count == temp_people_num
          relative_error_array = relative_error_array_by_half_opinion(half_num(people_count), possibility_correct)
          expected_error = relative_error_array.inject(:+)
          average_index = 0
          relative_error_array.each_with_index do |e, i| # もっと簡単にかけそう
            average_index += people_count_arr[i + 2] * (e / expected_error)
          end
          method_utility =  (1 - expected_error) - WEIGHT * (average_index.to_f / @collecting_deadline)
          break
        end
      end
      average_method_utility += temp_probability_by_poisson * method_utility
    end
    average_method_utility
  end

  # 誰か一人集まりかつ、時刻引数time_limitで意見収集を打ち切り,多数決で意思決定を行う
  def baseline_method_deciding_by_time_limit_with_poisson(possibility_correct, time_limit)
    average_method_utility = 0
    # 0~@collecting_deadline人来るときのみを考慮する(平均の二倍以上の人が集まる確率は限りなく0なので0に近似)
    @collecting_deadline.times do |t_people|
      # t_people人来るとき
      when_people_come = simulate_when_people_come(t_people)  # 人がいつ来るか配列で表す EXAMPLE [1, 0, 1] => 時刻0と時刻2に人がくる
      temp_probability_by_poisson = @poisson.probability{ |x| x == t_people }
      method_utility = 0 # 効用 = 精度(正解率) - かかる時間(決定する時刻 / collecting_deadline)
      people_count = 0 # 何人目か
      when_people_come.each_with_index do |elem, index|
        if index >= time_limit && people_count >= 1
          method_utility = (1 - relative_error_by_majority_vote(people_count, possibility_correct)) - WEIGHT * (index.to_f / @collecting_deadline)
          break
        end
        next if elem.nil? # 人が来ない時刻は飛ばす
        people_count += 1
      end
      average_method_utility += temp_probability_by_poisson * method_utility
    end
    average_method_utility
  end

  def half_num(num)
    (num.to_f / 2).ceil
  end

  # nCk 実行例 5C2 = 5 * 4 / 2! = 10
  def combi(n, k)
    k = n - k if 2 * k > n
    return 1 if k == 0
    ((n - k + 1)..n).reduce(&:*) / (1..k).reduce(&:*)
  end

  # 誤差率をもとめる.先にある割合の意見(finish_num)を集めた方を意見集約の結果とするアルゴリズム
  # このアルゴリズムは必要な人数が動的に変化するので、誤差率をfinish_num個の要素にした配列で返す
  def relative_error_array_by_half_opinion(finish_num, possibility_correct) # possibility_correct => 人が正解する確率p
    relative_error = []
    finish_num.times do |t|
      relative_error << ((1 - possibility_correct)**finish_num) * (possibility_correct**t) * combi(finish_num - 1 + t, t)
    end
    relative_error # EXAMPLE (finish_num = 3 )[0.2, 0.3, 0.5] 0.2は3:0で決まるとき 0.3は3:1で決まるとき 0.5は3:2で決まるとき
  end

  # 誤差率をもとめる.people_num人で多数決を行い意見集約の結果とするアルゴリズム
  def relative_error_by_majority_vote(people_num, possibility_correct) # possibility_correct => 人が正解する確率p
    half_num = half_num(people_num)
    relative_error = 0
    half_num.times do |t|
      relative_error += (possibility_correct**t) * ((1 - possibility_correct)**(people_num - t)) * combi(people_num, t)
    end
    relative_error
  end

  # 確率pを変動させて、誤差率εの求める
  def baseline_method1(possibility_correct) # possibility_correct => 人が正解する確率p
    # 終了する人数を求める
    finish_num = @people_half
    # 誤差率を求め、返す
    relative_error_array_by_half_opinion(finish_num, possibility_correct).inject(:+)
  end

  # 確率pを変動させて、誤差率εの求める
  def baseline_method2(possibility_correct)
    # 多数決を行い誤差率を求め、返す
    relative_error_by_majority_vote(@people_num, possibility_correct)
  end

  # 誤差率εを変動させて、必要な人数Xを求める
  def baseline_method3(relative_error)
    # 必要な人数を求める 1,3,5,,,,と増やす
    people_num = 1
    # 終了する人数を求める
    temp_finish_num = half_num(people_num)
    # 必要な平均人数
    average_num = 0
    # 徐々に人数を増やしていき、誤差率を満たす結果の場合ループを終了する
    loop do
      relative_error_array = relative_error_array_by_half_opinion(temp_finish_num, @possibility_correct)
      expected_error = relative_error_array.inject(:+)
      average_num = 0
      relative_error_array.each_with_index do |e, i| # もっと簡単にかけそう
        average_num += e * (i + temp_finish_num) / expected_error
      end
      break if expected_error <= relative_error
      people_num += 2
      temp_finish_num = half_num(people_num)
    end
    # 必要な人数の平均を返す
    average_num
  end

  # 多数決を意見集約のアルゴリズムとする
  def baseline_method4(relative_error)
    # 必要な人数を求める 1,3,5,,,,と増やす
    people_num = 1
    # 徐々に人数を増やしていき、誤差率を満たす結果の場合ループを終了する
    loop do
      expected_error = relative_error_by_majority_vote(people_num, @possibility_correct)
      break if expected_error <= relative_error
      people_num += 2
    end
    # 必要な人数を返す
    people_num
  end
end
