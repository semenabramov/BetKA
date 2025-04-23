export interface OddsSource {
    id?: number;
    name: string;
    url: string;
    premier_league_url?: string;
    championship_url?: string;
    league_one_url?: string;
    league_two_url?: string;
    bundesliga_one_url?: string;
    bundesliga_two_url?: string;
    liga_url?: string;
    la_liga_url?: string;
    serie_a_url?: string;
    ligue_one_url?: string;
    is_active: boolean;
    created_at?: string;
    updated_at?: string;
} 