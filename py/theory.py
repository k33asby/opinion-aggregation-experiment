@lru_cache(maxsize=None)
def poisson_probability(n, t, lambda_poisson):
    return math.e**(-lambda_poisson * t) * (lambda_poisson * t)**n / math.factorial(n)

@lru_cache(maxsize=None)
def gamma_probability(n, t, lambda_poisson):
    return lambda_poisson**n * t**(n - 1) * math.e**(-lambda_poisson * t) / math.factorial(n - 1)

@lru_cache(maxsize=None)
def g(m, n, t, T, lambda_poisson):
    return lambda_poisson**n * t**(m - 1) * (T - t)**(n - m) * math.e**(-lambda_poisson * T) / (math.factorial(m - 1) * math.factorial(n - m))

@lru_cache(maxsize=None)
def acc_odd(n, p):
    i = int((n + 1) / 2)
    acc = 0
    for j in range(i):
        acc += scm.comb(2 * i - 1, j) * p**(2 * i - 1 - j) * (1 - p)**j
    return acc

@lru_cache(maxsize=None)
def acc_even(n, p):
    i = int(n / 2)
    acc = 0
    for j in range(i):
        acc += scm.comb(2 * i, j) * p**(2 * i - j) * (1 - p)**j
    acc += scm.comb(2 * i, i) * p**i * (1 - p)**i / 2
    return acc

@lru_cache(maxsize=None)
def acc(n, p):
    if n % 2 == 1:
        return acc_odd(n, p)
    else:
        return acc_even(n, p)

# tまでに平均 t * lambda人到着するので、無限人まで繰り返したいが不可能なので t * lambda * 1.8回繰り返す
@lru_cache(maxsize=None)
def time_priority_method(t, w, p, lambda_poisson):
    if t == 0: return 0
    return np.sum(poisson_probability(i, t, lambda_poisson) * acc(i, p) for i in range(1, 1.8 * t * lambda_poisson)) - w * t

