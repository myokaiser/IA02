type Props = {
  running: boolean;
  onStart: () => void;
};

export default function Controls({ running, onStart }: Props) {
  return (
    <div className="flex items-center gap-3">
      <button
        onClick={onStart}
        disabled={running}
        className={`
          px-4 py-2 rounded-md font-mono text-sm
          transition
          ${
            running
              ? "bg-zinc-700 text-zinc-400 cursor-not-allowed"
              : "bg-green-500 hover:bg-green-400 text-black"
          }
        `}
      >
        {running ? "Running..." : "▶ Start Simulation"}
      </button>

      <div className="text-xs text-zinc-400">
        {running ? "Agent active" : "Idle"}
      </div>
    </div>
  );
}