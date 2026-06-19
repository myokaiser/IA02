export type GameState = {
  map: Record<string, string>;
  nb_lignes: number;
  nb_colonnes: number;
  position: string;
  orientation: string;
  done: boolean;
  phase: number;
  action: string;
  known: string[];
  danger: string[];
};