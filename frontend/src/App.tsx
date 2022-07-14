import React, { Suspense } from "react";
import SavingsComponent from "./SavingsComponent";

function App() {
  return (
    <div className="min-h-screen bg-white font-Lato">
      <Suspense
        fallback={
          <div className="text-center my-20 w-full flex flex-row justify-center align-middle">
            Loading savings...
          </div>
        }
      >
        <SavingsComponent></SavingsComponent>
      </Suspense>
    </div>
  );
}

export default App;
