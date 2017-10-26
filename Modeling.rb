class Modeling
  def initialize(people_num, possibility_correct)
    @people_num = people_num
    @people_half = half_num(@people_num) # 終了の値や半分の値に用いる
    @possibility_correct = possibility_correct
  end

  # 半分の値を求める
  def half_num(num)
    (num.to_f / 2).ceil
  end

  # 誤差率をもとめる.先に半分の意見(finish_num)を集めた方を意見集約の結果とするアルゴリズム
  def relative_error_by_half_opinion(finish_num, possibility_correct) # possibility_correct => 人が正解する確率p
    relative_error = 0
    finish_num.times do |t|
      relative_error += ((1 - possibility_correct)**finish_num) * (possibility_correct**t) * combi(finish_num - 1 + t, t)
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
    relative_error_by_half_opinion(finish_num, possibility_correct)
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
    # 徐々に人数を増やしていき、誤差率を満たす結果の場合ループを終了する
    loop do
      expected_error = relative_error_by_half_opinion(temp_finish_num, @possibility_correct)
      break if expected_error <= relative_error
      people_num += 2
      temp_finish_num = half_num(people_num)
    end
    # 必要な人数を返す
    people_num
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

  # コンビネーションの計算
  def combi(n, k)
    k = n - k if 2 * k > n
    return 1 if k == 0
    ((n - k + 1)..n).reduce(&:*) / (1..k).reduce(&:*)
  end
end
