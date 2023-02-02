import { useState, useContext } from "react";
import { Input, Button, message } from "antd";
import { fabric } from "fabric";
import { GlobalContext } from "./GlobalContext";
import LayerUpload from "./components/LayerUpload";

const OCRView = ({ title, URL }) => {
  return (
    <div className="border mt-4 m-1">
      {title}
      <div className="border overflow-auto">
        <img src={URL} alt="정보 없음" />
      </div>
    </div>
  );
};

const OCRTest = () => {
  const { backendHost, files } = useContext(GlobalContext);

  const [URL1, setURL1] = useState(null);
  const [URL2, setURL2] = useState(null);
  const [URL3, setURL3] = useState(null);

  const [loading, setLoading] = useState(false);

  const typicalURL = files.typical ? URL.createObjectURL(files.typical) : null;

  const req = async (URL, formData, set) => {
    return fetch(URL, {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        const canvas = new fabric.Canvas();
        for (let i = 0; i < data.length; i++) {
          const { x1, y1, w, h } = data[i];
          canvas.add(
            new fabric.Rect({
              left: x1,
              top: y1,
              width: w,
              height: h,
              fill: "rgba(0, 0, 0, 0.1)",
              stroke: "red",
              strokeWidth: 1,
            })
          );
        }
        fabric.Image.fromURL(typicalURL, (obj) => {
          canvas.setWidth(obj.width);
          canvas.setHeight(obj.height);
          canvas.setBackgroundImage(obj);
          canvas.renderAll();
          const url = canvas.toDataURL({ format: "png" });
          set(url);
        });
      })
      .catch((err) => {
        console.err(err);
        message.error("OCR 에러");
      });
  };

  const handleOCR = async () => {
    if (!files.typical || !files.untypical) {
      message.error("파일을 먼저 업로드해주세요.");
      return;
    }
    setLoading(true);

    const formData = new FormData();
    formData.append("file", files.typical);

    const r1 = req(`${backendHost}test/clova_raw`, formData, setURL1);
    const r2 = req(`${backendHost}test/clova_post`, formData, setURL2);
    const r3 = req(`${backendHost}test/clova_tess`, formData, setURL3);

    Promise.all([r1, r2, r3]).finally(() => {
      setLoading(false);
    });
  };

  return (
    <div className="border-t">
      <h2 className="text-2xl">OCR 테스트</h2>
      <Button loading={loading} onClick={handleOCR}>
        OCR 일괄 요청
      </Button>
      <LayerUpload title="대사 레이어" name="typical" />
      <div className="flex justify-center">
        <OCRView title="CLOVA (후처리X)" URL={URL1} />
        <OCRView title="CLOVA (후처리O)" URL={URL2} />
        <OCRView title="CLOVA-Tesseract" URL={URL3} />
      </div>
      1. CLOVA OCR 직접 2. CLOVA OCR 3. CLOVA - Tesseract 4. CLOVA - Tesseract -
      Typical 분류 5. CLOVA - Tesseract - Untypical 분류 등 등
    </div>
  );
};

const HostTest = () => {
  const { backendHost, setBackendHost } = useContext(GlobalContext);
  return (
    <div className="m-auto w-80 mb-4 ">
      <h2 className="text-2xl">호스트 변경</h2>
      <Input
        addonBefore="Host"
        value={backendHost}
        onChange={(e) => {
          setBackendHost(e.target.value);
        }}
      />
    </div>
  );
};

const FontTest = () => {
  const [fontList, setFontList] = useState([]);
  const { idRef } = useContext(GlobalContext);
  return (
    <div className="border">
      <h2 className="text-2xl">폰트 테스트</h2>
      <Button
        onClick={() => {
          const fontlist = Array.from(document.fonts).map(
            (fontface) => fontface.family
          );
          setFontList(fontlist);
        }}
      >
        폰트 목록 갱신
      </Button>
      <Button
        onClick={() => {
          fetch("http://49.50.160.104:30002/test/ttf", {
            method: "GET",
          })
            .then((res) => {
              console.log("res", res);
              return res.text();
            })
            .then((uri) => fetch(uri.replace(/^"/, "").replace(/"$/, "")))
            .then((res) => res.blob())
            .then((blob) => blob.arrayBuffer())
            .then((ab) => {
              const font = new FontFace(`exp-font-${idRef.current++}`, ab);
              console.log("added", `exp-font-${idRef.current - 1}`);
              font
                .load()
                .then((e) => {
                  document.fonts.add(font);
                })
                .catch((e) => {
                  console.error("error", font.family, e);
                });
            });
        }}
      >
        폰트 FETCH
      </Button>
      <p style={{ fontFamily: `exp-font-${idRef.current - 1}` }}>
        A quick brown fox jumps over the lazy dog.
      </p>
      <div className="border">
        <p>폰트 {fontList.length} 개</p>
        <ul>
          {fontList.map((font, i) => {
            return (
              <li className={font} style={{ fontFamily: font }}>
                {font}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};

const Dev = () => {
  return (
    <div className="mt-4 mx-24 text-center">
      <h1 className="text-3xl font-bold mb-2">개발자 페이지</h1>
      각종 테스트 기능 추가 예정
      <br />
      <div className="h-4" />
      <FontTest />
      <HostTest />
      <OCRTest />
    </div>
  );
};

export default Dev;
