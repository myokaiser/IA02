"use client";

import { useState } from "react";
import EscapeButton from "@/src/components/EscapeButton";

const sections = [
  {
    id: "purpose",
    title: "Purpose",
  },
  {
    id: "rules",
    title: "Game Rules",
  },  
  {
    id: "representation",
    title: "Knowledge Representation",
  },
  {
    id: "architecture",
    title: "Architecture",
  },
  {
    id: "algorithms",
    title: "Algorithms",
  },
  {
    id: "future",
    title: "Future Improvements",
  },
];

export default function MotivationPage() {
  const [activeSection, setActiveSection] = useState("purpose");

  return (
    <div className="min-h-screen bg-black text-white flex font-mono">
      {/* SIDEBAR */}
      <aside className="w-72 border-r border-zinc-800 sticky top-0 h-screen">
        <div className="p-6">
          <h1 className="text-2xl font-bold tracking-wider mb-4 text-zinc-200">
            PROJECT OVERVIEW
          </h1>

          <div className="space-y-2">
          {sections.map((section) => (
            <button
            key={section.id}
            onClick={() => {
              setActiveSection(section.id);

              document
              .getElementById(section.id)
              ?.scrollIntoView({
                behavior: "smooth",
                block: "start",
              });
            }}
            className={`
              w-full font-mono text-left px-3 py-2 rounded-lg transition
              hover:bg-zinc-800
              ${
                activeSection === section.id
                  ? "bg-zinc-800 border border-zinc-600"
                  : "bg-transparent"
              }
            `}
            >
              {section.title}
            </button>
          ))}
          </div>
        </div>
      </aside>

      {/* CONTENT */}
      <main className="flex-1 overflow-y-auto scrollbar-none snap-y snap-mandatory">
        <div className="max-w-5xl mx-auto px-12 py-16">

          {/* HEADER */}
          <div className="mb-24">
            <h1 className="text-6xl font-bold mb-6">
              Hitman AI
            </h1>

            <p className="text-zinc-400 text-lg max-w-3xl">
              {`A SAT-based autonomous agent capable of exploring,
              reasoning and completing stealth assassination
              missions under partial information.`}
            </p>
          </div>

          {/* PURPOSE */}
          <section
            id="purpose"
            className="scroll-mt-20 mb-24"
          >
            <h2 className="text-4xl font-bold mb-8">
              Purpose
            </h2>

            <div className="space-y-6 text-zinc-300 leading-8">
              <p>
                {`This project is a modernized and optimized version
                of the final assignment for the IA02 –
                Problem Solving and Logic Programming course.`}
              </p>

              <p>
                {`The objective is to control the famous contract
                killer Hitman. Before entering the area, the only
                information available is the number of guards and
                civilians present.`}
              </p>

              <p>
               {` During the exploration phase, Hitman must gather
                information while remaining discreet. Every action
                matters: movement is costly, encounters with guards
                are risky, and deduction plays a central role in
                discovering the layout of the map.`}
              </p>

              <p>
                {`During the execution phase, guards and civilians
                become sensitive to Hitman's presence. The agent
                must retrieve a disguise, locate a piano wire,
                eliminate the target and safely return to the
                entrance.`}
              </p>
            </div>
          </section>

          {/* RULES */}
          <section
            id="rules"
            className="scroll-mt-20 mb-24"
          >
            <h2 className="text-4xl font-bold mb-8">
              Game Rules
            </h2>

            <div className="space-y-6 text-zinc-300 leading-8">
              <p>
                {`The environment is represented as a grid-based map initially 
                unknown to the agent.`}
              </p>

              {/* AVAILABLE ACTIONS */}
              <h2 className="text-3xl font-bold mb-8">
                Available Actions
              </h2>

              <p>
                {`Hitman can perform the following actions:`}
              </p>
              <ul className="pl-10 list-disc space-y-4 text-zinc-300">
                <li>
                  Move forward.
                </li>
                <li>
                  Turn clockwise.
                </li>
                <li>
                  Turn counter-clockwise.
                </li>
                <li>
                  Neutralize guards.
                </li>
                <li>
                  Neutralize civilians.
                </li>
                <li>
                  Pick up objects.
                </li>
                <li>
                  Wear a disguise.
                </li>
                <li>
                  Eliminate the target.
                </li>
              </ul>
              <p>
                {`Each action has an associated cost, encouraging efficient planning 
                and stealthy behavior.`}
              </p>

              <h2 className="text-3xl font-bold mb-8">
                Vision
              </h2>
              <p>
                {`Hitman's vision extends in the direction he is currently facing.`}
              </p>

              <p>
               {`The vision system provides the exact content of every 
               visible cell until a wall blocks the line of sight.`}
              </p>

              <p>
                {`Observed information is considered perfectly reliable 
                and becomes permanent knowledge.`}
              </p>

              {/* HEARING */}
              <h2 className="text-3xl font-bold mb-8">
                Hearing
              </h2>
              <p>
                {`Hitman can hear nearby individuals within a fixed radius 
                around his current position.`}
              </p>

              <p>
               {`Unlike vision, hearing does not reveal positions or 
               identities. It only returns the number of people present 
               in the listening area.`}
              </p>

              <p>
                {`This information must therefore be combined with logical 
                reasoning to infer possible locations of guards and civilians.`}
              </p>

              {/* GUARDS AND CIVILIANS */}
              <h2 className="text-3xl font-bold mb-8">
                Guards and Civilians
              </h2>
              <p>
                {`Guards and civilians have a fixed orientation throughout 
                the mission.`}
              </p>

              <p>
               {`A guard observes the two cells directly in front of him.`}
              </p>

              <p>
                {`A civilian observes the cell directly in front of
                 him and his own position.`}
              </p>

              <p>
                {`Being observed by a guard increases the mission 
                penalty. During the execution phase, being detected 
                can compromise the mission.`}
              </p>

              {/* MISSION OBJECTIVE */}
              <h2 className="text-3xl font-bold mb-8">
                Mission Objective
              </h2>
              <p>
                {`To complete the mission, Hitman must:`}
              </p>

              <ul className="pl-10 list-decimal space-y-4 text-zinc-300">
                <li>
                  Explore the environment.
                </li>
                <li>
                  Locate the piano wire.
                </li>
                <li>
                  Find the target.
                </li>
                <li>
                  Eliminate the target.
                </li>
                <li>
                  Return safely to the starting position.
                </li>
              </ul>
            </div>
          </section>

          {/* REPRESENTATION */}
          <section
            id="representation"
            className="scroll-mt-20 mb-24"
          >
            <h2 className="text-4xl font-bold mb-8">
              Knowledge Representation
            </h2>

            <div className="space-y-6 text-zinc-300 leading-8">
              <p>
                {`The project relies on a propositional SAT 
                solver to represent and reason about the environment.`}
              </p>

              <p>
                {`The knowledge base follows a deliberately rigid 
                structure in order to guarantee logical consistency.`}
              </p>

              {/* CELL REPRESENTATION */}
              <h2 className="text-3xl font-bold mb-8">
                Cell Representation
              </h2>

              <p>
                {`Each cell is associated with a set of propositional 
                variables describing its nature.`} 
              </p>
              <p>
                {`Possible contents include:`}
              </p>
              <ul className="pl-10 list-disc space-y-4 text-zinc-300">
                <li>
                  Empty
                </li>
                <li>
                  Wall
                </li>
                <li>
                  Piano Wire
                </li>
                <li>
                  Suit
                </li>
                <li>
                  Target
                </li>
                <li>
                  Guard
                </li>
                <li>
                  Civilian
                </li>
              </ul>
              <p>
                {`A cell can contain exactly one of these categories.`}
              </p>

              {/* PERSON, ROLE AND ORIENTATION */}
              <h2 className="text-3xl font-bold mb-8">
                Person, Role and Orientation
              </h2>
              <p>
                {`Human entities are represented using three conceptual layers:`}
              </p>
              <ul className="pl-10 list-decimal space-y-4 text-zinc-300">
                <li>
                  Person
                </li>
                <li>
                  Role
                </li>
                <li>
                  Orientation
                </li>
              </ul>
              <p>
                {`For example:`}
              </p>
              <ul className="pl-10 list-disc space-y-4 text-zinc-300">
                <li>
                  Guard North
                </li>
                <li>
                  Guard South
                </li>
                <li>
                  Guard East
                </li>
                <li>
                  Guard West
                </li>
                <li>
                  Civilian North
                </li>
                <li>
                  Civilian South
                </li>
                <li>
                  Civilian East
                </li>
                <li>
                  Civilian West
                </li>
              </ul>
              <p>
                {`The notion of "Person" is separated from role 
                and orientation.`}
              </p>

              <p>
               {`This allows the agent to reason at multiple 
               levels of abstraction:`}
              </p>
              <ul className="pl-10 list-disc space-y-4 text-zinc-300">
                <li>
                  A cell may contain a person.
                </li>
                <li>
                  The person may be a guard or a civilian.
                </li>
                <li>
                  The person may face a specific direction.
                </li>
              </ul>
              <p>
                {`This decomposition enables deductions that would not 
                be possible with a single monolithic representation.`}
              </p>

              {/* GLOBAL CONSTRAINTS */}
              <h2 className="text-3xl font-bold mb-8">
                Global Constraints
              </h2>
              <p>
                {`Several global constraints are enforced:`}
              </p>
              <ul className="pl-10 list-disc space-y-4 text-zinc-300">
                <li>
                  Exactly one content per cell.
                </li>
                <li>
                  Exactly one target on the map.
                </li>
                <li>
                  Exactly one suit on the map.
                </li>
                <li>
                  Exactly one piano wire on the map.
                </li>
                <li>
                  A known number of guards and civilians.
                </li>
              </ul>

              <p>
               {`These constraints allow information gathered 
               through vision and hearing to propagate across 
               the entire map.`}
              </p>

              {/* DEDUCTION */}
              <h2 className="text-3xl font-bold mb-8">
                Deduction
              </h2>
              <p>
                {`Observations are translated into SAT clauses.`}
              </p>

              <p>
               {`The solver is then queried to determine whether 
               a proposition is:`}
              </p>
              <ul className="pl-10 list-disc space-y-4 text-zinc-300">
                <li>
                  Necessarily true
                </li>
                <li>
                  Necessarily false
                </li>
                <li>
                  Still unknown
                </li>
                <li>
                  Exactly one piano wire on the map.
                </li>
                <li>
                  A known number of guards and civilians.
                </li>
              </ul>

              <p>
                {`This mechanism allows the agent to discover information 
                about unseen parts of the environment before directly 
                observing them.`}
              </p>
            </div>
          </section>

          {/* ARCHITECTURE */}
          <section
            id="architecture"
            className="scroll-mt-20 mb-24"
          >
            <h2 className="text-4xl font-bold mb-8">
              Architecture
            </h2>

            <div className="space-y-6 text-zinc-300 leading-8">
              <p>
                {`The project is organized as a full-stack
                application.`}
              </p>

              <p>
                {`The backend is implemented in Python and contains
                the SAT reasoning engine, pathfinding algorithms,
                map management and simulation logic.`}
              </p>

              <p>
                {`The frontend is built with Next.js and TypeScript.
                It provides real-time visualization of the map,
                AI decisions and user interactions.`}
              </p>

              <p>
                {`Communication between both layers is performed
                through a Flask REST API.`}
              </p>
            </div>
          </section>

          {/* ALGORITHMS */}
          <section
            id="algorithms"
            className="scroll-mt-20 mb-24"
          >
            <h2 className="text-4xl font-bold mb-8">
              Algorithms
            </h2>

            <div className="space-y-6 text-zinc-300 leading-8">
              <p>
                {`The core of the project combines symbolic
                reasoning and path planning techniques.`}
              </p>

              <p>
                {`A SAT solver maintains the agent's knowledge of
                the environment and allows logical deductions from
                observations gathered through vision and hearing.`}
              </p>

              <p>
                {`Exploration relies on frontier detection and
                heuristic scoring functions to prioritize
                informative and low-risk positions.`}
              </p>

              <p>
                {`Navigation uses an A*-inspired pathfinding
                algorithm with dynamic movement costs based on
                danger zones, previously visited cells and
                uncertainty.`}
              </p>

              <p>
                {`The combination of deduction and planning enables
                Hitman to efficiently explore unknown maps while
                minimizing exposure to threats.`}
              </p>
            </div>
          </section>

          {/* FUTURE */}
          <section
            id="future"
            className="scroll-mt-20 pb-55"
          >
            <h2 className="text-4xl font-bold mb-8">
              Future Improvements
            </h2>

            <ul className="pl-10 list-disc space-y-4 text-zinc-300">
              <li>
                Human vs AI game mode
              </li>

              <li>
                Custom map editor
              </li>

              <li>
                Advanced deduction rules
              </li>

              <li>
                SAT solver optimizations
              </li>

              <li>
                Additional stealth mechanics
              </li>

              <li>
                Large-scale benchmarking on complex maps
              </li>
            </ul>
          </section>
        </div>
      </main>
      <EscapeButton />
    </div>
  );
}