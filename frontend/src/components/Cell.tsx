type Props = {
  value?: string;
  isPlayer: boolean;
  orientation: string;
};

function getColor(value?: string) {
  if (!value) return "bg-zinc-900";

  if (value === "WALL") return "bg-zinc-600";
  if (value === "TARGET") return "bg-red-500";
  if (value === "SUIT") return "bg-yellow-400";
  if (value === "PIANO_WIRE") return "bg-orange-500";
  if (value.includes("GUARD")) return "bg-blue-500";
  if (value.includes("CIVIL")) return "bg-purple-500";

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

export default function Cell({ value, isPlayer, orientation }: Props) {
  return (
    <div
      className={`
        w-6 h-6
        flex items-center justify-center
        text-[10px] font-mono
        transition-all duration-150
        border border-zinc-800
        ${getColor(value)}
        ${isPlayer ? "ring-2 ring-green-400 z-10 scale-110" : ""}
      `}
    >
      {isPlayer ? (
        <span className="text-white font-bold">
          {getPlayerArrow(orientation)}
        </span>
      ) : value ? (
        <span className="text-white/80">
          {value[0]}
        </span>
      ) : null}
    </div>
  );
}