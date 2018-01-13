# 1,準備
# Poisson過程
# 単位時間あたりの到着数 λ
# 時刻tまでにn人が到着する確率
def poisson_probability(n, t, lambda_poisson):
    return float(math.e**(-lambda_poisson * t) * (lambda_poisson * t)**n / math.factorial(n))

# Gamma分布
# 時刻tにn人目が到着する確率
def gamma_probability(n, t, lambda_poisson):
    return float(lambda_poisson**n * Decimal(t)**(n - 1) * Decimal(math.e)**(-lambda_poisson * Decimal(t)) / math.factorial(n - 1))


# 時刻Tまでにn人現われるときに， 時刻t(=< T)にm(=< n)人目が到着する確率g(m,n,t,T)
def g(m, n, t, T, lambda_poisson):
    return float(lambda_poisson**Decimal(n) / (math.factorial(Decimal(m) - Decimal(1)) * math.factorial(Decimal(n) - Decimal(m))) \
    * Decimal(t)**Decimal(m - 1) * Decimal(T - t)**Decimal(n - m) * Decimal(math.e)**(Decimal(-1) * Decimal(lambda_poisson) * Decimal(T)))

# 多数決による判定精度
# n人で多数決を行う場合の判定精度をacc(n)で表す
# 個人の判定精度をpとする
def acc_odd(n, p): # nが奇数2i-1のとき
    i = int((n + 1) / 2)
    acc = 0
    for j in range(i):
        acc += scm.comb(2 * i - 1, j) * p**(2 * i - 1 - j) * (1 - p)**j
    return acc

def acc_even(n, p): # nが偶数2iのとき
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

# 2,単純な意見集約法
# 2.1,時刻優先意見集約法
# 時刻tまで待って多数決を行う
# 効用を予測精度と所要時間の差で表す
def time_priority_method(t, w, p, lambda_poisson):
    if t == 0: return 0
    return np.sum(poisson_probability(i, t, lambda_poisson) * acc(i, p) for i in xrange(1,200)) - (w * t)


# 増減を調べる
def inc_and_dec_time_priority_method(w, p, lambda_poisson):
    for t in xrange(1, 1000):
        diff = time_priority_method(t + 1, w, p, lambda_poisson) - time_priority_method(t, w, p, lambda_poisson)
        if diff < 0: return t

# 2.2, 投票数優先意見集約法
# n人集まるまで待って多数決を行う
# 効用を予測精度と所要時間の差で表す
def poll_priority_method(n, w, p, lambda_poisson):
    if n == 0: return 0
    return acc(n, p) - integrate.quad(lambda t: w * t * gamma_probability(n, t, lambda_poisson), 0, 1000)[0]


# 増減を調べる
def inc_and_dec_poll_priority_method(w, p, lambda_poisson):
    for n in xrange(1, 1000):
        diff = poll_priority_method(2 * n + 1, w, p, lambda_poisson) - poll_priority_method(2 * n - 1, w, p, lambda_poisson)
        if diff < 0: return 2 * n - 1

# 2.3, 得票数優先意見集約法
# 先にk票集まった案に決定する
# 効用を予測精度と所要時間の差で表す
def vote_priority_method(k, w, p, lambda_poisson):
    if k == 0: return 0
    utility = 0
    for j in xrange(k, 2 * k):
        value = integrate.quad(lambda t: w * t * gamma_probability(j, t, lambda_poisson), 0, 1000)[0]
        utility += (scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p * (1 - value)) + (scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p) * -value )
    return utility

# 増減を調べる
def inc_and_dec_vote_priority_method(w, p, lambda_poisson):
    for k in xrange(1, 1000):
        diff = vote_priority_method(k + 1, w, p, lambda_poisson) - vote_priority_method(k, w, p, lambda_poisson)
    if diff < 0: return k

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
    y_axis = []
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
