"use client";

import GameButton from "@/src/components/GameButton";
import SelectMapButton from "@/src/components/SelectMapButton";
import MotivationButton from "@/src/components/AboutButton";
import GitHubButton from "@/src/components/GitHubButton";

export default function Home() {
  return (
    <main className="h-screen bg-black text-white overflow-hidden">
      <div className="flex flex-col items-center justify-center h-full">

        {/* TITLE */}
        <h1 className="
          scale-[6] origin-center mb-6 select-none z-30
        ">
          HITMAN.
        </h1>

        {/* MENU CONTAINER */}
        <div className="relative">

          {/* TOP FADE */}
          <div
            className="
              pointer-events-none absolute top-0 left-0 right-0 h-24 bg-gradient-to-t from-transparent to-black z-20
            "
          />

          {/* BOTTOM FADE */}
          <div
            className="
              pointer-events-none absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-b from-transparent to-black z-20
            "
          />

          {/* SCROLLABLE MENU */}
          <div
            className="
              h-60 w-72 overflow-y-auto overscroll-none snap-y snap-mandatory scrollbar-none
            "
          >
            <div
              className="
                flex flex-col items-center gap-3 pt-24 pb-24
              "
            >
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