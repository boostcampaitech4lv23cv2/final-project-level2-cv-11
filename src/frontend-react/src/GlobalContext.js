import { createContext, useEffect, useState, useRef } from "react";
import { message } from "antd";
import { useNavigate } from "react-router-dom";
import { fabric } from "fabric";

export const GlobalContext = createContext({
  files: null,
  setFile: null,
});

export const GlobalContextProvider = ({ children }) => {
  const navigate = useNavigate();
  const [files, setFiles] = useState({});
  const [urls, setURLs] = useState({});
  const [result, setResult] = useState({ data: null, boxes: null });
  const [step, setStep] = useState(0);
  // Step은 자동 번역 수행시 사용되는 전역 상태
  // 0: 초기 상태 (캔버스 초기화, 박스 로드 등 수행)
  // 10: 시작
  // 11: 폰트 생성중
  // 20: OCR 완료
  // 21: 변환 완료 체크
  // 22: 변환 대기
  // 3: 변환 중
  // 4: 저장 중
  // 5: 결과 페이지로 이동
  // -1: OCR 실패
  const idRef = useRef(0);
  const [width, setWidth] = useState(100);
  const [height, setHeight] = useState(100);
  const [backendHost, setBackendHost] = useState("http://49.50.160.104:30002/");

  useEffect(() => {
    const urls = {};
    for (const [k, v] of Object.entries(files)) {
      if (k === "origin") continue;
      const url = URL.createObjectURL(v);
      urls[k] = url;
    }
    setURLs(urls);
  }, [files]);

  useEffect(() => {
    if (!urls.background) return;
    const img = new Image();
    img.src = urls.background;
    img.onload = () => {
      setWidth(img.width);
      setHeight(img.height);
    };

    if (!urls.typical || !urls.untypical || urls.origin) return;

    const canvas = new fabric.Canvas();

    const check = () => {
      if (canvas.backgroundImage && canvas.getObjects().length === 2) {
        console.log("all loaded");
        const origin = canvas.toDataURL({ format: "png" });
        setURLs({ ...urls, origin });
      }
    };

    fabric.Image.fromURL(urls.background, (obj) => {
      canvas.setWidth(obj.width);
      canvas.setHeight(obj.height);
      canvas.setBackgroundImage(obj);
      check();
    });

    const f = new fabric.Image.filters.RemoveColor({
      color: "#ffffff",
      threshold: 0.2,
      distance: 0.5,
    });

    fabric.Image.fromURL(urls.typical, (obj) => {
      obj.filters.push(f);
      obj.applyFilters();
      canvas.add(obj);
      canvas.renderAll();
      check();
    });

    fabric.Image.fromURL(urls.untypical, (obj) => {
      obj.filters.push(f);
      obj.applyFilters();
      canvas.add(obj);
      canvas.renderAll();
      check();
    });
  }, [urls]);

  useEffect(() => {
    if (step === 4) {
      navigate("/result");
      setStep(0);
    } else if (step === -1) {
      message.error("OCR 도중 에러가 발생했습니다.\n다시 시도해주세요.");
      navigate("/demo");
      setStep(0);
    }
  }, [step]);

  return (
    <GlobalContext.Provider
      value={{
        files,
        setFiles,
        result,
        setResult,
        step,
        setStep,
        idRef,
        width,
        height,
        backendHost,
        setBackendHost,
        urls,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export const GlobalContextConsumer = GlobalContext.Consumer;
