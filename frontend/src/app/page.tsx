"use client";

import GameButton from "@/src/components/GameButton";
import GitHubButton from "@/src/components/GitHubButton";

export default function Home() {

  return (
    <div className="p-6 flex flex-col gap-4 bg-black min-h-screen text-white">

      <div className="flex flex-col items-center justify-center min-h-screen bg-black gap-6">
        <div className="scale-[3] origin-center">
          HITMAN.
        </div>
        <div className="flex flex-col gap-1 items-center">
          <GameButton />
          <GitHubButton /> 
        </div>

      </div>

    </div>
  );
}