# ポアソン分布を計算する
# 返り値は単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻tまでにn回起こる確率
@lru_cache(maxsize=None)
def poisson_probability(n, t, lambda_poisson):
    return math.e**(-lambda_poisson * t) * (lambda_poisson * t)**n / math.factorial(n)

# 累積ポアソン分布を計算する
# nは離散であるので積分は用いずΣを用いて計算する
# 返り値は単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻tまでに0,1,2,3,4...n回起こる確率
@lru_cache(maxsize=None)
def cumulative_poisson_probability(n, t, lambda_poisson):
    cumulative_probability = 0
    for i in range(0, n + 1):
        cumulative_probability += math.e**(-1 * lambda_poisson * t) * (lambda_poisson * t)**i / math.factorial(i)
    return cumulative_probability

# ガンマ分布を計算する
# 返り値は単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻tにn回目が起こる確率
@lru_cache(maxsize=None)
def gamma_probability(n, t, lambda_poisson):
    return lambda_poisson**n * t**(n - 1) * math.e**(-lambda_poisson * t) / math.factorial(n - 1)

# 累積ガンマ分布を計算する
# 時間tは連続であるので積分を用いて計算する
# 返り値は単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻0~tにn回目が起こる確率
@lru_cache(maxsize=None)
def cumulative_gamma_probability(n, T, lambda_poisson):
    cumulative_probability, abserr = integrate.quad(lambda t: gamma_probability(n, t, lambda_poisson), 0, T)
    return cumulative_probability

# 確率gを計算する
# 返り値は確率gとは時刻Tまでにn人現われるときに、時刻t(≤T)にm(≤n)人目が到着する確率
@lru_cache(maxsize=None)
def g(m, n, t, T, lambda_poisson):
    return lambda_poisson**n * t**(m - 1) * (T - t)**(n - m) * math.e**(-lambda_poisson * T) / (math.factorial(m - 1) * math.factorial(n - m))

# 奇数人nで多数決を行う時の解答の精度を計算する(pは個人の判定精度)
@lru_cache(maxsize=None)
def acc_odd(n, p):
    i = int((n + 1) / 2)
    acc = 0
    for j in range(i):
        acc += scm.comb(2 * i - 1, j) * p**(2 * i - 1 - j) * (1 - p)**j
    return acc

# 偶数人nで多数決を行う時の解答の精度を計算する(pは個人の判定精度)
# ちょうど半々になった場合にはその確率の半分を判定精度に含める
@lru_cache(maxsize=None)
def acc_even(n, p):
    i = int(n / 2)
    acc = 0
    for j in range(i):
        acc += scm.comb(2 * i, j) * p**(2 * i - j) * (1 - p)**j
    acc += scm.comb(2 * i, i) * p**i * (1 - p)**i / 2
    return acc

# 奇数の場合と偶数の場合を分けたもの
@lru_cache(maxsize=None)
def acc(n, p):
    if n % 2 == 1:
        return acc_odd(n, p)
    else:
        return acc_even(n, p)

# 時刻tまで待って多数決を行う時刻優先意見集約法
# 返り値は効用(精度 - 重みw * 時間による損失)
@lru_cache(maxsize=None)
def time_priority_method(t, w, p, lambda_poisson):
    if t == 0: return 0
    # 本当はiを0から無限大まで回したいが不可能なので1.8*t*lambda_poisson回ループする
    return np.sum(poisson_probability(i, t, lambda_poisson) * acc(i, p) for i in range(0, int(1.8 * t * lambda_poisson))) - w * t

