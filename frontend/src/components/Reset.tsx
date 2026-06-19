type Props = {
  mode: string;
  running: boolean;
  onStart: (currentMode: string) => Promise<void>;
};

export default function Reset({ mode, running, onStart }: Props) {
  return (
    <div className="flex items-center gap-3">
      <button
        onClick={() => onStart(mode)}
        disabled={running}
        className={`
          px-4 py-2 rounded-md font-mono text-smbtransition
          ${
            running
              ? "bg-zinc-700 text-zinc-400 cursor-not-allowed"
              : "bg-green-500 hover:bg-green-400 text-black"
          }
        `}
      >
        {running ? "Running..." : "▶ Reset Simulation"}
      </button>
    </div>
  );
}