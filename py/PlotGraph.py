class plotGraph:

    def __init__(self, lambda_poisson, repeat):
        sns.set_style("whitegrid")
        self.model = modeling(lambda_poisson, repeat)

    # 縦軸を誤差率、横軸を個人の正解率
    def plot_error_probability_graph(self, people_num):
        x_axis = np.linspace(50,100,50)
        y_axis_majority_vote = self.model.relative_error_by_majority_vote(people_num, x_axis / 100)
        y_axis_half_opinion = sum(self.model.relative_error_list_by_half_opinion(self.model.half_num(people_num), x_axis / 100))
        plt.hold(True)
        plt.title('error_probability_graph %s people' % people_num)
        plt.xlabel('Possibility of correct')
        plt.ylabel('Relative error')
        plt.plot(x_axis, y_axis_majority_vote, label='Majority vote')
        plt.plot(x_axis, y_axis_half_opinion, label='Half opinion')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 必要になったら実装
    def plot_cost_error_graph(self):
        pass

    # 人数を変えてグラフを重ねる
    # 縦軸を誤差率、横軸を個人の正解率
    def plot_error_probability_graph_by_people_num(self):
        x_axis = np.linspace(50,100,50)
        y_axis_list = []
        for t in range(30):
            y_axis_list.append(self.model.relative_error_by_majority_vote(1 + 2 * t, x_axis / 100))
        plt.hold(True)
        plt.title('Error-probability graph by people number')
        plt.xlabel('Possibility of correct')
        plt.ylabel('Relative error')
        for y_axis in y_axis_list:
            plt.plot(x_axis, y_axis)
        plt.show()

    # 必要になったら実装
    def plot_cost_error_graph_by_probability(self):
        pass

    # ポアソン分布にしたがって効用の平均を求めたグラフ
    # 縦軸を効用、横軸を個人の正解率
    def plot_utility_probability_average_graph(self, majority_vote_people, half_opinion_people, time_limit, weight):
        x_axis = np.linspace(0.5,1.0,50)
        y_axis_dict = {}
        y_axis_dict["First peson"] = [self.model.deciding_by_first_person_average(x, weight) for x in x_axis]
        y_axis_dict["Majority vote"] = [self.model.deciding_by_majority_vote_average(x, majority_vote_people, weight) for x in x_axis]
        y_axis_dict["Half opinion"] = [self.model.deciding_by_half_opinion_average(x, half_opinion_people, weight) for x in x_axis]
        y_axis_dict["Time limit"] = [self.model.deciding_by_time_limit_average(x, time_limit, weight) for x in x_axis]
        plt.hold(True)
        plt.title('Utility-probability graph majority vote people:{0} half opinion people:{1} timelimit:{2} weight:{3}'.format(majority_vote_people, half_opinion_people, time_limit, weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # ポアソン分布にしたがって効用の分散を求めたグラフ
    # 縦軸を効用の分散、横軸を個人の正解率
    def plot_utility_probability_variance_graph(self, majority_vote_people, half_opinion_people, time_limit, weight):
        x_axis = np.linspace(0.5,1.0,50)
        y_axis_dict = {}
        y_axis_dict["First peson"] = [self.model.deciding_by_first_person_variance(x, weight) for x in x_axis]
        y_axis_dict["Majority vote"] = [self.model.deciding_by_majority_vote_variance(x, majority_vote_people, weight) for x in x_axis]
        y_axis_dict["Half opinion"] = [self.model.deciding_by_half_opinion_variance(x, half_opinion_people, weight) for x in x_axis]
        y_axis_dict["Time limit"] = [self.model.deciding_by_time_limit_variance(x, time_limit, weight) for x in x_axis]
        plt.hold(True)
        plt.title('Utility-probability graph majority vote people:{0} half opinion people:{1} timelimit:{2} weight:{3}'.format(majority_vote_people, half_opinion_people, time_limit, weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 重みを0.0,,,1.0と遷移させていったときの効用の平均
    # 縦軸を効用、横軸を重み
    def plot_utility_weight_average_graph(self, probability_correct, majority_vote_people, half_opinion_people, time_limit):
        x_axis = np.linspace(0.0, 1.0, 50)
        y_axis_dict = {}
        y_axis_dict["First peson"] = [self.model.deciding_by_first_person_average(probability_correct, x) for x in x_axis]
        y_axis_dict["Majority vote"] = [self.model.deciding_by_majority_vote_average(probability_correct, majority_vote_people, x) for x in x_axis]
        y_axis_dict["Half opinion"] = [self.model.deciding_by_half_opinion_average(probability_correct, half_opinion_people, x) for x in x_axis]
        y_axis_dict["Time limit"] = [self.model.deciding_by_time_limit_average(probability_correct, time_limit, x) for x in x_axis]
        plt.hold(True)
        plt.title('Utility-weight graph majority vote people:{0} half opinion people:{1} timelimit:{2} probability_correct:{3}'.format(majority_vote_people, half_opinion_people, time_limit, probability_correct))
        plt.xlabel('weight')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 重みを0.0,,,1.0と遷移させていったときの効用の分散
    # 縦軸を効用、横軸を重み
    def plot_utility_weight_variance_graph(self, probability_correct, majority_vote_people, half_opinion_people, time_limit):
        x_axis = np.linspace(0.0, 1.0, 50)
        y_axis_dict = {}
        y_axis_dict["First peson"] = [self.model.deciding_by_first_person_variance(probability_correct, x) for x in x_axis]
        y_axis_dict["Majority vote"] = [self.model.deciding_by_majority_vote_variance(probability_correct, majority_vote_people, x) for x in x_axis]
        y_axis_dict["Half opinion"] = [self.model.deciding_by_half_opinion_variance(probability_correct, half_opinion_people, x) for x in x_axis]
        y_axis_dict["Time limit"] = [self.model.deciding_by_time_limit_variance(probability_correct, time_limit, x) for x in x_axis]
        plt.hold(True)
        plt.title('Utility-weight graph majority vote people:{0} half opinion people:{1} timelimit:{2} probability_correct:{3}'.format(majority_vote_people, half_opinion_people, time_limit, probability_correct))
        plt.xlabel('weight')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 多数決を行う人数や時間制限どれくらいが最適であるか
    # ポアソン分布の平均にも依存すると考えられる
    # 平均
    # 縦軸を効用、横軸を個人の正解率
    def plot_utility_probability_average_graph_for_single_method(self, weight):
        x_axis = np.linspace(0.5, 1.0, 50)
        # 最初の一人
        y_axis_dict = {}
        y_axis_dict["First person"] = [self.model.deciding_by_first_person_average(x, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 多数決
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Majority vote" + str(2 * t + 1)] = [self.model.deciding_by_majority_vote_average(x, 2 * t + 1, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 半数
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Half opinion" + str(2 * t + 1)] = [self.model.deciding_by_half_opinion_average(x, 2 * t + 1, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 時間打ち切り
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Time limit" + str(4 * t + 1)] = [self.model.deciding_by_time_limit_average(x, 4 * t + 1, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 多数決を行う人数や時間制限どれくらいが最適であるか
    # ポアソン分布の平均にも依存すると考えられる
    # 分散
    # 縦軸を効用、横軸を個人の正解率
    def plot_utility_probability_variance_graph_for_single_method(self, weight):
        x_axis = np.linspace(0.5, 1.0, 50)
        # 最初の一人
        y_axis_dict = {}
        y_axis_dict["First person"] = [self.model.deciding_by_first_person_variance(x, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 多数決
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Majority vote" + str(2 * t + 1)] = [self.model.deciding_by_majority_vote_variance(x, 2 * t + 1, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 半数
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Half opinion" + str(2 * t + 1)] = [self.model.deciding_by_half_opinion_variance(x, 2 * t + 1, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 時間打ち切り
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Time limit" + str(4 * t + 1)] = [self.model.deciding_by_time_limit_variance(x, 4 * t + 1, weight) for x in x_axis]
        plt.title('Utility-probability graph weight: {}'.format(weight))
        plt.xlabel('Possibility correct')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()


    # 個人の正答率を一様分布で表したもの
    # 縦軸を効用、横軸を重み
    # 平均
    def plot_utility_weight_average_graph_with_uniform_distribution(self, s_probability, t_probability, majority_vote_people, half_opinion_people, time_limit):
        x_axis = np.linspace(0.0, 1.0, 20)
        y_axis_dict = {}
        y_axis_dict["First peson"] = [self.model.deciding_by_first_person_average_with_uniform_distribution(s_probability, t_probability, x) for x in x_axis]
        y_axis_dict["Majority vote"] = [self.model.deciding_by_majority_vote_average_with_uniform_distribution(s_probability, t_probability, majority_vote_people, x) for x in x_axis]
        y_axis_dict["Half opinion"] = [self.model.deciding_by_half_opinion_average_with_uniform_distribution(s_probability, t_probability, half_opinion_people, x) for x in x_axis]
        y_axis_dict["Time limit"] = [self.model.deciding_by_time_limit_average_with_uniform_distribution(s_probability, t_probability, time_limit, x) for x in x_axis]
        plt.hold(True)
        plt.title('Utility-weight graph uniform distribution majority vote people:{0} halp opinion people: {1} timelimit:{2} probability_correct:{3}~{4}'.format(majority_vote_people, half_opinion_people, time_limit, s_probability, s_probability + t_probability ))
        plt.xlabel('weight')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 個人の正答率を一様分布で表したもの
    # 縦軸を効用、横軸を重み
    # 分散
    def plot_utility_weight_variance_graph_with_uniform_distribution(self, s_probability, t_probability, majority_vote_people, half_opinion_people, time_limit):
        x_axis = np.linspace(0.0, 1.0, 20)
        y_axis_dict = {}
        y_axis_dict["First peson"] = [self.model.deciding_by_first_person_variance_with_uniform_distribution(s_probability, t_probability, x) for x in x_axis]
        y_axis_dict["Majority vote"] = [self.model.deciding_by_majority_vote_variance_with_uniform_distribution(s_probability, t_probability, majority_vote_people, x) for x in x_axis]
        y_axis_dict["Half opinion"] = [self.model.deciding_by_half_opinion_variance_with_uniform_distribution(s_probability, t_probability, half_opinion_people, x) for x in x_axis]
        y_axis_dict["Time limit"] = [self.model.deciding_by_time_limit_variance_with_uniform_distribution(s_probability, t_probability, time_limit, x) for x in x_axis]
        plt.hold(True)
        plt.title('Utility-weight graph uniform distribution majority vote people:{0} halp opinion people: {1} timelimit:{2} probability_correct:{3}~{4}'.format(majority_vote_people, half_opinion_people, time_limit, s_probability, s_probability + t_probability ))
        plt.xlabel('weight')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 多数決を行う人数や時間制限どれくらいが最適であるか
    # ポアソン分布の平均にも依存すると考えられる
    # 確率を一様分布として扱う
    # 平均
    # 縦軸を効用の平均、横軸を重み
    def plot_utility_weight_average_graph_with_uniform_distribution_for_single_method(self, s_probability, t_probability):
        x_axis = np.linspace(0.0, 1.0, 20)
        # 最初の一人
        y_axis_dict = {}
        y_axis_dict["First person"] = [self.model.deciding_by_first_person_average_with_uniform_distribution(s_probability, t_probability, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 多数決
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Majority vote" + str(2 * t + 1)] = [self.model.deciding_by_majority_vote_average_with_uniform_distribution(s_probability, t_probability, 2 * t + 1, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 半数
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Half opinion" + str(2 * t + 1)] = [self.model.deciding_by_half_opinion_average_with_uniform_distribution(s_probability, t_probability, 2 * t + 1, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 時間打ち切り
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Time limit" + str(4 * t + 1)] = [self.model.deciding_by_time_limit_average_with_uniform_distribution(s_probability, t_probability, 4 * t + 1, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Utility')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # 多数決を行う人数や時間制限どれくらいが最適であるか
    # ポアソン分布の平均にも依存すると考えられる
    # 確率を一様分布として扱う
    # 分散
    # 縦軸を効用の分散、横軸を重み
    def plot_utility_weight_variance_graph_with_uniform_distribution_for_single_method(self, s_probability, t_probability):
        x_axis = np.linspace(0.0, 1.0, 20)
        # 最初の一人
        y_axis_dict = {}
        y_axis_dict["First person"] = [self.model.deciding_by_first_person_variance_with_uniform_distribution(s_probability, t_probability, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 多数決
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Majority vote" + str(2 * t + 1)] = [self.model.deciding_by_majority_vote_variance_with_uniform_distribution(s_probability, t_probability, 2 * t + 1, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 半数
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Half opinion" + str(2 * t + 1)] = [self.model.deciding_by_half_opinion_variance_with_uniform_distribution(s_probability, t_probability, 2 * t + 1, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()
        # 時間打ち切り
        y_axis_dict = {}
        for t in range(10):
            y_axis_dict["Time limit" + str(4 * t + 1)] = [self.model.deciding_by_time_limit_variance_with_uniform_distribution(s_probability, t_probability, 4 * t + 1, x) for x in x_axis]
        plt.title('Utility-probability graph probability_correct:{0}~{1}'.format(s_probability, s_probability + t_probability))
        plt.xlabel('weight')
        plt.ylabel('Variance')
        for key, value in y_axis_dict.iteritems():
            plt.plot(x_axis, value, label = key)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

    # ---------------------以下は理論に基づいた実装に対するグラフメソッド---------------------
    def plot_poisson(self, time, lambda_poisson):
        x_axis = np.linspace(0, 2 * time * lambda_poisson, 2 * time * lambda_poisson + 1)
        y_axis = []
        for x in x_axis:
            y_axis.append(self.model.poisson_probability(x, time, lambda_poisson))
        plt.title('poisson time: {0} lambda: {1}'.format(time, lambda_poisson))
        plt.xlabel('people')
        plt.ylabel('probability')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_cumulative_poisson(self, time, lambda_poisson):
        x_axis = np.linspace(0, 2 * time * lambda_poisson, 2 * time * lambda_poisson + 1)
        y_axis = []
        for x in x_axis:
            y_axis.append(self.model.cumulative_poisson_probability(int(x), time, lambda_poisson))
        plt.title('cumulative poisson time: {0} lambda: {1}'.format(time, lambda_poisson))
        plt.xlabel('people')
        plt.ylabel('probability')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_gamma(self, people, lambda_poisson):
        x_axis = np.linspace(0, 2 * people / lambda_poisson , 2 * people / lambda_poisson + 1)
        y_axis = []
        for x in x_axis:
            y_axis.append(self.model.gamma_probability(people, x, lambda_poisson))
        plt.title('gamma people: {0} lambda: {1}'.format(people, lambda_poisson))
        plt.xlabel('time')
        plt.ylabel('probability')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_cumulative_gamma(self, people, lambda_poisson):
        x_axis = np.linspace(0, 2 * people / lambda_poisson , 2 * people / lambda_poisson + 1)
        y_axis = []
        for x in x_axis:
            y_axis.append(self.model.cumulative_gamma_probability(people, x, lambda_poisson))
        plt.title('cumulative gamma people: {0} lambda: {1}'.format(people, lambda_poisson))
        plt.xlabel('time')
        plt.ylabel('probability')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_g(self, m, n, T, lambda_poisson):
        x_axis = np.linspace(0, T, T + 1)
        y_axis = []
        for x in x_axis:
            y_axis.append(self.model.g(m, n, x, T, lambda_poisson))
        plt.title("g m: {0} n: {1} T:{2} lambda: {3}".format(m, n, T, lambda_poisson))
        plt.xlabel('time')
        plt.ylabel('probability')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_time_priority(self, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.time_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('time priority method weight: {0} person_probability: {1}'.format(w, p))
        plt.xlabel('time')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_poll_priority(self, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.poll_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('poll priority method weight: {0} person_probability: {1}'.format(w, p))
        plt.xlabel('poll people')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_vote_priority(self, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.vote_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('vote priority method weight: {0} person_probability: {1}'.format(w, p))
        plt.xlabel('require vote people')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_method1(self, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.time_priority_method(int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('method1 weight: {0} person_probability: {1}'.format(w, p))
        plt.xlabel('time')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_method2(self, T1, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.method2(T1,int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('method2 T1: {0} weight: {1} person_probability: {2}'.format(T1, w, p))
        plt.xlabel('poll people')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_method3(self, T1, T2, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.method3(T1, T2, int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('method3 T1: {0} T2: {1} weight: {2} person_probability: {3}'.format(T1, T2, w, p))
        plt.xlabel('poll people')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_method4(self, T1, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.method4(T1,int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('method4 T1: {0} weight: {1} person_probability: {2}'.format(T1, w, p))
        plt.xlabel('require vote people')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()

    def plot_method5(self, T1, T2, w, p, lambda_poisson):
        x_axis = np.linspace(0, 50, 51)
        y_axis = [self.model.method5(T1, T2, int(x), w, p, lambda_poisson) for x in x_axis]
        plt.title('method5 T1: {0} T2: {1} weight: {2} person_probability: {3}'.format(T1, T2, w, p))
        plt.xlabel('poll people')
        plt.ylabel('utility')
        plt.plot(x_axis, y_axis)
        plt.show()
