import { GRID_SIZES, GridSize } from "@/src/lib/gridConfig";

type Props = {
  value?: string;
  isPlayer: boolean;
  orientation: string;
  is_known: boolean;
  size?: GridSize;
};

function getColor(value?: string) {
  if (!value) return "bg-zinc-900";
  if (value === "WALL") return "bg-zinc-600";
  if (value === "TARGET") return "bg-red-500";
  if (value === "SUIT") return "bg-yellow-400";
  if (value === "PIANO_WIRE") return "bg-orange-500";
  if (value.includes("GUARD")) return "bg-blue-500";
  if (value.includes("CIVIL")) return "bg-purple-500";
  if (value === "UNKNOWN") return "bg-zinc-950";
  return "bg-zinc-900";
}

function getPlayerArrow(orientation: string) {
  switch (orientation) {
    case "N":
      return "▲";
    case "S":
      return "▼";
    case "W":
      return "◀";
    case "E":
      return "▶";
    default:
      return "●";
  }
}

export default function Cell({
  value,
  isPlayer,
  orientation,
  is_known,
  size = 3,
}: Props) {
  const config = GRID_SIZES[size];

  return (
    <div
      className={`
        flex items-center justify-center
        transition-all duration-150
        border border-zinc-800
        ${getColor(value)}
        ${isPlayer ? "ring-2 ring-green-400 z-10" : ""}
      `}
      style={{
        width: config.cell,
        height: config.cell,
        fontSize: config.font,
      }}
    >
      {isPlayer ? (
        <span className="text-white font-bold">
          {getPlayerArrow(orientation)}
        </span>
      ) : value ? (
        <span className={`${ is_known ? "text-white" : "text-zinc-500"}`}>
          {value === "UNKNOWN" ? "?" : value[0]}
        </span>
      ) : null}
    </div>
  );
}