class Modeling:

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

    def possibility_correct_by_majority_vote(self, people_num, possibility_correct):
        return (1 - self.relative_error_by_majority_vote(people_num, possibility_correct))

    def relative_error_by_majority_vote(self, people_num, possibility_correct):
        half_num = self.half_num(people_num)
        relative_error = 0
        for t in range(half_num):
            relative_error += (possibility_correct**t) * ((1 - possibility_correct)**(people_num - t)) * scm.comb(people_num, t)
        return relative_error

    def possibility_correct_array_by_half_opinion(self, finish_num, possibility_correct):
        possibility_correct_arr = []
        for t in range(finish_num):
            possibility_correct_arr.append((possibility_correct**finish_num) * ((1 - possibility_correct)**t) * scm.comb(finish_num - 1 + t, t))
        return possibility_correct_arr

    def relative_error_array_by_half_opinion(self, finish_num, possibility_correct):
        relative_error = []
        for t in range(finish_num):
            relative_error.append(((1 - possibility_correct)**finish_num) * (possibility_correct**t) * scm.comb(finish_num - 1 + t, t))
        return relative_error

    def deciding_by_first_person_with_poisson(self, possibility_correct, weight):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n] # ポアソン分布したがって来る人数
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                method_utility += possibility_correct - weight * (float(i) / self.collecting_deadline)
                break
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def deciding_by_majority_vote_with_poisson(self, possibility_correct, majority_vote_people, weight):
        temp_method_utility = 0
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
                    method_utility +=  self.possibility_correct_by_majority_vote(people_count, possibility_correct) - weight * (float(i) / self.collecting_deadline)
                    break
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def deciding_by_half_opinion_with_poisson(self, possibility_correct, temp_people_num, weight):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            people_count_arr = []
            if people_num < temp_people_num: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count_arr.append(i)
                people_count += 1
                if people_count == temp_people_num:
                    possibility_correct_arr = self.possibility_correct_array_by_half_opinion(self.half_num(temp_people_num), possibility_correct)
                    sum_possibility = sum(possibility_correct_arr)
                    average_index = 0
                    for index in range(len(possibility_correct_arr)):
                        average_index += people_count_arr[self.half_num(temp_people_num) - 1 + index] * (possibility_correct_arr[index] / sum_possibility)
                    method_utility = sum_possibility - weight * (float(average_index) / self.collecting_deadline)
                    break
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def deciding_by_time_limit_with_poisson(self, possibility_correct, time_limit, weight):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            for i in range(len(when_people_come)):
                if i >= time_limit and people_count >= 1:
                    method_utility = (1 - self.relative_error_by_majority_vote(people_count, possibility_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
                if when_people_come[i] == 0: continue
                people_count += 1
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def deciding_by_first_person_with_poisson_for_variance(self, possibility_correct, weight):
        temp_method_utility = []
        for n in range(self.repeat):
            people_num = self.poisson[n] # ポアソン分布したがって来る人数
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                method_utility += possibility_correct - weight * (float(i) / self.collecting_deadline)
                break
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility

    def deciding_by_majority_vote_with_poisson_for_variance(self, possibility_correct, majority_vote_people, weight):
        temp_method_utility = []
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
                    method_utility += (1 - self.relative_error_by_majority_vote(people_count, possibility_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility

    def deciding_by_half_opinion_with_poisson_for_variance(self, possibility_correct, temp_people_num, weight):
        temp_method_utility = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            people_count_arr = []
            if people_num < temp_people_num: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count_arr.append(i)
                people_count += 1
                if people_count == temp_people_num:
                    possibility_correct_arr = self.possibility_correct_array_by_half_opinion(self.half_num(temp_people_num), possibility_correct)
                    sum_possibility = sum(possibility_correct_arr)
                    average_index = 0
                    for index in range(len(possibility_correct_arr)):
                        average_index += people_count_arr[self.half_num(temp_people_num) - 1 + index] * (possibility_correct_arr[index] / sum_possibility)
                    method_utility = sum_possibility - weight * (float(average_index) / self.collecting_deadline)
                    break
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility

    def deciding_by_time_limit_with_poisson_for_variance(self, possibility_correct, time_limit, weight):
        temp_method_utility = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            for i in range(len(when_people_come)):
                if i >= time_limit and people_count >= 1:
                    method_utility = (1 - self.relative_error_by_majority_vote(people_count, possibility_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
                if when_people_come[i] == 0: continue
                people_count += 1
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility

    # -----以上はRubyと同じ実装-----
    # -----ここからは新しい実装-----
    # 個人の正解率を一様分布で表現する
    # s_possibilityからs_possibility + t_possibilityまでの一様分布の個人の正解率
    def deciding_by_first_person_with_uniform_distribution(self, s_possibility, t_possibility, weight):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n] # ポアソン分布したがって来る人数
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                method_utility += possibility_correct - weight * (float(i) / self.collecting_deadline)
                break
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def deciding_by_majority_vote_with_uniform_distribution(self, s_possibility, t_possibility, majority_vote_people, weight):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n]
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            if people_num < majority_vote_people: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count += 1
                if people_count == majority_vote_people:
                    method_utility += (1 - self.relative_error_by_majority_vote(people_count, possibility_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def deciding_by_half_opinion_with_uniform_distribution(self, s_possibility, t_possibility, temp_people_num, weight):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n]
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            people_count_arr = []
            if people_num < temp_people_num: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count_arr.append(i)
                people_count += 1
                if people_count == temp_people_num:
                    possibility_correct_arr = self.possibility_correct_array_by_half_opinion(self.half_num(temp_people_num), possibility_correct)
                    sum_possibility = sum(possibility_correct_arr)
                    average_index = 0
                    for index in range(len(possibility_correct_arr)):
                        average_index += people_count_arr[self.half_num(temp_people_num) - 1 + index] * (possibility_correct_arr[index] / sum_possibility)
                    method_utility = sum_possibility - weight * (float(average_index) / self.collecting_deadline)
                    break
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def deciding_by_time_limit_with_uniform_distribution(self, s_possibility, t_possibility, time_limit, weight):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n]
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            for i in range(len(when_people_come)):
                if i >= time_limit and people_count >= 1:
                    method_utility = (1 - self.relative_error_by_majority_vote(people_count, possibility_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
                if when_people_come[i] == 0: continue
                people_count += 1
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    # 分散
    def deciding_by_first_person_with_uniform_distribution_for_variance(self, s_possibility, t_possibility, weight):
        temp_method_utility = []
        for n in range(self.repeat):
            people_num = self.poisson[n] # ポアソン分布したがって来る人数
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                method_utility += possibility_correct - weight * (float(i) / self.collecting_deadline)
                break
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility

    def deciding_by_majority_vote_with_uniform_distribution_for_variance(self, s_possibility, t_possibility, majority_vote_people, weight):
        temp_method_utility = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            if people_num < majority_vote_people: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count += 1
                if people_count == majority_vote_people:
                    method_utility += (1 - self.relative_error_by_majority_vote(people_count, possibility_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility

    def deciding_by_half_opinion_with_uniform_distribution_for_variance(self, s_possibility, t_possibility, temp_people_num, weight):
        temp_method_utility = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            people_count_arr = []
            if people_num < temp_people_num: continue
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0: continue
                people_count_arr.append(i)
                people_count += 1
                if people_count == temp_people_num:
                    possibility_correct_arr = self.possibility_correct_array_by_half_opinion(self.half_num(temp_people_num), possibility_correct)
                    sum_possibility = sum(possibility_correct_arr)
                    average_index = 0
                    for index in range(len(possibility_correct_arr)):
                        average_index += people_count_arr[self.half_num(temp_people_num) - 1 + index] * (possibility_correct_arr[index] / sum_possibility)
                    method_utility = sum_possibility - weight * (float(average_index) / self.collecting_deadline)
                    break
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility

    def deciding_by_time_limit_with_uniform_distribution_for_variance(self, s_possibility, t_possibility, time_limit, weight):
        temp_method_utility = []
        for n in range(self.repeat):
            people_num = self.poisson[n]
            possibility_correct = (np.random.rand() * t_possibility + s_possibility) / 100
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            people_count = 0
            for i in range(len(when_people_come)):
                if i >= time_limit and people_count >= 1:
                    method_utility = (1 - self.relative_error_by_majority_vote(people_count, possibility_correct)) - weight * (float(i) / self.collecting_deadline)
                    break
                if when_people_come[i] == 0: continue
                people_count += 1
            temp_method_utility.append(method_utility)
        variance_method_utility = np.var(temp_method_utility)
        return variance_method_utility


    # ベースライン手法
    # 今X人いる 誤差をε以下にしたい
    # 存在する方法のなかから最善のものを選択してそれがX人を下回るならそれを採用する
    # 存在する方法
    # *個人の意見
    # *多数決
    # *自信による重み付け
    # *自信の最大のもの
    # *SP
    # Xを超えてしまったなら、εを大きくしてこれを繰り返す
    def baseline_method(self, people_num, relative_error):
        method_dict = {}
        pass
