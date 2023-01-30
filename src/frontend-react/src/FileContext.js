// TODO: 파일 이름 GlobalContext 등으로 변경
import { createContext, useEffect, useState, useRef } from "react";
import FontList from "./FontList.json";

export const FileContext = createContext({
  files: null,
  setFile: null,
});

export const FileContextProvider = ({ children }) => {
  const [files, setFiles] = useState({});
  const [result, setResult] = useState({ data: null, boxes: null });
  const [step, setStep] = useState(0);
  // Step은 자동 번역 수행시 사용되는 전역 상태
  // 0: 초기 상태
  // 1: 시작
  // 2: OCR 완료
  // 3: OCR 영역 => Textbox 변환 완료
  const idRef = useRef(0);

  useEffect(() => {
    const fetchData = async () => {
      const names = ["background", "typical", "untypical"];
      const blobs = await Promise.all(
        names.map((name) => fetch(`/${name}.png`).then((res) => res.blob()))
      );
      const files = {
        background: blobs[0],
        typical: blobs[1],
        untypical: blobs[2],
      };
      setFiles(files);
    };
    fetchData();

    FontList.forEach(({ name, url }) => {
      const font = new FontFace(name, `url(${encodeURI(url)})`);
      font
        .load()
        .then((e) => {
          document.fonts.add(font);
        })
        .catch((e) => {
          console.error("error", font.family, e);
        });
    });
  }, []);

  return (
    <FileContext.Provider
      value={{
        files,
        setFiles,
        result,
        setResult,
        step,
        setStep,
        idRef,
      }}
    >
      {children}
    </FileContext.Provider>
  );
};

export const FileContextConsumer = FileContext.Consumer;
