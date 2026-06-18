"use client";

import GameButton from "@/src/components/GameButton";
import SelectMapButton from "@/src/components/SelectMapButton";
import MotivationButton from "@/src/components/MotivationButton";
import GitHubButton from "@/src/components/GitHubButton";

export default function Home() {
  return (
    <main className="h-screen bg-black text-white overflow-hidden">
      <div className="flex flex-col items-center justify-center h-full">

        {/* Titre */}
        <h1 className="
          scale-[4] origin-center
          mb-12
          select-none
        ">
          HITMAN.
        </h1>

        {/* Liste scrollable */}
        <div className="relative">

          {/* Fade inférieur */}
          <div
            className="
              pointer-events-none
              absolute
              bottom-0
              left-0
              right-0
              h-15
              bg-gradient-to-b
              from-transparent
              to-black
              z-10
            "
          />

          <div
            className="
              h-25
              w-72
              overflow-y-auto
              scrollbar-none
              snap-y
              snap-mandatory
            "
          >
            <div className="flex flex-col items-center gap-1 pb-30">

              <div className="snap-center">
                <GameButton />
              </div>

              <div className="snap-center">
                <SelectMapButton />
              </div>

              <div className="snap-center">
                <MotivationButton />
              </div>

              <div className="snap-center">
                <GitHubButton />
              </div>

            </div>
          </div>
        </div>
      </div>
    </main>
  );
}