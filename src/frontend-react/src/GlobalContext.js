import { createContext, useEffect, useState, useRef } from "react";
import FontList from "./FontList.json";

export const GlobalContext = createContext({
  files: null,
  setFile: null,
});

export const GlobalContextProvider = ({ children }) => {
  const [files, setFiles] = useState({});
  const [result, setResult] = useState({ data: null, boxes: null });
  const [step, setStep] = useState(0);
  // Step은 자동 번역 수행시 사용되는 전역 상태
  // 0: 초기 상태
  // 1: 시작
  // 2: OCR 완료
  // 3: 변환 중
  // 4: 저장 중
  // 5: 결과 페이지로 이동
  // -1: OCR 실패
  const idRef = useRef(0);
  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);
  const [backendHost, setBackendHost] = useState("http://49.50.160.104:30002/");

  useEffect(() => {
    const fetchData = async () => {
      const names = ["background", "typical", "untypical"];
      const blobs = await Promise.all(
        names.map((name) =>
          fetch(`/sample1/${name}.png`).then((res) => res.blob())
        )
      );
      const files = {
        background: blobs[0],
        typical: blobs[1],
        untypical: blobs[2],
      };
      setFiles(files);
    };
    fetchData();

    const loaded = Array.from(document.fonts).map((font) => font.family);

    FontList.forEach(({ name, url }) => {
      if (loaded.includes(name)) return;
      const font = new FontFace(name, `url(${encodeURI(url)})`);
      font
        .load()
        .then((e) => {
          loaded.push(name);
          document.fonts.add(font);
        })
        .catch((e) => {
          console.error("error", font.family, e);
        });
    });
  }, []);

  useEffect(() => {
    if (!files.background) return;
    const url = URL.createObjectURL(files.background);
    const img = new Image();
    img.src = url;
    img.onload = () => {
      setWidth(img.width);
      setHeight(img.height);
    };
  }, [files]);

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
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export const GlobalContextConsumer = GlobalContext.Consumer;
