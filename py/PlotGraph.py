class PlotGraph:

    def __init__(self, lambda_poisson, repeat, weight, people_num, possibility_correct):
        self.model = Modeling(lambda_poisson, repeat, weight)
        self.people_num = people_num
        self.possibility_correct = possibility_correct

    def plot_error_possibility_graph(self):
        x_axis = np.linspace(50,100,50)
        y_axis_majority_vote = self.model.relative_error_by_majority_vote(self.people_num, x_axis / 100)
        y_axis_half_opinion = sum(self.model.relative_error_array_by_half_opinion(self.model.half_num(self.people_num), x_axis / 100))
        plt.hold(True)
        plt.title('error_possibility_graph %s people' % self.people_num)
        plt.xlabel('Possibility of correct')
        plt.ylabel('Relative error')
        plt.plot(x_axis, y_axis_majority_vote, label='Majority vote')
        plt.plot(x_axis, y_axis_half_opinion, label='Half opinion')
        plt.show()

    # 必要になったら実装
    def plot_cost_error_graph(self):
        pass

    def plot_error_possibility_graph_by_people_num(self):
        x_axis = np.linspace(50,100,50)
        y_axis_arr = []
        for t in range(30):
            y_axis_arr.append(self.model.relative_error_by_majority_vote(1 + 2 * t, x_axis / 100))
        plt.hold(True)
        plt.title('Error-possibility graph by people number')
        plt.xlabel('Possibility of correct')
        plt.ylabel('Relative error')
        for y_axis in y_axis_arr:
            plt.plot(x_axis, y_axis)
        plt.show()

    # 必要になったら実装
    def plot_cost_error_graph_by_possibility(self):
        pass

    def plot_utility_possibility_average_graph(self):
        x_axis = np.linspace(0.5,1.0,50)
        y_axis_arr = []
        y_axis_arr.append([self.model.deciding_by_first_person_with_poisson(x) for x in x_axis])
        y_axis_arr.append([self.model.deciding_by_majority_vote_with_poisson(x, 9) for x in x_axis])
        y_axis_arr.append([self.model.deciding_by_half_opinion_with_poisson(x, 5) for x in x_axis])
        y_axis_arr.append([self.model.deciding_by_time_limit_with_poisson(x, 18) for x in x_axis])
        plt.hold(True)
        plt.title('Utility-possibility graph')
        plt.xlabel('possibility_correct')
        plt.ylabel('Utility')
        for y_axis in y_axis_arr:
            plt.plot(x_axis, y_axis)
        plt.show()

    def plot_utility_possibility_variance_graph(self):
        x_axis = np.linspace(0.5,1.0,50)
        y_axis_arr = []
        y_axis_arr.append([self.model.deciding_by_first_person_with_poisson_for_variance(x) for x in x_axis])
        y_axis_arr.append([self.model.deciding_by_majority_vote_with_poisson_for_variance(x, 9) for x in x_axis])
        y_axis_arr.append([self.model.deciding_by_half_opinion_with_poisson_for_variance(x, 5) for x in x_axis])
        y_axis_arr.append([self.model.deciding_by_time_limit_with_poisson_for_variance(x, 18) for x in x_axis])
        plt.hold(True)
        plt.title('Utility-possibility graph')
        plt.xlabel('possibility_correct')
        plt.ylabel('Utility')
        for y_axis in y_axis_arr:
            plt.plot(x_axis, y_axis)
        plt.show()



    # -----以上はRubyと同じ実装-----
    # -----ここからは新しい実装-----
    # 縦軸をutility、横軸を重みにする
    def plot_utility_weight(arg):
        pass
