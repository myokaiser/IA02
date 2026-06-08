"use client";

import Grid from "@/src/components/Grid";
import Controls from "@/src/components/Controls";
import Reset from "@/src/components/Reset";
import { useGame } from "@/src/hooks/useGame";
import { useKeyboard } from "@/src/hooks/useKeyboard";

export default function Page() {
  const {
    state,
    running,

    reset,
    start,

    move,
    turnLeft,
    turnRight,
    kill,

    mode,
    setMode,
  } = useGame();

  useKeyboard({
    move,
    left: turnLeft,
    right: turnRight,
    kill,
  });

  const isFinished = state && state.done && state.phase === 2;

  if (!state) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-white">
        Loading initial state...
      </div>
    );
  }

return (
  <div className="min-h-screen bg-black text-white flex flex-col items-center gap-6 p-6">

    {/* CONTROLS */}
    <div className="flex flex-col items-center gap-4">

      <div className="flex gap-4">

        <button
          onClick={() => setMode("ai")}
          className={`px-4 py-2 ${mode === "ai" ? "bg-green-600" : "bg-zinc-600"} rounded`}
        >
          AI
        </button>

        <button
          onClick={() => setMode("manual")}
          className={`px-4 py-2 ${mode === "manual" ? "bg-green-600" : "bg-zinc-600"} rounded`}
        >
          Human
        </button>

      </div>


      {mode === "ai" && <>{!isFinished ? (
        <Controls running={running} onStart={start} />
      ) : (
        <Reset running={running} onStart={reset} />
      )}

      {!running && (
        <div className="text-xs text-zinc-400">
          Preview mode (initial state)
        </div>
      )}</>}
    </div>

    {/* GRID */}
    <div className="mt-4 origin-center">
      <Grid
        map={state.map}
        position={state.position}
        orientation={state.orientation}
        size={4}
      />
    </div>

    {/* STATUS */}
    {isFinished && (
      <div className="text-red-400 font-bold">
        Simulation finished
      </div>
    )}

  </div>
);
};