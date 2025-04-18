import numpy as np
import pandas as pd

def kelly_bet(bankroll, odds, confidence, fraction=3):
    """Рассчитывает ставку по критерию Келли с учетом текущего банкролла."""
    if odds <= 1 or (odds * confidence) <= 1:
        return 0  # избегаем деления на 0 или невыгодных ставок
    f_star = (odds * confidence - 1) / (odds - 1)
    bet = f_star * (1 / fraction) * bankroll
    return max(0, min(bet, bankroll))  # ставка не может превышать bankroll

def predict_bets(df_odds_conf, initial_bankroll=10000, fraction=2, min_bankroll=100):
    """
    df_odds_conf: Dataframe
    initial_bankroll: капитал
    fraction: коэффициент Келли
    min_bankroll: Сумма останова
    """
    df = df_odds_conf.copy()
    bankroll = initial_bankroll

    # Создаем отдельные DataFrame для каждого исхода
    home_bets = df[['home', 'away', 'odds_home', 'confidence_home']].copy()
    home_bets['outcome'] = 'home'
    home_bets.rename(columns={'odds_home': 'odds', 'confidence_home': 'confidence'}, inplace=True)

    draw_bets = df[['home', 'away', 'odds_draw', 'confidence_draw']].copy()
    draw_bets['outcome'] = 'draw'
    draw_bets.rename(columns={'odds_draw': 'odds', 'confidence_draw': 'confidence'}, inplace=True)

    away_bets = df[['home', 'away', 'odds_away', 'confidence_away']].copy()
    away_bets['outcome'] = 'away'
    away_bets.rename(columns={'odds_away': 'odds', 'confidence_away': 'confidence'}, inplace=True)

    # Объединяем все ставки в один DataFrame
    all_bets = pd.concat([home_bets, draw_bets, away_bets], ignore_index=True)

    # Рассчитываем value_bet и фильтруем невыгодные ставки
    all_bets['value_bet'] = np.where(
        all_bets['odds'] * all_bets['confidence'] > 1,
        all_bets['odds'] * all_bets['confidence'],
        np.nan
    )
    #print(all_bets)
    all_bets = all_bets.dropna(subset=['value_bet'])

    # Сортируем по value_bet (лучшие ставки сначала)
    all_bets = all_bets.sort_values('value_bet', ascending=False).reset_index(drop=True)

    # Применяем ставки с обновлением банкролла
    bets_info = []
    bankroll_history = []

    for _, row in all_bets.iterrows():
        if bankroll < min_bankroll:
            break

        bet = kelly_bet(bankroll, row['odds'], row['confidence'], fraction)
        if bet > 0:
            bets_info.append({
                'home': row['home'],
                'away': row['away'],
                'outcome': row['outcome'],
                'odds': row['odds'],
                'confidence': row['confidence'],
                'value_bet': row['value_bet'],
                'bet_amount': bet
            })
            bankroll -= bet
            bankroll_history.append(bankroll)

    # Создаем DataFrame с результатами
    result_df = pd.DataFrame(bets_info)
    if not result_df.empty:
        result_df['bankroll_after_bet'] = bankroll_history
    else:
        result_df['bankroll_after_bet'] = []
    result_df=result_df[result_df['bet_amount']>=50]
    result_df["possible_profit"] = result_df["odds"]*result_df["bet_amount"]-result_df["bet_amount"]

    # Сортируем по possible_profit (лучшие ставки сначала)

    return result_df