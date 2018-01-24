@lru_cache(maxsize=None)
def poisson_probability(n, t, lambda_poisson):
    return float(Decimal(math.e)**(-Decimal(lambda_poisson) * Decimal(t)) * (Decimal(lambda_poisson) * Decimal(t))**Decimal(n) / Decimal(math.factorial(n)))

@lru_cache(maxsize=None)
def gamma_probability(n, t, lambda_poisson):
    return float(Decimal(lambda_poisson)**n * Decimal(t)**(n - 1) * Decimal(math.e)**(-Decimal(lambda_poisson) * Decimal(t)) / math.factorial(n - 1))

@lru_cache(maxsize=None)
def g(m, n, t, T, lambda_poisson):
    return float(Decimal(lambda_poisson)**Decimal(n) * Decimal(t**(m - 1)) * Decimal((T - t)**(n - m)) * Decimal(math.e)**(-Decimal(lambda_poisson) * Decimal(T)) / (math.factorial(Decimal(m - 1)) * math.factorial(Decimal(n - m))))
