import Cell from "./Cell";
import { GRID_SIZES, GridSize } from "@/src/lib/gridConfig";

type Props = {
  map: Record<string, string>;
  position: string;
  orientation: string;
  size: GridSize;
};

const MAX_X = 6;
const MAX_Y = 5;

export default function Grid({
  map,
  position,
  orientation,
  size = 3,
}: Props) {
  const config = GRID_SIZES[size] ;

  const cells = [];

  for (let y = MAX_Y; y >= 0; y--) {
    for (let x = 0; x <= MAX_X; x++) {
      const key = `${x},${y}`;
      const value = map?.[key];

      const isPlayer =
        position[0] === `${x}` && position[3] === `${y}`;

      cells.push(
        <Cell
          key={key}
          value={value}
          isPlayer={isPlayer}
          orientation={orientation}
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