@lru_cache(maxsize=None)
def max_time_priority(w, p, lambda_poisson):
    value_down = time_priority_method(1, w, p, lambda_poisson)
    for t in range(2, 100000):
            value_up = time_priority_method(t, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return value_down
            value_down = value_up

@lru_cache(maxsize=None)
def max_time_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = time_priority_method(1, w, p, lambda_poisson)
    for t in range(2, 100000):
            value_up = time_priority_method(t, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return time_priority_method(t - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

@lru_cache(maxsize=None)
def poll_priority_method(n, w, p, lambda_poisson):
    if n == 0: return 0
    return acc(n, p) - w * n / lambda_poisson

@lru_cache(maxsize=None)
def max_poll_priority(w, p, lambda_poisson):
    value_down = poll_priority_method(1, w, p, lambda_poisson)
    for n in range(1, 100000):
            value_up = poll_priority_method(2 *n + 1, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return value_down
            value_down = value_up

@lru_cache(maxsize=None)
def max_poll_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = poll_priority_method(1, w, p, lambda_poisson)
    for n in range(1, 100000):
            value_up = poll_priority_method(2 * n + 1, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return poll_priority_method(2 * n - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

@lru_cache(maxsize=None)
def vote_priority_method(k, w, p, lambda_poisson):
    if k == 0: return 0
    utility = 0
    for j in range(k, 2 * k):
        value = w * j / lambda_poisson
        utility += (scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p * (1 - value)) + (scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p) * -value )
    return utility

@lru_cache(maxsize=None)
def max_vote_priority(w, p, lambda_poisson):
    value_down = vote_priority_method(1, w, p, lambda_poisson)
    for k in range(2, 100000):
            value_up = vote_priority_method(k, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return  value_down
            value_down = value_up

@lru_cache(maxsize=None)
def max_vote_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = vote_priority_method(1, w, p, lambda_poisson)
    for k in range(2, 100000):
            value_up = vote_priority_method(k, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return vote_priority_method(k - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

@lru_cache(maxsize=None)
def not_stop_by_T1(T1, n, w, p, lambda_poisson):
    return np.sum(poisson_probability(i, T1, lambda_poisson) * (acc(i, p) - w * T1) for i in range(0, n))

@lru_cache(maxsize=None)
def stop_by_T1(T1, n, w, p, lambda_poisson):
    return integrate.quad(lambda t: (acc(n, p) - w * t) * gamma_probability(n, t, lambda_poisson), 0, T1)[0]

@lru_cache(maxsize=None)
def method1(T1, n, w, p, lambda_poisson):
    if n == 0: return 0
    return not_stop_by_T1(T1, n, w, p, lambda_poisson) + stop_by_T1(T1, n, w, p, lambda_poisson)

# 返り値は最大の効用とその時のT1のリスト
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

@lru_cache(maxsize=None)
def integrate_for_method2_1(T1, T2, n, w, p, lambda_poisson, i):
    return integrate.quad(lambda t: (acc(n, p) - w * t) * g(n, i, t, T1, lambda_poisson), 0, T2)[0]

@lru_cache(maxsize=None)
def integrate_for_method2_2(T1, T2, n, w, p, lambda_poisson, i):
    return integrate.quad(lambda t: (acc(n, p) - w * T1) * g(n, i, t, T1, lambda_poisson), T2, T1)[0]

# T1までに平均 T1 * lambda人到着するので、無限人まで繰り返したいが不可能なので T1 * lambda * 1.8回繰り返す
@lru_cache(maxsize=None)
def method2(T1, T2, n, w, p, lambda_poisson):
    if n == 0: return 0
    return not_stop_by_T1(T1, n, w, p, lambda_poisson) \
     + np.sum(integrate_for_method2_1(T1, T2, n, w, p, lambda_poisson, i) \
     + integrate_for_method2_2(T1, T2, n, w, p, lambda_poisson, i) for i in range(n,int(T1 * lambda_poisson * 1.8)))

# utl_errorが0に近付けば近くほどutilityは正確になる(0.00001くらいでよい)
# T1はmethod1と同じモノを用いる
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
                    return max_utility
            value_down = value_up

# utl_errorが0に近付けば近くほどutilityは正確になる(0.00001くらいでよい)
# T1はmethod1と同じモノを用いる
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
@lru_cache(maxsize=None)
def plot_poisson(time, lambda_poisson):
    x_axis = np.linspace(0, 2 * time * lambda_poisson, 2 * time * lambda_poisson + 1)
    y_axis = [poisson_probability(x, time, lambda_poisson) for x in x_axis]
    plt.title('poisson time: {0} lambda: {1}'.format(time, lambda_poisson))
    plt.xlabel('people')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

@lru_cache(maxsize=None)
def plot_gamma(people, lambda_poisson):
    x_axis = np.linspace(0, 2 * people / lambda_poisson , 2 * people / lambda_poisson + 1)
    y_axis = [gamma_probability(people, x, lambda_poisson) for x in x_axis]
    plt.title('gamma people: {0} lambda: {1}'.format(people, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

@lru_cache(maxsize=None)
def plot_g(m, n, T, lambda_poisson):
    x_axis = np.linspace(0, T, T + 1)
    y_axis = [g(m, n, x, T, lambda_poisson) for x in x_axis]
    plt.title("g m: {0} n: {1} T:{2} lambda: {3}".format(m, n, T, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

@lru_cache(maxsize=None)
def plot_time_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [time_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('time priority method weight: {0} person_probability: {1}'.format(w, p))
    plt.xlabel('time')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

@lru_cache(maxsize=None)
def plot_poll_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [poll_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('poll priority method weight: {0} person_probability: {1}'.format(w, p))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

@lru_cache(maxsize=None)
def plot_vote_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [vote_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('vote priority method weight: {0} person_probability: {1}'.format(w, p))
    plt.xlabel('require vote people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

@lru_cache(maxsize=None)
def plot_method1(T1, w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method1(T1,int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method1 T1: {0} weight: {1} person_probability: {2}'.format(T1, w, p))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

@lru_cache(maxsize=None)
def plot_method2(T1, T2, w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method2(T1, T2, int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method2 T1: {0} T2: {1} weight: {2} person_probability: {3}'.format(T1, T2, w, p))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

# WIP
@lru_cache(maxsize=None)
def plot_method3(T1, w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method3(T1,int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method3 T1: {0} weight: {1} person_probability: {2}'.format(T1, w, p))
    plt.xlabel('require vote people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

# 横軸 実際のp, 縦軸 utility
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
    plt.show()

# 横軸 実際のlambda, 縦軸 utility
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
    plt.show()

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
    fig.show()
