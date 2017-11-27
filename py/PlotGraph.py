class PlotGraph:

    def test(self):
        x = np.linspace(50, 100, 1)
        y = 2 * (x**2)
        plt.plot(x,y)
        plt.show()
