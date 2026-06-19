"use client";

import { useEffect, useState } from "react";
import Grid from "@/src/components/Grid";
import EscapeButton from "@/src/components/EscapeButton";
import type { GameState } from "@/src/types/game";

import {
  getMaps,
  getMapPreview,
  selectMap,
} from "@/src/lib/api";

export default function MapsPage() {
  const [maps, setMaps] = useState<string[]>([]);
  const [selectedMap, setSelectedMap] = useState<string | null>(null);
  const [currentMap, setCurrentMap] = useState<string | null>(null);
  const [grid, setGrid] = useState<GameState | null>(null);

  useEffect(() => {
    const load = async () => {
      const data = await getMaps();

      const sorted = data.sort();
      setMaps(sorted);

      if (sorted.length > 0) {
        setSelectedMap(sorted[0]);
        setCurrentMap(sorted[0]);
      }
    };

    load();
  }, []);

  // fetch available maps
  useEffect(() => {
    if (!selectedMap) return;

    const loadPreview = async () => {
      const data = await getMapPreview(selectedMap);
      setGrid(data.grid);
    };

    loadPreview();
  }, [selectedMap]);

  // fetch selected map preview
  const chooseMap = async () => {
    if (!selectedMap) return;

    setCurrentMap(selectedMap);
    await selectMap(selectedMap);
  };

  return (
    <div className="flex h-screen bg-zinc-950 text-white">
      {/* SIDEBAR */}
      <div className="w-64 border-r border-zinc-800 p-4">
        <h1 className="text-2xl font-bold tracking-wider mb-4 text-zinc-200">
          AVAILABLE MAPS
        </h1>

        <div className="space-y-2">
          {maps.map((m) => (
            <button
              key={m}
              onClick={() => setSelectedMap(m)}
              className={`
                w-full font-mono text-left px-3 py-2 rounded-lg transition hover:bg-zinc-800  
                ${
                  selectedMap === m
                    ? "bg-zinc-800 border border-zinc-600"
                    : "bg-transparent"
                }
              `}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-6">
        <h2 className="text-xl  font-mono font-semibold mb-4 text-zinc-200">
          Preview:{" "}
          <span className="text-zinc-400">
            {selectedMap ?? "No map selected"}
          </span>
        </h2>

        {!grid ? (
          <div className=" font-mono text-zinc-500">Loading map...</div>
        ) : (
          <div className="flex flex-col items-start gap-4">
            <div className="inline-block border border-zinc-800 rounded-lg overflow-hidden">
                <div className="origin-center">
                    <Grid
                        map={grid.map}
                        position={grid.position}
                        orientation={grid.orientation}
                        nb_lignes={grid.nb_lignes}
                        nb_colonnes={grid.nb_colonnes}
                        known={grid.known}
                        danger={grid.danger}
                        size={4}
                    />
                </div>
            </div>

            <button
                onClick={chooseMap}
                className={`
                     font-mono px-6 py-3 rounded-lg font-semibold transition-colors duration-200
                    ${
                      currentMap === selectedMap
                        ? "bg-green-600 hover:bg-green-500"
                        : "bg-zinc-700 hover:bg-zinc-600"
                    }
                `}
            >
                {currentMap === selectedMap
                  ? "Selected Map"
                  : "Select This Map"
                }
            </button>
        </div>
        )}
      </div>
      <EscapeButton />
    </div>
  );
}