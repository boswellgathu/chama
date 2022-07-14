import React from "react";

const TableComponent = () => {
  return (
    <div className="flex flex-col">
      <div className="table w-full h16 bg-gray-100 rounded-full">
        <div className="table-row h-16 w-full text-slate-400">
          <div className="table-cell align-middle pl-4 w-1/4">Name</div>
          <div className="table-cell align-middle w-1/4 text-center">May</div>
          <div className="table-cell align-middle w-1/4 text-center">June</div>
          <div className="table-cell align-middle w-1/4 text-center">July</div>
        </div>
      </div>
      <div className="table w-full h-16 hover:bg-gray-50 hover:drop-shadow-2xl hover:rounded-3xl mt-5">
        <div className="table-row h-16 w-full">
          <div className="table-cell align-middle pl-4 w-1/4">
            Githuria Wamiohere
          </div>
          <div className="table-cell align-middle w-1/4 text-center">Paid</div>
          <div className="table-cell align-middle w-1/4 text-center">
            Not Paid
          </div>
          <div className="table-cell align-middle w-1/4 text-center">
            Not Paid
          </div>
        </div>
      </div>
    </div>
  );
};

export default TableComponent;
