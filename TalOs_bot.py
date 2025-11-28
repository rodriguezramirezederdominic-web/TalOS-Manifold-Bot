import time
import requests
from manifoldbot import ManifoldAPI
from config import MANIFOLD_API_KEY, TARGET_CREATOR_USERNAME, MIN_EDGE
from brain import MarketBrain
from kelly import calculate_kelly_bet

class TalOS:
    def __init__(self):
        self.api = ManifoldAPI(MANIFOLD_API_KEY)
        self.brain = MarketBrain()
        self.target_user_id = self._get_user_id(TARGET_CREATOR_USERNAME)
        print(f"TalOS En Línea. Objetivo Usuario: {TARGET_CREATOR_USERNAME} ({self.target_user_id})")

    def _get_user_id(self, username):
        """Resuelve el nombre de usuario a un ID numérico."""
        try:
            user = self.api.get_user_by_username(username)
            return user.id
        except:
            # Búsqueda manual si el método de la librería falla
            url = f"https://api.manifold.markets/v0/user/{username}"
            resp = requests.get(url).json()
            return resp.get('id')

    def fetch_target_markets(self):
        """Busca mercados binarios activos creados por MikhailTal."""
        # Nota: manifoldbot puede no tener un filtro directo por creador en `get_markets`.
        # Consultamos manualmente la API para mayor precisión.
        url = "https://api.manifold.markets/v0/markets"
        params = {
            "creatorId": self.target_user_id,
            "limit": 100
        }
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            print("Error al buscar mercados")
            return []
            
        markets = resp.json()
        # Filtrar solo mercados binarios activos (no resueltos)
        return [m for m in markets if m['isResolved'] is False and m['outcomeType'] == 'BINARY']

    def execute_strategy(self):
        markets = self.fetch_target_markets()
        me = self.api.get_me()
        bankroll = me.balance

        print(f"Escaneando {len(markets)} mercados de {TARGET_CREATOR_USERNAME}...")

        for market in markets:
            question = market['question']
            market_prob = market['probability']
            market_id = market['id']
            description = market.get('textDescription', '')

            # 1. Analizar
            my_prob = self.brain.analyze_market(question, description, market_prob)
            
            # 2. Calcular Ventaja (Edge)
            edge = abs(my_prob - market_prob)
            print(f"P: {question[:30]}... | Mkt: {market_prob:.2f} | Brain: {my_prob:.2f} | Ventaja: {edge:.2f}")

            if edge > MIN_EDGE:
                # 3. Calcular tamaño de apuesta (Kelly)
                bet_amount = calculate_kelly_bet(market_prob, my_prob, bankroll)
                
                if bet_amount < 1:
                    continue

                outcome = "YES" if my_prob > market_prob else "NO"
                
                print(f" >> DISPARANDO: {outcome} en {market_id} por {bet_amount:.1f} mana")
                
                # 4. Ejecutar
                try:
                    self.api.create_bet(
                        contractId=market_id,
                        amount=bet_amount,
                        outcome=outcome
                    )
                    # Actualizar estimación de saldo localmente para evitar gastar de más en un solo ciclo
                    bankroll -= bet_amount 
                except Exception as e:
                    print(f"Fallo al apostar: {e}")
            
            time.sleep(1) # Cortesía para no saturar la API

if __name__ == "__main__":
    bot = TalOS()
    while True:
        try:
            bot.execute_strategy()
        except Exception as e:
            print(f"Error Crítico en el Bucle: {e}")
        
        print("Durmiendo ciclo...")
        time.sleep(300) # Ejecutar cada 5 minutos