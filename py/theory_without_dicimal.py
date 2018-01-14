def poisson_probability(n, t, lambda_poisson):
    return math.e**(-lambda_poisson * t) * (lambda_poisson * t)**n / math.factorial(n)

# P(n, t+1) - P(n, t)
def diff_poisson(n, t, lambda_poisson):
    return math.e**(-lambda_poisson * t) * (lambda_poisson * t)**n * (math.e**-lambda_poisson * lambda_poisson**n - 1) / math.factorial(n)

def gamma_probability(n, t, lambda_poisson):
    return lambda_poisson**n * t**(n - 1) * math.e**(-lambda_poisson * t) / math.factorial(n - 1)

def g(m, n, t, T, lambda_poisson):
    return lambda_poisson**n * t**(m - 1) * (T - t)**(n - m) * math.e**(-lambda_poisson * T) / (math.factorial(m - 1) * math.factorial(n - m))

def acc_odd(n, p):
    i = int((n + 1) / 2)
    acc = 0
    for j in range(i):
        acc += scm.comb(2 * i - 1, j) * p**(2 * i - 1 - j) * (1 - p)**j
    return acc

def acc_even(n, p):
    i = int(n / 2)
    acc = 0
    for j in range(i):
        acc += scm.comb(2 * i, j) * p**(2 * i - j) * (1 - p)**j
    acc += scm.comb(2 * i, i) * p**i * (1 - p)**i / 2
    return acc

def acc(n, p):
    if n % 2 == 1:
        return acc_odd(n, p)
    else:
        return acc_even(n, p)

def time_priority_method(t, w, p, lambda_poisson):
    if t == 0: return 0
    return np.sum(poisson_probability(i, t, lambda_poisson) * acc(i, p) for i in range(1,200)) - (w * t)

def inc_and_dec_time_priority_method(w, p, lambda_poisson):
    for t in range(1, 1000):
        diff = time_priority_method(t + 1, w, p, lambda_poisson) - time_priority_method(t, w, p, lambda_poisson)
        if diff < 0: return t

# 正しい動作しない
# def diff_time_priority_method(w, p, lambda_poisson):
#     for t in range(1, 1000):
#         diff = np.sum(diff_poisson(i, t, lambda_poisson) * acc(i, p) for i in range(1,200)) - w
#         if diff < 0: return t

def poll_priority_method(n, w, p, lambda_poisson):
    if n == 0: return 0
    return acc(n, p) - integrate.quad(lambda t: w * t * gamma_probability(n, t, lambda_poisson), 0, 1000)[0]

def inc_and_dec_poll_priority_method(w, p, lambda_poisson):
    for n in range(1, 1000):
        diff = poll_priority_method(2 * n + 1, w, p, lambda_poisson) - poll_priority_method(2 * n - 1, w, p, lambda_poisson)
        if diff < 0: return 2 * n - 1

def vote_priority_method(k, w, p, lambda_poisson):
    if k == 0: return 0
    utility = 0
    for j in range(k, 2 * k):
        value = integrate.quad(lambda t: w * t * gamma_probability(j, t, lambda_poisson), 0, 1000)[0]
        utility += (scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p * (1 - value)) + (scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p) * -value )
    return utility

def inc_and_dec_vote_priority_method(w, p, lambda_poisson):
    for k in range(1, 1000):
        diff = vote_priority_method(k + 1, w, p, lambda_poisson) - vote_priority_method(k, w, p, lambda_poisson)
    if diff < 0: return k

def method1(t, w, p, lambda_poisson):
    return time_priority_method(t, w, p, lambda_poisson)

def inc_and_dec_method1(w, p, lambda_poisson):
    return inc_and_dec_time_priority_method(w, p, lambda_poisson)

def method2(T1, n, w, p, lambda_poisson):
    if n == 0: return 0
    return np.sum(poisson_probability(i, T1, lambda_poisson) * (acc(i, p) - w * T1) for i in range(0, n)) + integrate.quad(lambda t: (acc(n, p) - w * t) * gamma_probability(n, t, lambda_poisson), 0, T1)[0]

def inc_and_dec_method2(T1, w, p, lambda_poisson):
    for n in range(1, 50):
        diff = method2(T1, 2 * n + 1, w, p, lambda_poisson) - method2(T1, 2 * n - 1, w, p, lambda_poisson)
        if diff < 0:
            return 2 * n - 1

def method3(T1, T2, n, w, p, lambda_poisson):
    if n == 0: return 0
    return np.sum(poisson_probability(i, T1, lambda_poisson) * (acc(i, p) - w * T1) for i in range(0, n)) + \
    np.sum(integrate.quad(lambda t: (acc(n, p) - w * t) * g(n, i, t, T1, lambda_poisson), 0, T2)[0] + \
    integrate.quad(lambda t: (acc(n, p) - w * T1) * g(n, i, t, T1, lambda_poisson), T2, T1)[0] for i in range(n, 120))

def inc_and_dec_method3(T1, T2, w, p, lambda_poisson):
    for n in range(1, 50):
        diff = method3(T1, T2, 2 * n + 1, w, p, lambda_poisson) - method3(T1, T2, 2 * n - 1, w, p, lambda_poisson)
        if diff < 0:
            return 2 * n - 1

# ------------グラフをプロットするメソッド------------
def plot_poisson(time, lambda_poisson):
    x_axis = np.linspace(0, 2 * time * lambda_poisson, 2 * time * lambda_poisson + 1)
    y_axis = [poisson_probability(x, time, lambda_poisson) for x in x_axis]
    plt.title('poisson time: {0} lambda: {1}'.format(time, lambda_poisson))
    plt.xlabel('people')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_gamma(people, lambda_poisson):
    x_axis = np.linspace(0, 2 * people / lambda_poisson , 2 * people / lambda_poisson + 1)
    y_axis = [gamma_probability(people, x, lambda_poisson) for x in x_axis]
    plt.title('gamma people: {0} lambda: {1}'.format(people, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_g(m, n, T, lambda_poisson):
    x_axis = np.linspace(0, T, T + 1)
    y_axis = [g(m, n, x, T, lambda_poisson) for x in x_axis]
    plt.title("g m: {0} n: {1} T:{2} lambda: {3}".format(m, n, T, lambda_poisson))
    plt.xlabel('time')
    plt.ylabel('probability')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_time_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [time_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('time priority method weight: {0} person_probability: {1}'.format(w, p))
    plt.xlabel('time')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_poll_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [poll_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('poll priority method weight: {0} person_probability: {1}'.format(w, p))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_vote_priority(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [vote_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('vote priority method weight: {0} person_probability: {1}'.format(w, p))
    plt.xlabel('require vote people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_method1(w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [time_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method1 weight: {0} person_probability: {1}'.format(w, p))
    plt.xlabel('time')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_method2(T1, w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method2(T1,int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method2 T1: {0} weight: {1} person_probability: {2}'.format(T1, w, p))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()

def plot_method3(T1, T2, w, p, lambda_poisson, s_time, t_time):
    x_axis = np.linspace(s_time, t_time, t_time - s_time + 1)
    y_axis = [method3(T1, T2, int(x), w, p, lambda_poisson) for x in x_axis]
    plt.title('method3 T1: {0} T2: {1} weight: {2} person_probability: {3}'.format(T1, T2, w, p))
    plt.xlabel('poll people')
    plt.ylabel('utility')
    plt.plot(x_axis, y_axis)
    plt.show()
