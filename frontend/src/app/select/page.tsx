"use client";

import { useEffect, useState } from "react";
import Grid from "@/src/components/Grid";

type Data = {
    map: Record<string, string>,
    nb_lignes: number,
    nb_colonnes: number,
    position: string,
    orientation: string,
    done: boolean,
    phase: number,
    action: string,
    known: string[]
}

export default function MapsPage() {
  const [maps, setMaps] = useState<string[]>([]);
  const [selectedMap, setSelectedMap] = useState<string | null>(null);
  const [currentMap, setCurrentMap] = useState<string | null>(null);
  const [grid, setGrid] = useState<Data | null>(null);

  const chooseMap = async () => {
    if (!selectedMap) return;

    setCurrentMap(selectedMap);

    await fetch("http://localhost:5000/map", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            map: selectedMap,
        }),
    });
    };

  // fetch available maps
  useEffect(() => {
    fetch("http://localhost:5000/maps")
      .then((res) => res.json())
      .then((data) => {
            const sorted = data.sort();

            setMaps(sorted);

            if (sorted.length > 0) {
                setSelectedMap(sorted[0]);
                setCurrentMap(sorted[0]);
            }
      });
  }, []);

  // fetch selected map preview
  useEffect(() => {
    if (!selectedMap) return;

    fetch("http://localhost:5000/map-preview", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ map: selectedMap }),
    })
      .then((res) => res.json())
      .then((data) => setGrid(data.grid));
  }, [selectedMap]);

  return (
    <div className="flex h-screen bg-zinc-950 text-white">
      {/* SIDEBAR */}
      <div className="w-64 border-r border-zinc-800 p-4">
        <h1 className="text-lg font-bold mb-4 text-zinc-200">
          Available Maps
        </h1>

        <div className="space-y-2">
          {maps.map((m) => (
            <button
              key={m}
              onClick={() => setSelectedMap(m)}
              className={`
                w-full text-left px-3 py-2 rounded-lg transition
                hover:bg-zinc-800
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
        <h2 className="text-xl font-semibold mb-4 text-zinc-200">
          Preview:{" "}
          <span className="text-zinc-400">
            {selectedMap ?? "No map selected"}
          </span>
        </h2>

        {!grid ? (
          <div className="text-zinc-500">Loading map...</div>
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
                        size={4}
                    />
                </div>
            </div>

            <button
                onClick={chooseMap}
                className={`
                    px-6 py-3 rounded-lg font-semibold transition-colors duration-200
                    ${
                        currentMap === selectedMap
                            ? "bg-green-600 hover:bg-green-500"
                            : "bg-zinc-700 hover:bg-zinc-600"
                    }
                `}
            >
                {currentMap === selectedMap
                    ? "Selected Map"
                    : "Select This Map"}
            </button>
        </div>
        )}
      </div>
    </div>
  );
}