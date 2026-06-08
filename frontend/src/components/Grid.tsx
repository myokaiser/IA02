import Cell from "./Cell";

type Props = {
  map: Record<string, string>;
  position: string;
  orientation: string;
};

const MAX_X = 6;
const MAX_Y = 5;

export default function Grid({ map, position, orientation }: Props) {
  const cells = [];

  for (let y = MAX_Y; y >= 0; y--) {
    for (let x = 0; x <= MAX_X; x++) {
      const key = `${x},${y}`;
      const value = map?.[key];

      const isPlayer = position[0] === `${x}` && position[3] === `${y}`;

      cells.push(
        <Cell
          key={key}
          value={value}
          isPlayer={isPlayer}
          orientation={orientation}
        />
      );
    }
  }

  return (
    <div className="grid grid-cols-7 gap-[1px] bg-zinc-800 p-2 rounded-lg shadow-xl w-fit">
      {cells}
    </div>
  );
}