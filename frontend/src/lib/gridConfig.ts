export const GRID_SIZE = 3 as const;

export const GRID_SIZES = {
  1: {
    cell: 20,
    gap: 1,
    font: 8,
  },
  2: {
    cell: 28,
    gap: 1,
    font: 10,
  },
  3: {
    cell: 36,
    gap: 2,
    font: 12,
  },
  4: {
    cell: 44,
    gap: 2,
    font: 14,
  },
} as const;

export type GridSize = keyof typeof GRID_SIZES;