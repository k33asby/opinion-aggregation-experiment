class Modeling
  def initialize(people_num, possibility_correct)
    @people_num = people_num
    @possibility_correct = possibility_correct
  end

  # 正解の確率pを変動させて、誤差率εの求める
  # @people_numは意見を集める人数であり、コストを表す
  # 先に(@people_num / 2)の意見を集めた方を意見集約の結果とするアルゴリズム
  # 引数は人が正解する確率p
  def baseline_method1(possibility_correct)
    # 終了する値を求める
    finish_num = (@people_num.to_f / 2).ceil
    # 誤差率を求める
    relative_error = 0
    finish_num.times do |t|
      relative_error += ((1 - possibility_correct)**finish_num) * (possibility_correct**t) * combi(finish_num - 1 + t, t)
    end
    # 誤差率を返す
    relative_error
  end

  # 誤差率εを変動させて、必要な人数Xを求める
  # 多数決を意見集約のアルゴリズムとする
  def baseline_method2(relative_error)
    # 必要な人数を求める 1,3,5,,,,と増やす
    people_num = 1
    # 半数の人数を求める
    half_num = (people_num.to_f / 2).ceil
    # 徐々に人数を増やしていき、誤差率を満たす結果の場合ループを終了する
    loop do
      expected_error = 0
      half_num.times do |t|
        expected_error += (@possibility_correct**t) * ((1 - @possibility_correct)**(people_num - t)) * combi(people_num, t)
      end
      break if expected_error <= relative_error
      people_num += 2
      half_num = (people_num.to_f / 2).ceil
    end
    # 必要な人数を返す
    people_num
  end

  def combi(n, k)
    k = n - k if 2 * k > n
    return 1 if k == 0
    ((n - k + 1)..n).reduce(&:*) / (1..k).reduce(&:*)
  end
end
