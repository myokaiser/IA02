import Cell from "./Cell";
import { GRID_SIZES, GridSize } from "@/src/lib/gridConfig";

type Props = {
  map: Record<string, string>;
  position: string;
  orientation: string;
  nb_lignes: number;
  nb_colonnes: number;
  known: string[];
  danger: string[];
  size: GridSize;
};

export default function Grid({
  map,
  position,
  orientation,
  nb_lignes,
  nb_colonnes,
  known,
  danger,
  size = 3,
}: Props) {
  const config = GRID_SIZES[size] ;

  const MAX_X = nb_colonnes - 1;
  const MAX_Y = nb_lignes - 1;

  const cells = [];

  for (let y = MAX_Y; y >= 0; y--) {
    for (let x = 0; x <= MAX_X; x++) {
      const key = `${x},${y}`;
      const value = map?.[key];
      const is_known = known.includes(key);
      const is_danger = danger.includes(key);

      const isPlayer =
        position[0] === `${x}` && position[3] === `${y}`;

      cells.push(
        <Cell
          key={key}
          value={value}
          isPlayer={isPlayer}
          orientation={orientation}
          is_known={is_known}
          is_danger={is_danger}
          size={size}
        />
      );
    }
  }

  return (
    <div
      className="grid bg-zinc-800 rounded-lg shadow-xl w-fit"
      style={{
        gridTemplateColumns: `repeat(7, ${config.cell}px)`,
        gap: `${config.gap}px`,
        padding: `${config.gap * 2}px`,
      }}
    >
      {cells}
    </div>
  );
}