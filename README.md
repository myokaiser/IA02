# HITMAN IA02 – Remastered Edition

## Overview

This project is a complete remaster and optimization of the final assignment from the **IA02 – Problem Solving and Logic Programming** course.

The original project provided a functional implementation of the Hitman agent and its logical reasoning system. This repository revisits that work with a focus on:

* Algorithmic improvements
* Codebase refactoring
* Performance optimizations
* Enhanced SAT-based reasoning
* Modern web visualization
* Improved architecture and maintainability
* New gameplay and debugging tools

Several parts of the original implementation have been entirely redesigned or rewritten to improve both the agent's behavior and the overall user experience.

---

## Repository Structure

### `frontend/`

Contains the modern web interface built with **Next.js**, **TypeScript**, and **Tailwind CSS**.

Features include:

* Interactive game visualization
* AI simulation controls
* Map selection menu
* Project documentation pages
* Real-time communication with the backend API

---

### `backend/`

Contains the complete game engine and AI logic.

Main responsibilities:

* SAT-based knowledge representation
* Logical deduction engine
* Exploration algorithms
* Pathfinding
* Phase 1 and Phase 2 gameplay logic
* Map management
* Flask REST API

---

### `raw/`

Contains the original project exactly as it was delivered at the end of the course.

This folder is preserved for historical and comparison purposes and serves as a reference to evaluate the changes introduced by the remastered version.

---

## Running the Project

The application consists of two independent services that must be started simultaneously.

### 1. Start the Backend

Open a terminal in the `backend` directory:

```bash
flask run
```

The Flask API will start on its configured port.

---

### 2. Start the Frontend

Open another terminal in the `frontend` directory:

```bash
pnpm run dev
```

The Next.js application will start and become available in your browser.

---

## Technologies

### Backend

* Python
* Flask
* SAT Solver
* A* Pathfinding
* Propositional Logic

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

---

## Project Goals

The objective is to control Hitman in a partially observable environment.

The agent must:

1. Explore an unknown map.
2. Deduce hidden information using logical reasoning.
3. Locate useful equipment.
4. Find the target.
5. Eliminate the target.
6. Escape safely.

The project combines symbolic AI, planning, pathfinding, and game visualization into a single application.

---

## Notes

This repository is intended as a modernization effort rather than a replacement of the original work delivered.

The `raw/` directory preserves the initial implementation, while the current backend and frontend showcase a more advanced and maintainable version of the project.
