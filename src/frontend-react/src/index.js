import React, { createContext, useState } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import reportWebVitals from "./reportWebVitals";

import Main from "./Main";
import Demo from "./Demo";
import Result from "./Result";
import Header from "./components/Header";
import { FileContextProvider } from "./FileContext";
import Editor from "./Editor";
import Loading from "./Loading";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <FileContextProvider>
        <Header />
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/edit" element={<Editor />} />
          <Route path="/demo" element={<Demo />} />
          <Route path="/result" element={<Result />} />
          <Route path="/loading" element={<Loading />} />
        </Routes>
      </FileContextProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
