def calculate_kelly_bet(market_prob, my_prob, bankroll, kelly_fraction=0.25, max_bet=50):
    """
    Calcula el tamaño de apuesta óptimo utilizando el Criterio de Kelly Fraccionario.
    
    Argumentos:
        market_prob (float): La probabilidad actual en Manifold (0.0 a 1.0).
        my_prob (float): La probabilidad verdadera estimada por el bot (0.0 a 1.0).
        bankroll (float): Saldo actual disponible.
        kelly_fraction (float): Fracción de Kelly a utilizar (amortiguador de riesgo).
        max_bet (float): Cantidad máxima absoluta de mana para arriesgar.
        
    Retorna:
        float: La cantidad de mana a apostar. Retorna 0 si la ventaja es negativa.
    """
    if market_prob <= 0 or market_prob >= 1:
        return 0
    
    # Fórmula de Kelly: f = (p(b+1) - 1) / b
    # En opciones binarias (cuota 1/prob): f = p/market_prob - q/(1-market_prob)
    # donde p = my_prob, q = 1-my_prob
    
    # Determinar dirección
    if my_prob > market_prob:
        # Apostando SÍ (YES)
        # Cuota b = (1 - market_prob) / market_prob
        b = (1 / market_prob) - 1
        p = my_prob
        f = p - (1 - p) / b
    else:
        # Apostando NO
        # Cuota b = market_prob / (1 - market_prob)
        b = (1 / (1 - market_prob)) - 1
        p = 1 - my_prob
        f = p - (1 - p) / b

    # Aplicar gestión de riesgo (Kelly Fraccionario)
    f_star = f * kelly_fraction
    
    if f_star <= 0:
        return 0
        
    bet_amount = bankroll * f_star
    
    # Limitar la apuesta al máximo configurado
    return min(bet_amount, max_bet)