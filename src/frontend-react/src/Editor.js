import React, { useRef, useEffect, useState, useContext } from "react";
import {
  message,
  Divider,
  Checkbox,
  Button,
  Popconfirm,
  Upload,
  Segmented,
} from "antd";
import { useNavigate } from "react-router-dom";
import { PlusOutlined } from "@ant-design/icons";
import { fabric } from "fabric";
import Box from "./components/Box";
import "./Editor.css";
import FontList from "./FontList.json";
import { GlobalContext } from "./GlobalContext";

const newRect = (props) => {
  const box = new fabric.Rect({
    top: 0,
    left: 0,
    height: 100,
    width: 100,
    fill: "rgba(0, 0, 0, 0.1)",
    stroke: "red",
    strokeWidth: 1,
  });
  box.textKor = "";
  box.textEng = "";
  box.fontFamily = FontList[0]["name"];
  box.fontSize = 40;
  for (const key in props) {
    box[key] = props[key];
  }
  return box;
};

const rect2textbox = (rect) => {
  const textbox = new fabric.Textbox(rect.textEng, {});
  for (const key of [
    "id",
    "top",
    "left",
    "width",
    "height",
    "fontFamily",
    "fontSize",
    "textKor",
    "textEng",
    "recFonts",
  ]) {
    textbox[key] = rect[key];
  }
  return textbox;
};