# 時刻tまで待って多数決を行う時刻優先意見集約法の効用の最大値を求める
@lru_cache(maxsize=None)
def max_time_priority(w, p, lambda_poisson):
    value_down = time_priority_method(1, w, p, lambda_poisson)
    for t in range(2, 100000):
            value_up = time_priority_method(t, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return value_down
            value_down = value_up

# pやlambdaに誤差がある場合、時刻tまで待って多数決を行う時刻優先意見集約法の効用の最大値を求める
@lru_cache(maxsize=None)
def max_time_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = time_priority_method(1, w, p, lambda_poisson)
    for t in range(2, 100000):
            value_up = time_priority_method(t, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return time_priority_method(t - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

# n人集まるまで待って多数決を行う投票数優先意見集約法
# 返り値は効用(精度 - 重みw * 時間による損失)
@lru_cache(maxsize=None)
def poll_priority_method(n, w, p, lambda_poisson):
    if n == 0: return 0
    return acc(n, p) - w * n / lambda_poisson

# n人集まるまで待って多数決を行う投票数優先意見集約法の最大値を求める
@lru_cache(maxsize=None)
def max_poll_priority(w, p, lambda_poisson):
    value_down = poll_priority_method(1, w, p, lambda_poisson)
    for n in range(1, 100000):
            value_up = poll_priority_method(2 *n + 1, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return value_down
            value_down = value_up

# pやlambdaに誤差がある場合、n人集まるまで待って多数決を行う投票数優先意見集約法の最大値を求める
@lru_cache(maxsize=None)
def max_poll_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = poll_priority_method(1, w, p, lambda_poisson)
    for n in range(1, 100000):
            value_up = poll_priority_method(2 * n + 1, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return poll_priority_method(2 * n - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

# 先にk票集まった方に決定する得票数優先意見集約法
# 返り値は効用(精度 - 重みw * 時間による損失)
@lru_cache(maxsize=None)
def vote_priority_method(k, w, p, lambda_poisson):
    if k == 0: return 0
    utility = 0
    for j in range(k, 2 * k):
        value = w * j / lambda_poisson
        utility += (scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p * (1 - value)) + (scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p) * -value )
    return utility

# 先にk票集まった方に決定する得票数優先意見集約法の最大値を求める
@lru_cache(maxsize=None)
def max_vote_priority(w, p, lambda_poisson):
    value_down = vote_priority_method(1, w, p, lambda_poisson)
    for k in range(2, 100000):
            value_up = vote_priority_method(k, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return  value_down
            value_down = value_up

# pやlambdaに誤差がある場合、先にk票集まった方に決定する得票数優先意見集約法の最大値を求める
@lru_cache(maxsize=None)
def max_vote_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = vote_priority_method(1, w, p, lambda_poisson)
    for k in range(2, 100000):
            value_up = vote_priority_method(k, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return vote_priority_method(k - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

# 方法1のためのメソッド
# T1までに終了しない場合の効用を求める
@lru_cache(maxsize=None)
def not_stop_by_T1(T1, n, w, p, lambda_poisson):
    return np.sum(poisson_probability(i, T1, lambda_poisson) * (acc(i, p) - w * T1) for i in range(0, n))

# 方法1のためのメソッド
# T1までに終了する場合の効用を求める
@lru_cache(maxsize=None)
def stop_by_T1(T1, n, w, p, lambda_poisson):
    return integrate.quad(lambda t: (acc(n, p) - w * t) * gamma_probability(n, t, lambda_poisson), 0, T1)[0]

# 上の二つのメソッドを用いて効用を計算する
@lru_cache(maxsize=None)
def method1(T1, n, w, p, lambda_poisson):
    if n == 0: return 0
    return not_stop_by_T1(T1, n, w, p, lambda_poisson) + stop_by_T1(T1, n, w, p, lambda_poisson)

# 方法1の効用の最大値と、そのときのT1の2要素のリストを求める
@lru_cache(maxsize=None)
def max_method1(w, p, lambda_poisson):
    max_utility = 0
    T1_range = range(1, 10000)
    for t1 in T1_range:
        value_down = method1(t1, 1, w, p, lambda_poisson)
        for n in range(1, 10000):
                value_up = method1(t1, 2 * n + 1, w, p, lambda_poisson)
                if (value_up - value_down) <= 0:
                    if value_down > max_utility:
                        max_utility = value_down
                        break
                    else:
                        return [max_utility, t1]
                value_down = value_up

# pやlambdaに誤差がある場合、方法1の効用の最大値と、そのときのT1の2要素のリストを求める
@lru_cache(maxsize=None)
def max_method1_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    max_utility = 0
    param_arr = np.array((0, 0)) # [0] => T1, [1] => n
    T1_range = range(1, 10000)
    for t1 in T1_range:
        value_down = method1(t1, 1, w, p, lambda_poisson)
        for n in range(1, 10000):
                value_up = method1(t1, 2 * n + 1, w, p, lambda_poisson)
                if (value_up - value_down) <= 0:
                    if value_down > max_utility:
                        max_utility = value_down
                        param_arr = np.array((t1, 2 * n - 1))
                    else:
                        return [method1(param_arr[0], param_arr[1], w, p + p_error, lambda_poisson + lambda_poison_error), t1]
                    break
                value_down = value_up

# 方法2のためのメソッド
@lru_cache(maxsize=None)
def integrate_for_method2_1(T1, T2, n, w, p, lambda_poisson, i):
    return integrate.quad(lambda t: (acc(n, p) - w * t) * g(n, i, t, T1, lambda_poisson), 0, T2)[0]

# 方法2のためのメソッド
@lru_cache(maxsize=None)
def integrate_for_method2_2(T1, T2, n, w, p, lambda_poisson, i):
    return integrate.quad(lambda t: (acc(n, p) - w * T1) * g(n, i, t, T1, lambda_poisson), T2, T1)[0]

# 方法2の効用を計算する
@lru_cache(maxsize=None)
def method2(T1, T2, n, w, p, lambda_poisson):
    if n == 0: return 0
    return not_stop_by_T1(T1, n, w, p, lambda_poisson) \
     + np.sum(integrate_for_method2_1(T1, T2, n, w, p, lambda_poisson, i) \
     # 本当はiを0から無限大まで回したいが不可能なので1.8*t*lambda_poisson回ループする
     + integrate_for_method2_2(T1, T2, n, w, p, lambda_poisson, i) for i in range(n,int(T1 * lambda_poisson * 1.8)))

# 方法2の効用の最大を求める
# 近似のため、T1はmethod1と同じモノを用いる
# 近似のため、utl_errorが0に近付けば近くほどutilityは正確になる(0.00001くらいでよい)
@lru_cache(maxsize=None)
def max_method2(w, p, lambda_poisson, utl_error):
    max_utility = 0
    t1 = max_method1(w, p, lambda_poisson)[1]
    for t2 in range(1, t1 + 1):
        value_down = method2(t1, t2, 1, w, p, lambda_poisson)
        for n in range(1, 10000):
            value_up = method2(t1, t2, 2 * n + 1, w, p, lambda_poisson)
            if value_up - value_down <= utl_error:
                if value_down -  max_utility > utl_error:
                    max_utility = value_down
                    break
                else:
                    return [max_utility, t1, t2]
            value_down = value_up

# pやlambdaに誤差がある場合、方法2の効用の最大を求める
# 近似のため、T1はmethod1と同じモノを用いる
# 近似のため、utl_errorが0に近付けば近くほどutilityは正確になる(0.00001くらいでよい)
@lru_cache(maxsize=None)
def max_method2_with_error(w, p, p_error, lambda_poisson, lambda_poison_error, utl_error):
    max_utility = 0
    param_arr = np.array((0, 0, 0)) # [0] => T1, [1] => T2, [2] => n
    t1 = max_method1_with_error(w, p, 0, lambda_poisson, 0)[1]
    for t2 in range(1, t1 + 1):
        value_down = method2(t1, t2, 1, w, p, lambda_poisson)
        for n in range(1, 10000):
            value_up = method2(t1, t2, 2 * n + 1, w, p, lambda_poisson)
            if value_up - value_down <= utl_error:
                if value_down - max_utility > utl_error:
                    max_utility = value_down
                    param_arr = np.array((t1, t2, 2 * n - 1))
                    break
                else:
                    return method2(param_arr[0], param_arr[1], param_arr[2], w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

# WIP
# 方法3の効用の最大を求める
@lru_cache(maxsize=None)
def method3(T1, k, w, p, lambda_poisson):
    if k == 0: return 0
    utility = 0
    for j in range(k, 2 * k):
        # 積分を行う
        value_1 = integrate.quad(lambda t: w * t * gamma_probability(j, t, lambda_poisson), 0, T1)[0]
        # ----被積分関数を定義----
        @lru_cache(maxsize=None)
        def integrand_for_method3(t):
            integrand = 0
            for l in range(0, j):
                p_sum = 0
                for m in range(0, j):
                    p_sum += poisson_probability(m, T1, lambda_poisson)
                integrand += ((poisson_probability(l, T1, lambda_poisson) * acc(l, p) / p_sum)  - w * T1)
            return integrand * gamma_probability(j, t, lambda_poisson)
        # --------終わり--------
        value_2, abserr = integrate.quad(integrand_for_method3, T1, np.inf)
        utility += scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p * (1 - value_1 + value_2)
        utility += scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p) * (-value_1 + value_2)
    return utility

# ------------グラフをプロットするメソッド------------

# ポアソン分布をプロットする
# x軸:n, y軸:確率
# 単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻tまでにn回起こる確率をnを変動させて出力する
@lru_cache(maxsize=None)
def plot_poisson(time, lambda_poisson):
    x_axis = np.linspace(0, 2 * time * lambda_poisson, 2 * time * lambda_poisson + 1)
    y_axis = [poisson_probability(x, time, lambda_poisson) for x in x_axis]
    plt.title('poisson time: {0} lambda: {1}'.format(time, lambda_poisson))
    plt.xlabel('n')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.savefig("poisson.png")
    plt.show()

# 累積ポアソン分布をプロットする
# x軸:n, y軸:確率
# 単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻tまでに0,1,2,3...n回起こる確率をnを変動させて出力する
@lru_cache(maxsize=None)
def plot_cumulative_poisson(time, lambda_poisson):
    x_axis = np.linspace(0, 2 * time * lambda_poisson, 2 * time * lambda_poisson + 1)
    y_axis = []
    for x in x_axis:
        y_axis.append(cumulative_poisson_probability(int(x), time, lambda_poisson))
    plt.title('cumulative poisson time: {0} lambda: {1}'.format(time, lambda_poisson))
    plt.xlabel('n')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

# ガンマ分布をプロットする
# x軸:t, y軸:確率
# 単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻tにn回目が起こる確率をプロットする
@lru_cache(maxsize=None)
def plot_gamma(n, lambda_poisson):
    x_axis = np.linspace(0, 2 * n / lambda_poisson , 10 * n / lambda_poisson)
    y_axis = [gamma_probability(n, x, lambda_poisson) for x in x_axis]
    plt.title('gamma n: {0} lambda: {1}'.format(n, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.savefig("gamma.png")
    plt.show()

# 累積ガンマ分布をプロットする
# x軸:t, y軸:確率
# 単位時間あたり平均λ回発生するようなランダムな事象があるときに、時刻0~tにn回目が起こる確率をプロットする
@lru_cache(maxsize=None)
def plot_cumulative_gamma(n, lambda_poisson):
    x_axis = np.linspace(0, 2 * n / lambda_poisson , 2 * n / lambda_poisson + 1)
    y_axis = []
    for x in x_axis:
        y_axis.append(cumulative_gamma_probability(n, x, lambda_poisson))
    plt.title('cumulative gamma n: {0} lambda: {1}'.format(n, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

# 関数gをプロットする
# x軸:t, y軸:確率
@lru_cache(maxsize=None)
def plot_g(m, n, T, lambda_poisson):
    x_axis = np.linspace(0, T, T + 1)
    y_axis = [g(m, n, x, T, lambda_poisson) for x in x_axis]
    plt.title("g m: {0} n: {1} T:{2} lambda: {3}".format(m, n, T, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.savefig("g.png")
    plt.show()

# 時刻優先意見集約法をプロットする
# x軸:時刻, y軸:効用
@lru_cache(maxsize=None)
def plot_time_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [time_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('time priority method weight: {0} person_probability: {1} lambda_poisson: {2}'.format(w, p, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.savefig("time_priority.png")
    plt.show()

# 投票数優先意見集約法をプロットする
# x軸:投票数, y軸:効用
@lru_cache(maxsize=None)
def plot_poll_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [poll_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('poll priority method weight: {0} person_probability: {1} lambda_poisson: {2}'.format(w, p, lambda_poisson))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.savefig("poll_priority.png")
    plt.show()

# 得票数優先意見集約法をプロットする
# x軸:得票数, y軸:効用
@lru_cache(maxsize=None)
def plot_vote_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [vote_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('vote priority method weight: {0} person_probability: {1} lambda_poisson: {2}'.format(w, p, lambda_poisson))
    plt.xlabel('require vote people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.savefig("vote_priority.png")
    plt.show()

# 方法1をプロットする
# x軸:投票数, y軸:効用
@lru_cache(maxsize=None)
def plot_method1(w, p, lambda_poisson, s_time, t_time):
    # 最適なパラメータT1を固定してからループを回す
    T1 = max_method1(w, p, lambda_poisson)[1]
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method1(T1,int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method1 T1: {0} weight: {1} person_probability: {2} lambda_poisson: {3}'.format(T1, w, p, lambda_poisson))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.savefig("method1.png")
    plt.show()

# 方法2をプロットする
# x軸:投票数, y軸:効用
@lru_cache(maxsize=None)
def plot_method2(w, p, lambda_poisson, s_time, t_time):
    # 最適なパラメータT1,T2に固定してからループを回す
    max_method2_arr = max_method2(w, p, lambda_poisson, 0.0001)
    T1 = max_method2_arr[1]
    T2 = max_method2_arr[2]
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method2(T1, T2, int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method2 T1: {0} T2: {1} weight: {2} person_probability: {3} lambda_poisson: {4}'.format(T1, T2, w, p, lambda_poisson))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.savefig("method2.png")
    plt.show()

# WIP
@lru_cache(maxsize=None)
def plot_method3(T1, w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method3(T1,int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method3 T1: {0} weight: {1} person_probability: {2} lambda_poisson: {3}'.format(T1, w, p, lambda_poisson))
    plt.xlabel('require vote people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.savefig("method3.png")
    plt.show()

# pに誤差がある場合に手法を比較する
# x軸:実際のp, y軸:効用
@lru_cache(maxsize=None)
def plot_method_utility_with_p_error(w, predicted_p, predicted_lambda_poisson, lambda_poison_error, utl_error):
    x_axis = np.linspace(0.51, 0.99, 49)
    time_priority_axis = [max_time_priority_with_error(w, predicted_p, p - predicted_p, predicted_lambda_poisson, lambda_poison_error) for p in x_axis]
    poll_priority_axis = [max_poll_priority_with_error(w, predicted_p, p - predicted_p, predicted_lambda_poisson, lambda_poison_error) for p in x_axis]
    vote_priority_axis = [max_vote_priority_with_error(w, predicted_p, p - predicted_p, predicted_lambda_poisson, lambda_poison_error) for p in x_axis]
    method1_axis = [max_method1_with_error(w, predicted_p, p - predicted_p, predicted_lambda_poisson, lambda_poison_error)[0] for p in x_axis]
    method2_axis = [max_method2_with_error(w, predicted_p, p - predicted_p, predicted_lambda_poisson, lambda_poison_error, utl_error) for p in x_axis]
    plt.title('method utility with p error w: {0} predicted_p: {1} predicted_lambda: {2} lambda_error: {3} utl_error: {4}'.format(w, predicted_p, predicted_lambda_poisson, lambda_poison_error, utl_error))
    plt.xlabel('actual p')
    plt.ylabel('utility')
    plt.plot(x_axis, time_priority_axis, label="time priority")
    plt.plot(x_axis, poll_priority_axis, label="poll priority")
    plt.plot(x_axis, vote_priority_axis, label="vote priority")
    plt.plot(x_axis, method1_axis, label="method1")
    plt.plot(x_axis, method2_axis, label="method2")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.savefig("method_utility_with_p_error.png")
    plt.show()


# λに誤差がある場合に手法を比較する
# x軸:実際のλ, y軸:効用
@lru_cache(maxsize=None)
def plot_method_utility_with_lambda_poisson_error(w, predicted_p, p_error, predicted_lambda_poisson, utl_error):
    x_axis = np.linspace(0, 1, 10)
    time_priority_axis = [max_time_priority_with_error(w, predicted_p, p_error, predicted_lambda_poisson, lambda_poisson - predicted_lambda_poisson) for lambda_poisson in x_axis]
    poll_priority_axis = [max_poll_priority_with_error(w, predicted_p, p_error, predicted_lambda_poisson, lambda_poisson - predicted_lambda_poisson) for lambda_poisson in x_axis]
    vote_priority_axis = [max_vote_priority_with_error(w, predicted_p, p_error, predicted_lambda_poisson, lambda_poisson - predicted_lambda_poisson) for lambda_poisson in x_axis]
    method1_axis = [max_method1_with_error(w, predicted_p, p_error, predicted_lambda_poisson, lambda_poisson - predicted_lambda_poisson)[0] for lambda_poisson in x_axis]
    method2_axis = [max_method2_with_error(w, predicted_p, p_error, predicted_lambda_poisson, lambda_poisson - predicted_lambda_poisson, utl_error) for lambda_poisson in x_axis]
    plt.title('method utility with lambda error w: {0} predicted_p: {1} p_error: {2} predicted_lambda: {3} utl_error: {4}'.format(w, predicted_p, p_error, predicted_lambda_poisson, utl_error))
    plt.xlabel('actual lambda')
    plt.ylabel('utility')
    plt.plot(x_axis, time_priority_axis, label="time priority")
    plt.plot(x_axis, poll_priority_axis, label="poll priority")
    plt.plot(x_axis, vote_priority_axis, label="vote priority")
    plt.plot(x_axis, method1_axis, label="method1")
    plt.plot(x_axis, method2_axis, label="method2")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.savefig("method_utility_with_lambda_poisson_error.png")
    plt.show()

# x軸:p, y軸:λとして、最適な手法の色をプロットする
@lru_cache(maxsize=None)
def plot_best_method(w, p_error, lambda_error, utl_error):
    color_list = []
    lambda_range = np.linspace(0, 1, 2)
    p_range = np.linspace(0.6, 0.9, 2)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('best method plot w: {0} p_error: {1} lambda_error: {2} utl_error: {3}'.format(w, p_error, lambda_error, utl_error))
    ax.set_xlabel('predicted p')
    ax.set_ylabel('predicted lambda')
    for p_i in range(len(p_range)):
        for l_i in range(len(lambda_range)):
            max_utility_dict = {
                "red": max_time_priority_with_error(w, p_range[p_i], p_error, lambda_range[l_i], lambda_error),
                "yellow": max_poll_priority_with_error(w, p_range[p_i], p_error, lambda_range[l_i], lambda_error),
                "blue": max_vote_priority_with_error(w, p_range[p_i], p_error, lambda_range[l_i], lambda_error),
                "gray": max_method1_with_error(w, p_range[p_i], p_error, lambda_range[l_i], lambda_error)[0],
#                 "black": max_method2_with_error(w, p_range[p_i], p_error, lambda_range[l_i], lambda_error, utl_error)
            }
            ax.scatter(p_range[p_i], lambda_range[l_i], marker='s', s=150, c=max(max_utility_dict.items(), key=lambda x:x[1])[0], alpha=0.7)
    fig.savefig("best_method.png")
    fig.show()
