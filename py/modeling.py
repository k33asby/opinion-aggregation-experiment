class Modeling:

    def __init__(self, people_num, possibility_correct, lambda_poisson, repeat, weight):
        self.people_num = people_num
        self.people_half = self.half_num(people_num)
        self.possibility_correct = possibility_correct
        self.lambda_poisson = lambda_poisson
        self.correcting_deadline = lambda_poisson * 2
        self.repeat = repeat
        self.poisson = np.random.poisson(lambda_poisson, 1000000)
        self.weight = float(weight)

    def half_num(self,num):
        return math.ceil(float(num) / 2)

    def simulate_when_people_come_list(self, people_num):
        when_people_come = [0] * self.correcting_deadline
        for t in range(people_num):
            when_people_come[t] = 1
        random.shuffle(when_people_come)
        return when_people_come

    def deciding_by_first_person_with_poisson(self, possibility_correct):
        temp_method_utility = 0
        for n in range(self.repeat):
            people_num = self.poisson[n] # ポアソン分布したがって来る人数
            when_people_come = self.simulate_when_people_come_list(people_num)
            method_utility = 0
            for i in range(len(when_people_come)):
                if when_people_come[i] == 0:
                    continue
                else:
                    method_utility += possibility_correct - self.weight * (float(i) / self.correcting_deadline)
                    break
            temp_method_utility += method_utility
        average_method_utility = temp_method_utility / self.repeat
        return average_method_utility

    def test(self):
            s = np.random.poisson(50, 10000000)
            print(s[9000000])
            count, bins, ignored = plt.hist(s, 14, normed=True)
            plt.show()