const OCRButton = ({ file, setBoxes, canvas, idRef }) => {
  const { files, step, setStep, backendHost } = useContext(GlobalContext);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (files.typical && files.untypical && step == 1) onClick();
  }, [step, files]);

  const onClick = async () => {
    if (!files.typical || !files.untypical) {
      message.error("파일을 먼저 업로드해주세요.");
      return;
    }

    setLoading(true);
    const boxes = [];

    const formData = new FormData();
    formData.append("file", files.typical);
    const p1 = fetch(`${backendHost}txt_extraction/v2`, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        for (let i = 0; i < data.length; i++) {
          const { x1, y1, x2, y2, text, fonts } = data[i];
          const box = newRect({
            left: x1,
            top: y1,
            width: x2 - x1,
            hegiht: y2 - y1,
            textKor: text,
            recFonts: fonts,
            fontFamily: fonts[0]["name"],
            id: idRef.current++,
          });
          box.recFonts = fonts;
          boxes.push(box);
        }
      });

    const untypicalFormData = new FormData();
    untypicalFormData.append("file", files.untypical);
    const p2 = fetch(`${backendHost}txt_extraction/v2`, {
      method: "POST",
      body: untypicalFormData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        for (let i = 0; i < data.length; i++) {
          const { x1, y1, x2, y2, text, fonts } = data[i];
          const box = newRect({
            left: x1,
            top: y1,
            width: x2 - x1,
            hegiht: y2 - y1,
            textKor: text,
            recFonts: fonts,
            fontFamily: fonts[0]["name"],
            id: idRef.current++,
          });
          box.recFonts = fonts;
          boxes.push(box);
        }
      });

    await Promise.all([p1, p2])
      .then(() => {
        console.log("then", boxes);
        message.success("OCR에 성공했습니다.");
        boxes.sort((a, b) => a.top - b.top);
        boxes.forEach((box) => {
          canvas.add(box);
        });
        setBoxes(boxes);
        if (step == 1) setStep(2);
      })
      .catch((e) => {
        console.error(e);
        message.error("OCR에 실패했습니다.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <Button id="ocr-button" loading={loading} onClick={onClick}>
      OCR 수행
    </Button>
  );
};

const Editor = () => {
  const navigate = useNavigate();
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);

  const [boxes, setBoxes] = useState([]);

  const {
    files,
    setFiles,
    result,
    setResult,
    step,
    setStep,
    idRef,
    width,
    height,
  } = useContext(GlobalContext);

  const removeBox = (id) => {
    const box = boxes.find((b) => b.id === id);
    if (!box) return;
    fabricRef.current?.remove(box);
    setBoxes(boxes.filter((b) => b !== box));
  };

  const [backgroundObj, setBackgroundObj] = useState(null);
  const [typicalObj, setTypicalObj] = useState(null);
  const [untypicalObj, setUntypicalObj] = useState(null);

  const [layer, setLayer] = useState("배경");

  useEffect(() => {
    const initFabric = () => {
      fabricRef.current = new fabric.Canvas(canvasRef.current);

      if (result.boxes) {
        result.boxes.forEach((box) => {
          fabricRef.current.add(box);
        });
        setBoxes(result.boxes);
      }

      // 이벤트 리스너 등록
      const f = (e) => {
        e.target.refresh(e.target);
      };
      const fs = (e) => {
        const { selected, deselected } = e;
        if (selected)
          selected.forEach((box) => {
            box.setSelected(true);
          });
        if (deselected)
          deselected.forEach((box) => {
            box.setSelected(false);
          });
      };
      fabricRef.current.on({
        "object:modified": f,
        "object:moving": f,
        "object:scaling": f,
        "selection:cleared": fs,
        "selection:created": fs,
        "selection:updated": fs,
      });
    };
    const disposeFabric = () => {
      fabricRef.current.dispose();
    };

    initFabric();

    return () => {
      disposeFabric();
    };
  }, []);

  // 파일 로드
  useEffect(() => {
    for (const key in files) {
      const file = files[key];
      const url = URL.createObjectURL(file);
      fabric.Image.fromURL(url, (obj) => {
        switch (key) {
          case "background":
            setBackgroundObj(obj);
            break;
          case "typical":
            setTypicalObj(obj);
            break;
          case "untypical":
            setUntypicalObj(obj);
            break;
        }
      });
    }
  }, [files]);

  // 배경 업데이트
  useEffect(() => {
    const obj =
      layer === "배경"
        ? backgroundObj
        : layer === "대사"
        ? typicalObj
        : untypicalObj;
    fabricRef.current?.setBackgroundImage(obj, () => {
      fabricRef.current.renderAll();
    });
  }, [backgroundObj, typicalObj, layer]);

  const convertAll = () => {
    const canvas = fabricRef.current;
    const textboxes = boxes.map(rect2textbox);
    canvas.remove(...boxes);
    canvas.add(...textboxes);
    setBoxes(textboxes);
    setLayer("배경");
  };

  useEffect(() => {
    setResult({ ...result, boxes });
  }, [boxes]);

  useEffect(() => {
    if (step == 2) {
      if (boxes[0].get("type") === "rect") convertAll();
      else if (boxes[0].get("type") === "textbox") {
        setTimeout(() => {
          const data = fabricRef.current.toDataURL({ format: "png" });
          setResult({ data, boxes });
          setStep(3);
        }, 1000);
      }
    }
  }, [step, boxes]);

  return (
    <div className="text-center">
      <div className="p-2.5">
        <Segmented
          options={["배경", "대사", "효과음"]}
          value={layer}
          onChange={(e) => {
            setLayer(e);
          }}
        />
        <OCRButton
          canvas={fabricRef.current}
          file={files["typical"]}
          setBoxes={setBoxes}
          idRef={idRef}
        />
        <Button onClick={convertAll}>대사 일괄 변환</Button>
        <Button
          onClick={() => {
            const canvas = fabricRef.current;
            canvas.remove(...canvas.getObjects());
            setBoxes([]);
          }}
          danger
        >
          대사 일괄 삭제
        </Button>
        <Button
          type="primary"
          onClick={() => {
            const data = fabricRef.current.toDataURL({ format: "png" });
            setResult({ data, boxes });
            navigate("/result");
          }}
        >
          완성!
        </Button>
        <Button
          type="primary"
          onClick={() => {
            fabricRef.current?.renderAll();
            console.log("boxes", boxes);
            console.log("files", files);
          }}
        >
          디버그
        </Button>
      </div>

      <div className="flex justify-center">
        <div
          className="border m-0 p-0"
          style={{
            width: width,
            height: height,
          }}
        >
          {/* <canvas ref={canvasRef} width={800} height={800} /> */}
          <canvas
            className="border"
            ref={canvasRef}
            width={width}
            height={height}
          />
        </div>
        <div className="border" style={{ width: width, height: height }}>
          <Divider>대사 목록</Divider>
          {(boxes.length > 0 &&
            boxes.map((box, i) => (
              <Box
                key={box.id}
                i={i}
                box={box}
                delBox={() => {
                  removeBox(box.id);
                }}
                convertBox={() => {
                  const canvas = fabricRef.current;
                  const textbox = rect2textbox(box);
                  canvas.remove(box);
                  canvas.add(textbox);
                  setBoxes(boxes.map((b) => (b === box ? textbox : b)));
                }}
              />
            ))) || <div className="m-12">대사가 없습니다</div>}

          <Button
            onClick={() => {
              const box = newRect({
                top: 100,
                left: 100,
                width: 100,
                height: 100,
                id: idRef.current++,
              });
              fabricRef.current?.add(box);
              setBoxes([...boxes, box]);
            }}
            icon={<PlusOutlined />}
          >
            대사 추가하기
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Editor;
