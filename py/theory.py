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

@lru_cache(maxsize=None)
def time_priority_method(t, w, p, lambda_poisson):
    if t == 0: return 0
    return np.sum(poisson_probability(i, t, lambda_poisson) * acc(i, p) for i in range(1,120)) - (w * t)

@lru_cache(maxsize=None)
def max_time_priority(w, p, lambda_poisson):
    value_down = time_priority_method(1, w, p, lambda_poisson)
    for t in range(2, 1000):
            value_up = time_priority_method(t, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return value_down
            value_down = value_up

@lru_cache(maxsize=None)
def max_time_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = time_priority_method(1, w, p, lambda_poisson)
    for t in range(2, 1000):
            value_up = time_priority_method(t, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return time_priority_method(t - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

@lru_cache(maxsize=None)
def inc_and_dec_time_priority_method(w, p, lambda_poisson):
    for t in range(1, 1000):
        diff = -w
        for i in range(1, 120):
            diff += (poisson_probability(i, t + 1, lambda_poisson) - poisson_probability(i, t, lambda_poisson)) * acc(i, p)
        if diff < 0: return t

@lru_cache(maxsize=None)
def poll_priority_method(n, w, p, lambda_poisson):
    if n == 0: return 0
    return acc(n, p) - w * 0.5 * n

@lru_cache(maxsize=None)
def max_poll_priority(w, p, lambda_poisson):
    value_down = poll_priority_method(1, w, p, lambda_poisson)
    for n in range(1, 1000):
            value_up = poll_priority_method(2 *n + 1, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return value_down
            value_down = value_up

@lru_cache(maxsize=None)
def max_poll_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = poll_priority_method(1, w, p, lambda_poisson)
    for n in range(1, 1000):
            value_up = poll_priority_method(2 *n + 1, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return poll_priority_method(2 * n - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

@lru_cache(maxsize=None)
def inc_and_dec_poll_priority_method(w, p, lambda_poisson):
    for n in range(1, 1000):
        diff = acc(2 * n + 1, p) - acc(2 * n - 1, p) - w
        if diff < 0: return 2 * n - 1

@lru_cache(maxsize=None)
def vote_priority_method(k, w, p, lambda_poisson):
    if k == 0: return 0
    utility = 0
    for j in range(k, 2 * k):
        value = w * 0.5 * j
        utility += (scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p * (1 - value)) + (scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p) * -value )
    return utility

@lru_cache(maxsize=None)
def max_vote_priority(w, p, lambda_poisson):
    value_down = vote_priority_method(1, w, p, lambda_poisson)
    for k in range(2, 1000):
            value_up = vote_priority_method(k, w, p, lambda_poisson)
            if (value_up - value_down) <= 0: return  value_down
            value_down = value_up

@lru_cache(maxsize=None)
def max_vote_priority_with_error(w, p, p_error, lambda_poisson, lambda_poison_error):
    value_down = vote_priority_method(1, w, p, lambda_poisson)
    for k in range(2, 1000):
            value_up = vote_priority_method(k, w, p, lambda_poisson)
            if (value_up - value_down) <= 0:
                return vote_priority_method(k - 1, w, p + p_error, lambda_poisson + lambda_poison_error)
            value_down = value_up

@lru_cache(maxsize=None)
def inc_and_dec_vote_priority_method(w, p, lambda_poisson):
    for k in range(1, 1000):
        diff = vote_priority_method(k + 1, w, p, lambda_poisson) - vote_priority_method(k, w, p, lambda_poisson)
        if diff < 0: return k

@lru_cache(maxsize=None)
def method1(t, w, p, lambda_poisson):
    return time_priority_method(t, w, p, lambda_poisson)

@lru_cache(maxsize=None)
def inc_and_dec_method1(w, p, lambda_poisson):
    return inc_and_dec_time_priority_method(w, p, lambda_poisson)

@lru_cache(maxsize=None)
def not_stop_by_T1(T1, n, w, p, lambda_poisson):
    return np.sum(poisson_probability(i, T1, lambda_poisson) * (acc(i, p) - w * T1) for i in range(0, n))

@lru_cache(maxsize=None)
def stop_by_T1(T1, n, w, p, lambda_poisson):
    return integrate.quad(lambda t: (acc(n, p) - w * t) * gamma_probability(n, t, lambda_poisson), 0, T1)[0]

@lru_cache(maxsize=None)
def method2(T1, n, w, p, lambda_poisson):
    if n == 0: return 0
    return not_stop_by_T1(T1, n, w, p, lambda_poisson) + stop_by_T1(T1, n, w, p, lambda_poisson)

@lru_cache(maxsize=None)
def max_method2(T1_start, T1_end, w, p, lambda_poisson):
    max_utility = 0
    T1_range = range(T1_start, T1_end)
    for t1 in T1_range:
        value_down = method2(t1, 1, w, p, lambda_poisson)
        for n in range(1, 1000):
                value_up = method2(t1, 2 * n + 1, w, p, lambda_poisson)
                if (value_up - value_down) <= 0:
                    if value_down > max_utility: max_utility = value_down
                    break
                value_down = value_up
    return  max_utility

@lru_cache(maxsize=None)
def max_method2_with_error(T1_start, T1_end, w, p, p_error, lambda_poisson, lambda_poison_error):
    max_utility = 0
    param_arr = np.array((0, 0)) # [0] => T1, [1] => n
    T1_range = range(T1_start, T1_end)
    for t1 in T1_range:
        value_down = method2(t1, 1, w, p, lambda_poisson)
        for n in range(1, 1000):
                value_up = method2(t1, 2 * n + 1, w, p, lambda_poisson)
                if (value_up - value_down) <= 0:
                    if value_down > max_utility:
                        max_utility = value_down
                        param_arr = np.array((t1, 2 * n - 1))
                    break
                value_down = value_up
    return  method2(param_arr[0], param_arr[1], w, p + p_error, lambda_poisson + lambda_poison_error)

@lru_cache(maxsize=None)
def inc_and_dec_method2(T1, w, p, lambda_poisson):
    for n in range(1, 1000):
        diff = poisson_probability(2 * n, T1, lambda_poisson) * (acc(2 * n, p) - w * T1) + poisson_probability(2 * n - 1, T1, lambda_poisson) * (acc(2 * n - 1, p) - w * T1) + integrate.quad(lambda t: (acc(2 * n + 1, p) - w * t) * gamma_probability(2 * n + 1, t, lambda_poisson), 0, T1)[0] - integrate.quad(lambda t: (acc(2 * n - 1 , p) - w * t) * gamma_probability(2 * n - 1, t, lambda_poisson), 0, T1)[0]
        if diff < 0:
            return 2 * n - 1

# @lru_cache(maxsize=None)
# def method3(T1, T2, n, w, p, lambda_poisson):
#     if n == 0: return 0
#     return np.sum(poisson_probability(i, T1, lambda_poisson) * (acc(i, p) - w * T1) for i in range(0, n)) + \
#     np.sum(integrate.quad(lambda t: (acc(n, p) - w * t) * g(n, i, t, T1, lambda_poisson), 0, T2)[0] + \
#     integrate.quad(lambda t: (acc(n, p) - w * T1) * g(n, i, t, T1, lambda_poisson), T2, T1)[0] for i in range(n, 120))

@lru_cache(maxsize=None)
def integrate_for_method3_1(T1, T2, n, w, p, lambda_poisson, i):
    return integrate.quad(lambda t: (acc(n, p) - w * t) * g(n, i, t, T1, lambda_poisson), 0, T2)[0]

@lru_cache(maxsize=None)
def integrate_for_method3_2(T1, T2, n, w, p, lambda_poisson, i):
    return integrate.quad(lambda t: (acc(n, p) - w * T1) * g(n, i, t, T1, lambda_poisson), T2, T1)[0]

@lru_cache(maxsize=None)
def method3(T1, T2, n, w, p, lambda_poisson):
    if n == 0: return 0
    return not_stop_by_T1(T1, n, w, p, lambda_poisson) + np.sum(integrate_for_method3_1(T1, T2, n, w, p, lambda_poisson, i) + integrate_for_method3_2(T1, T2, n, w, p, lambda_poisson, i) for i in range(n, 100))

@lru_cache(maxsize=None)
def max_method3(T1_start, T1_end, w, p, lambda_poisson):
    max_utility = 0
    T1_range = range(T1_start, T1_end)
    for t1 in T1_range:
        for t2 in range(1, t1 + 1):
            temp_utility_list = []
            value_down = method3(t1, t2, 1, w, p, lambda_poisson)
            for n in range(1, 1000):
                value_up = method3(t1, t2, 2 * n + 1, w, p, lambda_poisson)
                if (value_up - value_down) <= 0:
                    if value_down > max_utility: max_utility = value_down
                    break
                value_down = value_up
    return max_utility

@lru_cache(maxsize=None)
def max_method3_with_error(T1_start, T1_end, w, p, p_error, lambda_poisson, lambda_poison_error):
    max_utility = 0
    param_arr = np.array((0, 0, 0)) # [0] => T1, [1] => T2, [2] => n
    T1_range = range(T1_start, T1_end)
    for t1 in T1_range:
        for t2 in range(1, t1 + 1):
            value_down = method3(t1, t2, 1, w, p, lambda_poisson)
            for n in range(1, 1000):
                value_up = method3(t1, t2, 2 * n + 1, w, p, lambda_poisson)
                if (value_up - value_down) <= 0:
                    if value_down > max_utility:
                        max_utility = value_down
                        param_arr = np.array((t1, t2, 2 * n - 1))
                    break
                value_down = value_up
    return method3(param_arr[0], param_arr[1], param_arr[2], w, p + p_error, lambda_poisson + lambda_poison_error)

@lru_cache(maxsize=None)
def inc_and_dec_method3(T1, T2, w, p, lambda_poisson):
    for n in range (1, 1000):
        diff = poisson_probability(2 * n, T1, lambda_poisson) * (acc(2 * n, p) - w * T1) + poisson_probability(2 * n - 1, T1, lambda_poisson) * (acc(2 * n - 1, p) - w * T1) \
        + np.sum(integrate.quad(lambda t: (acc(2 * n + 1, p) - w * t) * g(2 * n + 1, i, t, T1, lambda_poisson), 0, T2)[0] + \
        integrate.quad(lambda t: (acc(2 * n + 1, p) - w * T1) * g(2 * n + 1, i, t, T1, lambda_poisson), T2, T1)[0] for i in range(2 * n + 1, 30)) \
        - np.sum(integrate.quad(lambda t: (acc(2* n - 1, p) - w * t) * g(2 * n - 1, i, t, T1, lambda_poisson), 0, T2)[0] + \
        integrate.quad(lambda t: (acc(2 * n - 1, p) - w * T1) * g(2 * n - 1, i, t, T1, lambda_poisson), T2, T1)[0] for i in range(2 * n - 1, 30))
        if diff < 0:
            return 2 * n - 1

@lru_cache(maxsize=None)
def method4(T1, k, w, p, lambda_poisson):
    if k == 0: return 0
    utility = 0
    for j in range(k, 2 * k):
        # 積分を行う
        value_1 = integrate.quad(lambda t: w * t * gamma_probability(j, t, lambda_poisson), 0, T1)[0]
        # ----被積分関数を定義----
        @lru_cache(maxsize=None)
        def integrand_for_method4(t):
            integrand = 0
            for l in range(0, j):
                p_sum = 0
                for m in range(0, j):
                    p_sum += poisson_probability(m, T1, lambda_poisson)
                integrand += ((poisson_probability(l, T1, lambda_poisson) * acc(l, p) / p_sum)  - w * T1)
            return integrand * gamma_probability(j, t, lambda_poisson)
        # --------終わり--------
        value_2, abserr = integrate.quad(integrand_for_method4, T1, np.inf)
        utility += scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p * (1 - value_1 + value_2)
        utility += scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p) * (-value_1 + value_2)
    return utility
