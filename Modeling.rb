require 'poisson'

class Modeling
  def initialize(people_num, possibility_correct)
    @people_num = people_num
    @people_half = half_num(@people_num) # 終了の値や半分の値に用いる
    @possibility_correct = possibility_correct
  end

  # ポアソン分布のテスト
  def test_random
    poisson = Poisson.new(50) # 平均50のポアソン分布
    sum = 0
    40.times do |t|
      sum += poisson.probability{ |x| x == t + 30 }
    end
    p sum
  end

  # 一人目の意見を採用するという雑魚アルゴリズム
  # TODO 時刻0から99で行なっているが1から100の方が好ましい気がする
  def baseline_method_deciding_by_first_person_with_poisson(possibility_correct)
    collecting_deadline = 60 # 意見収集の締め切り 59時刻
    poisson = Poisson.new(30) # 平均30人のポアソン分布
    average_method_utility = 0
    # 0~59人来るときのみを考慮する(それ以外は0に近似する)
    60.times do |t_people|
      # t_people人来るとき
      when_people_come = Array.new(collecting_deadline) # 人がいつ来るか配列で表す
      temp_probability_by_poisson = poisson.probability{ |x| x == t_people }
      t_people.times do |t|
        when_people_come[t] = 1
      end
      method_utility = 0 # 効用 = 精度(正解率) - かかる時間(決定する時刻 / collecting_deadline)
      when_people_come.shuffle.each_with_index do |elem, index|
        next if elem.nil? # 人が来ないときは飛ばす
        weight = 0.5.to_f / collecting_deadline # 時間がかかることに対する重み
        method_utility += possibility_correct - index.to_f * weight
        break
      end
      average_method_utility += temp_probability_by_poisson * method_utility
    end
    average_method_utility
  end

  # 5人で多数決して意見集約を行うというアルゴリズム
  def baseline_method_deciding_by_majority_vote_with_poisson(possibility_correct)
    collecting_deadline = 60 # 意見収集の締め切り 59時刻
    poisson = Poisson.new(30) # 平均30人のポアソン分布
    average_method_utility = 0
    # 0~59人来るときのみを考慮する(それ以外は0に近似する)
    60.times do |t_people|
      # t_people人来るとき
      when_people_come = Array.new(collecting_deadline) # 人がいつ来るか配列で表す
      temp_probability_by_poisson = poisson.probability{ |x| x == t_people }
      t_people.times do |t|
        when_people_come[t] = 1
      end
      method_utility = 0 # 効用 = 精度(正解率) - かかる時間(決定する時刻 / collecting_deadline)
      people_count = 0 # 何人目か
      next if t_people < 5 # 5人集まらない場合は、utility = 0
      when_people_come.shuffle.each_with_index do |elem, index|
        next if elem.nil? # 人が来ない時刻は飛ばす
        people_count += 1
        if people_count == 5
          weight = 0.5.to_f / collecting_deadline
          method_utility +=  (1 - relative_error_by_majority_vote(people_count, possibility_correct)) - index.to_f * weight
          break
        end
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
    relative_error
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
