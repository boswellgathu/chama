import React from "react";
import TableComponent from "./TableComponent";

const SavingsComponent = () => {
  return (
    <div className="flex flex-row w-full pr-8">
      {/* side bar */}
      <div className="w-32 mr-2"></div>
      {/* main body */}
      <div className="flex flex-col w-full">
        <div className="w-full mt-8 flex flex-row justify-between">
          <h1 className="text-4xl font-extrabold">Savings</h1>
          <button className="bg-ChamaBlue text-white h-10 w-36 px-2 font-semibold rounded-full">
            <svg
              className="h-5 w-5 inline-block mr-2"
              width="30"
              height="30"
              viewBox="0 0 30 30"
              stroke-width="1"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              {" "}
              <path stroke="none" d="M0 0h30v30H0z" />{" "}
              <line x1="12" y1="5" x2="12" y2="19" />{" "}
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Add Saving
          </button>
        </div>
        <div className="w-full rounded-3xl bg-ChamaGrey h-24 mt-6 flex flex-row justify-between items-center">
          <div className="bg-white rounded-3xl w-96 h-16 ml-4">
            <form className="group relative">
              <svg
                width="24"
                height="24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
                className="absolute left-3 top-1/2 -mt-3 text-slate-400 pointer-events-none group-focus-within:text-ChamaBlue leading-6"
              >
                <path d="m19 19-3.5-3.5"></path>
                <circle cx="11" cy="11" r="6"></circle>
              </svg>
              <input
                className="focus:ring-2 focus:ring-ChamaBlue focus:outline-none appearance-none w-full h-16 text-sm leading-6 text-slate-900 placeholder-slate-400 rounded-3xl py-2 pl-10 ring-1 ring-slate-200 shadow-sm"
                type="text"
                aria-label="Search users"
                placeholder="Search users..."
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="absolute top-1/2 right-3 -mt-3 text-slate-400 pointer-events-none group-focus-within:text-ChamaBlue rotate-90"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
                width="24"
                height="24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                />
              </svg>
            </form>
          </div>
          <form className="group relative group-focus-within:text-ChamaBlue">
            <svg
              width="24"
              height="24"
              xmlns="http://www.w3.org/2000/svg"
              className="absolute left-2 top-1/2 -mt-3 text-slate-400 pointer-events-none group-focus-within:text-ChamaBlue leading-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <select
              id="states"
              className="focus:ring-2 focus:ring-ChamaBlue focus:outline-none text-sm rounded-tl-full rounded-bl-full w-24 p-2.5 px-10 text-slate-400"
            >
              <option selected>Year</option>
              <option value="CA">2020</option>
              <option value="TX">2021</option>
              <option value="WH">2022</option>
            </select>
            <select
              id="states"
              className="focus:ring-2 focus:ring-ChamaBlue focus:outline-none text-sm rounded-tr-full rounded-br-full mr-2 w-48 py-2.5 pl-5 pr-10 text-slate-400"
            >
              <option selected>Select Quarters</option>
              <option value="CA">January - March</option>
              <option value="TX">May - July</option>
              <option value="WH">September - November</option>
            </select>
          </form>
        </div>
        <div className="text-sm font-bold text-center text-gray-500 border-b border-gray-200 mt-5">
          <ul className="flex flex-wrap -mb-px">
            <li className="mr-2">
              <button className="inline-block p-4 text-ChamaBlue rounded-t-lg border-b-4 border-ChamaBlue  active">
                Current savings
              </button>
            </li>
            <li className="mr-2">
              <button
                className="inline-block p-4 border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300"
                aria-current="page"
              >
                All savings
              </button>
            </li>
            <li className="mr-2">
              <button className="inline-block p-4 rounded-t-lg border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300">
                Settings
              </button>
            </li>
          </ul>
        </div>
        {/* table & dashboard */}
        <div className="flex flex-col w-2/3 my-6 mx-2">
          <TableComponent />
          <div className=""></div>
        </div>
      </div>
    </div>
  );
};

export default SavingsComponent;
