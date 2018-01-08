class modeling:

    def __init__(self,lambda_poisson, repeat):
        self.lambda_poisson = lambda_poisson
        self.collecting_deadline = lambda_poisson * 2
        self.repeat = repeat
        self.poisson = np.random.poisson(lambda_poisson, 1000)

    def half_num(self,num):
        return int(math.ceil(float(num) / 2))

    def simulate_when_people_come_list(self, people_num):
        when_people_come = [0] * self.collecting_deadline
        for t in range(people_num):
            when_people_come[t] = 1
        random.shuffle(when_people_come)
        return when_people_come

    def probability_correct_by_majority_vote(self, people_num, probability_correct):
        return (1 - self.relative_error_by_majority_vote(people_num, probability_correct))

    def relative_error_by_majority_vote(self, people_num, probability_correct):
        half_num = self.half_num(people_num)
        relative_error = 0
        for t in range(half_num):
            relative_error += (probability_correct**t) * ((1 - probability_correct)**(people_num - t)) * scm.comb(people_num, t)
        return relative_error

    def probability_correct_list_by_half_opinion(self, finish_num, probability_correct):
        probability_correct_list = []
        for t in range(finish_num):
            probability_correct_list.append((probability_correct**finish_num) * ((1 - probability_correct)**t) * scm.comb(finish_num - 1 + t, t))
        return probability_correct_list

    def relative_error_list_by_half_opinion(self, finish_num, probability_correct):
        relative_error = []
        for t in range(finish_num):
            relative_error.append(((1 - probability_correct)**finish_num) * (probability_correct**t) * scm.comb(finish_num - 1 + t, t))
        return relative_error

    def method_utility_list_decideing_by_first_person(self, probability_correct, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                method_utility += probability_correct - weight * (float(i) / self.collecting_deadline)
                break
            method_utility_list.append(method_utility)
        return method_utility_list

    def method_utility_list_decideing_by_majority_vote(self, probability_correct, majority_vote_people, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            if people_num < majority_vote_people: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count += 1
                if people_count == majority_vote_people:
                    method_utility +=  self.probability_correct_by_majority_vote(people_count, probability_correct) - weight * (float(i) / self.collecting_deadline)
                    break
            method_utility_list.append(method_utility)
        return method_utility_list

    def method_utility_list_decideing_by_half_opinion(self, probability_correct, temp_people_num, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            people_count_list = []
            if people_num < temp_people_num: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count_list.append(i)
                people_count += 1
                if people_count == temp_people_num:
                    probability_correct_list = self.probability_correct_list_by_half_opinion(self.half_num(temp_people_num), probability_correct)
                    sum_probability = sum(probability_correct_list)
                    average_index = 0
                    for index in range(len(probability_correct_list)):
                        average_index += people_count_list[self.half_num(temp_people_num) - 1 + index] * (probability_correct_list[index] / sum_probability)
                    method_utility = sum_probability - weight * (float(average_index) / self.collecting_deadline)
                    break
            method_utility_list.append(method_utility)
        return method_utility_list

    def method_utility_list_decideing_by_time_limit(self, probability_correct, time_limit, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            for i in range(len(when_people_come)):
                if i >= time_limit and people_count >= 1:
                    method_utility = (1 - self.relative_error_by_majority_vote(people_count, probability_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
                if when_people_come[i] == 0: continue
                people_count += 1
            method_utility_list.append(method_utility)
        return method_utility_list

    def deciding_by_first_person_average(self, probability_correct, weight):
        method_utility_list = self.method_utility_list_decideing_by_first_person(probability_correct, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_majority_vote_average(self, probability_correct, majority_vote_people, weight):
        method_utility_list = self.method_utility_list_decideing_by_majority_vote(probability_correct, majority_vote_people, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_half_opinion_average(self, probability_correct, temp_people_num, weight):
        method_utility_list = self.method_utility_list_decideing_by_half_opinion(probability_correct, temp_people_num, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_time_limit_average(self, probability_correct, time_limit, weight):
        method_utility_list = self.method_utility_list_decideing_by_time_limit(probability_correct, time_limit, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_first_person_variance(self, probability_correct, weight):
        method_utility_list = self.method_utility_list_decideing_by_first_person(probability_correct, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    def deciding_by_majority_vote_variance(self, probability_correct, majority_vote_people, weight):
        method_utility_list = self.method_utility_list_decideing_by_majority_vote(probability_correct, majority_vote_people, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    def deciding_by_half_opinion_variance(self, probability_correct, temp_people_num, weight):
        method_utility_list = self.method_utility_list_decideing_by_half_opinion(probability_correct, temp_people_num, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    def deciding_by_time_limit_variance(self, probability_correct, time_limit, weight):
        method_utility_list = self.method_utility_list_decideing_by_time_limit(probability_correct, time_limit, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    # 個人の正解率を一様分布で表現する
    # s_probability ~ s_probability + t_probabilityまでの一様分布の個人の正解率
    def method_utility_list_decideing_by_first_person_with_uniform_distribution(self, s_probability, t_probability, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n] # ポアソン分布したがって来る人数
            probability_correct = (np.random.rand() * t_probability + s_probability) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                method_utility += probability_correct - weight * (float(i) / self.collecting_deadline)
                break
            method_utility_list.append(method_utility)
        return method_utility_list

    def method_utility_list_decideing_by_majority_vote_with_uniform_distribution(self, s_probability, t_probability, majority_vote_people, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            probability_correct = (np.random.rand() * t_probability + s_probability) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            if people_num < majority_vote_people: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count += 1
                if people_count == majority_vote_people:
                    method_utility += (1 - self.relative_error_by_majority_vote(people_count, probability_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
            method_utility_list.append(method_utility)
        return method_utility_list

    def method_utility_list_decideing_by_half_opinion_with_uniform_distribution(self, s_probability, t_probability, temp_people_num, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            probability_correct = (np.random.rand() * t_probability + s_probability) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            people_count_list = []
            if people_num < temp_people_num: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count_list.append(i)
                people_count += 1
                if people_count == temp_people_num:
                    probability_correct_list = self.probability_correct_list_by_half_opinion(self.half_num(temp_people_num), probability_correct)
                    sum_probability = sum(probability_correct_list)
                    average_index = 0
                    for index in range(len(probability_correct_list)):
                        average_index += people_count_list[self.half_num(temp_people_num) - 1 + index] * (probability_correct_list[index] / sum_probability)
                    method_utility = sum_probability - weight * (float(average_index) / self.collecting_deadline)
                    break
            method_utility_list.append(method_utility)
        return method_utility_list

    def method_utility_list_decideing_by_time_limit_with_uniform_distribution(self, s_probability, t_probability, time_limit, weight):
        method_utility_list = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            probability_correct = (np.random.rand() * t_probability + s_probability) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            for i in range(len(when_people_come)):
                if i >= time_limit and people_count >= 1:
                    method_utility = (1 - self.relative_error_by_majority_vote(people_count, probability_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
                if when_people_come[i] == 0: continue
                people_count += 1
            method_utility_list.append(method_utility)
        return method_utility_list

    def deciding_by_first_person_average_with_uniform_distribution(self, s_probability, t_probability, weight):
        method_utility_list = self.method_utility_list_decideing_by_first_person_with_uniform_distribution(s_probability, t_probability, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_majority_vote_average_with_uniform_distribution(self, s_probability, t_probability, majority_vote_people, weight):
        method_utility_list = self.method_utility_list_decideing_by_majority_vote_with_uniform_distribution(s_probability, t_probability, majority_vote_people, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_half_opinion_average_with_uniform_distribution(self, s_probability, t_probability, temp_people_num, weight):
        method_utility_list = self.method_utility_list_decideing_by_half_opinion_with_uniform_distribution(s_probability, t_probability, temp_people_num, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_time_limit_average_with_uniform_distribution(self, s_probability, t_probability, time_limit, weight):
        method_utility_list = self.method_utility_list_decideing_by_time_limit_with_uniform_distribution(s_probability, t_probability, time_limit, weight)
        average_method_utility = np.mean(method_utility_list)
        return average_method_utility

    def deciding_by_first_person_variance_with_uniform_distribution(self, s_probability, t_probability, weight):
        method_utility_list = self.method_utility_list_decideing_by_first_person_with_uniform_distribution(s_probability, t_probability, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    def deciding_by_majority_vote_variance_with_uniform_distribution(self, s_probability, t_probability, majority_vote_people, weight):
        method_utility_list = self.method_utility_list_decideing_by_majority_vote_with_uniform_distribution(s_probability, t_probability, majority_vote_people, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    def deciding_by_half_opinion_variance_with_uniform_distribution(self, s_probability, t_probability, temp_people_num, weight):
        method_utility_list = self.method_utility_list_decideing_by_half_opinion_with_uniform_distribution(s_probability, t_probability, temp_people_num, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    def deciding_by_time_limit_variance_with_uniform_distribution(self, s_probability, t_probability, time_limit, weight):
        method_utility_list = self.method_utility_list_decideing_by_time_limit_with_uniform_distribution(s_probability, t_probability, time_limit, weight)
        variance_method_utility = np.var(method_utility_list)
        return variance_method_utility

    # ------------------以下は理論に基づいた実装を行う------------------

    # 1,準備
    # Poisson過程
    # 単位時間あたりの到着数 λ
    # 時刻tまでにn人が到着する確率
    def poisson_probability(self, n, t, lambda_poisson):
        return math.e**(-lambda_poisson * t) * (lambda_poisson * t)**n / math.factorial(n)

    # Poisson過程
    # 累積確率
    def cumulative_poisson_probability(self, n, t, lambda_poisson):
        cumulative_probability = 0
        for i in range(0, n + 1):
            cumulative_probability += math.e**(-lambda_poisson * t) * (lambda_poisson * t)**i / math.factorial(i)
        return cumulative_probability

    # Gamma分布
    # 時刻tにn人目が到着する確率
    def gamma_probability(self, n, t, lambda_poisson):
        return lambda_poisson**n * t**(n - 1) * math.e**(-lambda_poisson * t) / math.factorial(n - 1)

    # Gamma分布
    # 累積確率
    def cumulative_gamma_probability(self, n, T, lambda_poisson):
        cumulative_probability, abserr = integrate.quad(lambda t: self.gamma_probability(n, t, lambda_poisson), 0, T)
        return cumulative_probability

    # 時刻Tまでにn人現われるときに，時刻t(≤ T)にn人目が到着する(時刻tからTの間には一人も現われない)確率g(n,t,T)
    def g(self, n, t, T, lambda_poisson):
        return lambda_poisson**n * t**(n - 1) * math.e**(-lambda_poisson * T) / math.factorial(n - 1)

    # 多数決による判定精度
    # n人で多数決を行う場合の判定精度をacc(n)で表す
    # 個人の判定精度をpとする
    def acc_odd(self, n, p): # nが奇数2i-1のとき
        i = int((n + 1) / 2)
        acc = 0
        for j in range(i):
            acc += scm.comb(2 * i - 1, j) * p**(2 * i - 1 - j) * (1 - p)**j
        return acc

    def acc_even(self, n, p): # nが偶数2iのとき
        i = int(n / 2)
        acc = 0
        for j in range(i):
            acc += scm.comb(2 * i, j) * p**(2 * i - j) * (1 - p)**j
        acc += scm.comb(2 * i, i) * p**i * (1 - p)**i / 2
        return acc

    def acc(self, n, p):
        if n % 2 == 1:
            return self.acc_odd(n, p)
        else:
            return self.acc_even(n, p)

    # 2,単純な意見集約法

    # 2.1,時刻優先意見集約法
    # 時刻tまで待って多数決を行う
    # 効用を予測精度と所要時間の差で表す
    def time_priority_method(self, t, w, p, lambda_poisson):
        if t == 0: return 0
        utility = 0
        for i in range(1, 2 * lambda_poisson * t, 1):
                utility += self.poisson_probability(i, t, lambda_poisson) * self.acc(i, p)
        utility -= w * t
        return utility

    # 増減を調べる
    def inc_and_dec_time_priority_method(self, w, p, lambda_poisson):
        for t in range(1, 1000):
            diff = self.time_priority_method(t + 1, w, p, lambda_poisson) - self.time_priority_method(t, w, p, lambda_poisson)
            if diff < 0: return t

    # 2.2, 投票数優先意見集約法
    # n人集まるまで待って多数決を行う
    # 効用を予測精度と所要時間の差で表す
    def poll_priority_method(self, n, w, p, lambda_poisson):
        if n == 0: return 0
        utility = 0
        utility += self.acc(n, p)
        # 積分を行う
        value, abserr = integrate.quad(lambda t: w * t * self.gamma_probability(n, t, lambda_poisson), 0, 1000)
        utility -= value
        return utility

    # 増減を調べる
    def inc_and_dec_poll_priority_method(self, w, p, lambda_poisson):
        for n in range(1, 1000):
            diff = self.poll_priority_method(2 * n + 1, w, p, lambda_poisson) - self.poll_priority_method(2 * n - 1, w, p, lambda_poisson)
            if diff < 0: return 2 * n - 1

    # 2.3, 得票数優先意見集約法
    # 先にk票集まった案に決定する
    # 効用を予測精度と所要時間の差で表す
    def vote_priority_method(self, k, w, p, lambda_poisson):
        if k == 0: return 0
        utility = 0
        for j in range(k, 2 * k):
            temp_probability = scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p
            # 積分を行う
            value, abserr = integrate.quad(lambda t: w * t * self.gamma_probability(j, t, lambda_poisson), 0, 1000)
            utility += temp_probability * (1 - value)
        return utility

    # 増減を調べる
    def inc_and_dec_vote_priority_method(self, w, p, lambda_poisson):
        for k in range(1, 1000):
            diff = self.vote_priority_method(k + 1, w, p, lambda_poisson) - self.vote_priority_method(k, w, p, lambda_poisson)
            if diff < 0: return k

    # 3, 組み合わせ意見集約法
    # 方法1, 時刻T1まで待つ
    # 方法2, 投票者数がnに達すれば判定し終了、達しなければT1まで待つ
    # 方法3, 時刻T2(=< T1)までに投票者数がnに達すれば判定し終了、達しなければT1まで待つ(T2 = T1とすれば方法2と方法3は同じ)
    # 方法4, 得票者数がkに達すれば判定し終了、達しなければT1まで待つ
    # 方法5, 時間T2(=< T1)までに得票者数がkに達すれば判定を終了し、達しなければT1まで待つ (T2 = T1とすれば方法4と方法5は同じ)

    # 方法1(時刻優先意見集約法と同じ) 時刻T1まで待つ
    def method1(self, t, w, p, lambda_poisson):
        return self.time_priority_method(t, w, p, lambda_poisson)

    # 増減を調べる
    def inc_and_dec_method1(self, w, p, lambda_poisson):
        return self.inc_and_dec_time_priority_method(w, p, lambda_poisson)

    # 方法2 投票者数がnに達すれば判定し終了、達しなければT1まで待つ
    def method2(self, T1, n, w, p, lambda_poisson):
        if n == 0: return 0
        utility = 0
        for i in range(0, n):
            utility += self.poisson_probability(i, T1, lambda_poisson) * (self.acc(i, p) - w * T1)
        # 積分を行う
        value, abserr = integrate.quad(lambda t: (self.acc(n, p) - w * t) * self.gamma_probability(n, t, lambda_poisson), 0, T1)
        utility += value
        return utility

    # 増減を調べる
    def inc_and_dec_method2(self, T1, w, p, lambda_poisson):
        for n in range(1, 50):
            diff = self.method2(T1, 2 * n + 1, w, p, lambda_poisson) - self.method2(T1, 2 * n - 1, w, p, lambda_poisson)
            if diff < 0:
                return 2 * n - 1

    # 方法3 時刻T2(=< T1)までに投票者数がnに達すれば判定し終了、達しなければT1まで待つ(T2 = T1とすれば方法2と方法3は同じ)
    def method3(self, T1, T2, n, w, p, lambda_poisson):
        if n == 0: return 0
        utility = 0
        # T1までにn人集まらないとき
        for i in range(0, n):
            utility += self.poisson_probability(i, T1, lambda_poisson) * (self.acc(i, p) - w * T1)
        # T1までにn人集まるがT2までにはn人集まらないとき
        for i in range(n, 100):
            utility += (self.poisson_probability(i, T1, lambda_poisson) - self.poisson_probability(i, T2, lambda_poisson)) * (self.acc(i, p) - w * T1)
        # 積分を行う
        # T2までにn人集まるとき
        value, abserr = integrate.quad(lambda t: (self.acc(n, p) - w * t) * self.gamma_probability(n, t, lambda_poisson), 0, T2)
        utility += value
        return utility


    # 増減を調べる
    def inc_and_dec_method3(self, T1, T2, w, p, lambda_poisson):
        for n in range(1, 50):
            diff = self.method3(T1, T2, 2 * n + 1, w, p, lambda_poisson) - self.method3(T1, T2, 2 * n - 1, w, p, lambda_poisson)
            if diff < 0:
                return 2 * n - 1

    # 方法4 得票者数がkに達すれば判定し終了、達しなければT1まで待つ
    def method4(self, T1, k, w, p, lambda_poisson):
        if k == 0: return 0
        utility = 0
        for i in range(0, k):
            for j in range(i, 2 * i):
                utility += self.poisson_probability(j, T1, lambda_poisson) * (scm.comb(j - 1, j - i) * p**(i - 1) * (1 - p)**(j - i) * p) * (1 - w * T1)
        # ----被積分関数を定義----
        def integrand_for_method4(t):
            integrand = 0
            for j in range(k, 2 * k):
                integrand += (scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p) * (1 - w * t) * self.gamma_probability(j, t, lambda_poisson)
            return integrand
        # --------終わり--------
        #積分を行う
        value, abserr = integrate.quad(integrand_for_method4, 0, T1)
        utility += value
        return utility

    # 方法5 時間T2(=< T1)までに得票者数がkに達すれば判定を終了し、達しなければT1まで待つ (T2 = T1とすれば方法4と方法5は同じ)
    def method5(self, T1, T2, k, w, p, lambda_poisson):
        if k == 0: return 0
        utility = 0
        # T1までにk票集まらないとき
        for i in range(0, k):
            for j in range(i, 2 * i):
                utility += self.poisson_probability(j, T1, lambda_poisson) * (scm.comb(j - 1, j - i) * p**(i - 1) * (1 - p)**(j - i) * p) * (1 - w * T1)
        # T1までにk票集まるがT2までにはk票集まらないとき
        for i in range(k, 100):
            for j in range(i, 2 * i):
                utility += (self.poisson_probability(i, T1, lambda_poisson) - self.poisson_probability(i, T2, lambda_poisson)) * (scm.comb(j - 1, j - i) * p**(i - 1) * (1 - p)**(j - i) * p) * (1 - w * T1)
        # 積分を行う
        # T2までにk票集まるとき
        # ----被積分関数を定義----
        def integrand_for_method5(t):
            integrand = 0
            for j in range(k, 2 * k):
                integrand += (scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p) * (1 - w * t) * self.gamma_probability(j, t, lambda_poisson)
            return integrand
        # --------終わり--------
        value, abserr = integrate.quad(integrand_for_method5, 0, T2)
        utility += value
        return utility
