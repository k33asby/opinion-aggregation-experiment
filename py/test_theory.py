# integrate g and poisson should be same
def test_f(t):
    return g(4,10,t,5,2)
value, abserr = integrate.quad(test_f, 0, 5)
print "integrate g and poisson should be same."
print value
print poisson_probability(10,5,2)
print "--------------------------------------------------"

# time_priotity_method probability sum should be 1.0
def time_priotity_method_probability_sum(t, p, lambda_poisson):
    return np.sum(poisson_probability(i, t, lambda_poisson) for i in range(1, int(1.8 * t * lambda_poisson)))
print "time_priotity_method probability sum should be 1.0."
print time_priotity_method_probability_sum(20, 0.6, 1)
print "--------------------------------------------------"

# poll_priority_method probabilty sum should be 1.0
def poll_priotity_method_probability_sum(n, p, lambda_poisson):
    return integrate.quad(lambda t: gamma_probability(n, t, lambda_poisson), 0, np.inf)[0]
print "poll_priority_method probabilty sum should be 1.0."
print poll_priotity_method_probability_sum(20, 0.6, 1)
print "--------------------------------------------------"

# vote_priority_method probabilty sum should be 1.0
def vote_priotity_method_probability_sum(k, p, lambda_poisson):
    return np.sum((scm.comb(j - 1, j - k) * p**(k - 1) * (1 - p)**(j - k) * p) + (scm.comb(j - 1, j - k) * p**(j - k) * (1 - p)**(k - 1) * (1 - p)) for j in range(k, 2 * k))
print "vote_priority_method probabilty sum should be 1.0."
print vote_priotity_method_probability_sum(20, 0.6, 1)
print "--------------------------------------------------"

# method1 probability sum should be 1.0
def method1_probability_sum(T1, n, lambda_poisson):
    p_sum = 0
    for i in range(0, n):
        p_sum += poisson_probability(i, T1, lambda_poisson)
    # 積分を行う
    value, abserr = integrate.quad(lambda t: gamma_probability(n, t, lambda_poisson), 0, T1)
    p_sum += value
    return p_sum
print "method1 probability sum should be 1.0."
print method1_probability_sum(20, 10, 1)
print "--------------------------------------------------"

# method2 probability sum should be 1.0
def method2_probability_sum(T1, T2, n, w, lambda_poisson):
    p_sum = 0
    for i in range(0, n):
        p_sum += poisson_probability(i, T1, lambda_poisson)
    for i in range(n, 100):
        value_1, abserr = integrate.quad(lambda t: g(n, i, t, T1, lambda_poisson), 0, T2)
        value_2, abserr = integrate.quad(lambda t: g(n, i, t, T1, lambda_poisson), T2, T1)
        p_sum += value_1
        p_sum += value_2
    return p_sum
print "method2 probability sum should be 1.0."
print method2_probability_sum(30, 14, 10, 0.02, 1)
print "--------------------------------------------------"
