class table:

    def __init__(self):
        self.model = modeling()

    def table_method2(self, w, p, lambda_poisson):
        arr = range(1, 50)
        m2_df = pd.DataFrame({
            'a1': [self.model.method2(1, n, w, p, lambda_poisson) for n in arr],
            'b2': [self.model.method2(2, n, w, p, lambda_poisson) for n in arr],
            'c3': [self.model.method2(3, n, w, p, lambda_poisson) for n in arr],
            'd4': [self.model.method2(4, n, w, p, lambda_poisson) for n in arr],
            'e5': [self.model.method2(5, n, w, p, lambda_poisson) for n in arr],
            'f6': [self.model.method2(6, n, w, p, lambda_poisson) for n in arr],
            'g7': [self.model.method2(7, n, w, p, lambda_poisson) for n in arr],
            'h8': [self.model.method2(8, n, w, p, lambda_poisson) for n in arr],
            'i9': [self.model.method2(9, n, w, p, lambda_poisson) for n in arr],
            'j10': [self.model.method2(10, n, w, p, lambda_poisson) for n in arr],
            'k11': [self.model.method2(11, n, w, p, lambda_poisson) for n in arr],
            'l12': [self.model.method2(12, n, w, p, lambda_poisson) for n in arr],
            'm13': [self.model.method2(13, n, w, p, lambda_poisson) for n in arr],
            'n14': [self.model.method2(14, n, w, p, lambda_poisson) for n in arr],
            'o15': [self.model.method2(15, n, w, p, lambda_poisson) for n in arr],
            'p16': [self.model.method2(16, n, w, p, lambda_poisson) for n in arr],
            'q17': [self.model.method2(17, n, w, p, lambda_poisson) for n in arr],
            'r18': [self.model.method2(18, n, w, p, lambda_poisson) for n in arr],
            's19': [self.model.method2(19, n, w, p, lambda_poisson) for n in arr],
            't20': [self.model.method2(20, n, w, p, lambda_poisson) for n in arr],
        })
        return df.style.background_gradient(cmap='winter')

    def table_method3(self,T1 w, p, lambda_poisson):
        arr = range(1, 50)
        m3_df = pd.DataFrame({
            'a1': [self.model.method3(T1,1, n, w, p, lambda_poisson) for n in arr],
            'b2': [self.model.method3(T1,2, n, w, p, lambda_poisson) for n in arr],
            'c3': [self.model.method3(T1,3, n, w, p, lambda_poisson) for n in arr],
            'd4': [self.model.method3(T1,4, n, w, p, lambda_poisson) for n in arr],
            'e5': [self.model.method3(T1,5, n, w, p, lambda_poisson) for n in arr],
            'f6': [self.model.method3(T1,6, n, w, p, lambda_poisson) for n in arr],
            'g7': [self.model.method3(T1,7, n, w, p, lambda_poisson) for n in arr],
            'h8': [self.model.method3(T1,8, n, w, p, lambda_poisson) for n in arr],
            'i9': [self.model.method3(T1,9, n, w, p, lambda_poisson) for n in arr],
            'j10': [self.model.method3(T1,10, n, w, p, lambda_poisson) for n in arr],
            'k11': [self.model.method3(T1,11, n, w, p, lambda_poisson) for n in arr],
            'l12': [self.model.method3(T1,12, n, w, p, lambda_poisson) for n in arr],
            'm13': [self.model.method3(T1,13, n, w, p, lambda_poisson) for n in arr],
            'n14': [self.model.method3(T1,14, n, w, p, lambda_poisson) for n in arr],
            'o15': [self.model.method3(T1,15, n, w, p, lambda_poisson) for n in arr],
            'p16': [self.model.method3(T1,16, n, w, p, lambda_poisson) for n in arr],
            'q17': [self.model.method3(T1,17, n, w, p, lambda_poisson) for n in arr],
            'r18': [self.model.method3(T1,18, n, w, p, lambda_poisson) for n in arr],
            's19': [self.model.method3(T1,19, n, w, p, lambda_poisson) for n in arr],
            't20': [self.model.method3(T1,20, n, w, p, lambda_poisson) for n in arr],
        })
        return df.style.background_gradient(cmap='winter')
