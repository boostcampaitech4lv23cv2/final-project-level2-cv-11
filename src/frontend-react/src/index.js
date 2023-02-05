import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import "./font.css";
import reportWebVitals from "./reportWebVitals";

import Main from "./Main";
import Demo from "./Demo";
import Result from "./Result";
import Header from "./components/Header";
import { GlobalContextProvider } from "./GlobalContext";
import Editor from "./Editor";
import Loading from "./Loading";
import Dev from "./Dev";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <GlobalContextProvider>
        <Header />
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/edit" element={<Editor />} />
          <Route path="/demo" element={<Demo />} />
          <Route path="/result" element={<Result />} />
          <Route path="/loading" element={<Loading />} />
          <Route path="/dev" element={<Dev />} />
        </Routes>
        <div className="h-20" />
      </GlobalContextProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
