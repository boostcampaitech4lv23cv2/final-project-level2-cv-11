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
import { GlobalContext } from "./GlobalContext";
import OCRButton from "./components/OCRButton";
import { newRect, rect2textbox } from "./utils";

const Editor = ({ auto }) => {
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
    urls,
  } = useContext(GlobalContext);

  const removeBox = (id) => {
    const box = boxes.find((b) => b.id === id);
    if (!box) return;
    fabricRef.current?.remove(box);
    setBoxes(boxes.filter((b) => b !== box));
  };
  const removeBoxes = (ids) => {
    const newBoxes = [];
    boxes.forEach((b) => {
      if (!ids.includes(b.id)) newBoxes.push(b);
      else fabricRef.current?.remove(b);
    });
    setBoxes(newBoxes);
    fabricRef.current?.remove(...newBoxes);
  };
  const handleKeyDown = (e) => {
    if (e.key === "Delete") {
      const selected = fabricRef.current?.getActiveObjects();
      if (selected) {
        const ids = selected.map((s) => s.id);
        removeBoxes(ids);
      }
    }
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

    if (width === 0 || height === 0) {
      message.error("이미지가 로드되지 않았습니다.");
      setTimeout(() => {
        navigate("/");
      }, 1000);
    }

    document.onkeydown = handleKeyDown;

    initFabric();

    return () => {
      fabricRef.current.dispose();
      document.onkeydown = null;
      setStep(0);
    };
  }, []);

  // 파일 로드
  useEffect(() => {
    for (const key in urls) {
      const url = urls[key];
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
  }, [urls]);

  useEffect(() => {
    boxes.forEach((box) => {
      box.visible = layer === "배경" || box.layer === layer;
    });
    fabricRef.current?.renderAll();
  }, [layer]);

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
    console.log("convertAll", boxes);
    const canvas = fabricRef.current;
    const textboxes = boxes.map(rect2textbox);
    canvas.remove(...boxes);
    canvas.add(...textboxes);
    setBoxes(textboxes);
    setLayer("배경");
    canvas.renderAll();
    if (Math.floor(step / 10) == 2) setStep(21);
  };

  useEffect(() => {
    setResult({ ...result, boxes });
  }, [boxes]);

  useEffect(() => {
    if (step == 21) {
      const rects = boxes.filter((box) => box.get("type") === "rect");
      if (rects.length > 0) setStep(22);
      else setStep(3);
    } else if (step == 22) {
      setTimeout(() => {
        setStep(21);
      }, 1000);
    } else if (step == 20) {
      convertAll();
    } else if (step == 3) {
      if (layer !== "배경") {
        setLayer("배경");
        return;
      }
      const data = fabricRef.current.toDataURL({ format: "png" });
      setResult({ data, boxes });
      setTimeout(() => {
        setStep(4);
      }, 1000);
    }
  }, [step]);

  return (
    <div className="text-center">
      <div className="flex justify-center pb-2.5">
        <div className="mr-16">
          <h1 className="text-sm">레이어</h1>
          <Segmented
            options={["배경", "대사", "효과음"]}
            value={layer}
            onChange={(e) => {
              setLayer(e);
            }}
          />
        </div>
        <div className="mt-5">
          <OCRButton
            canvas={fabricRef.current}
            boxes={boxes}
            setBoxes={setBoxes}
          />
          <Button onClick={convertAll}>2. 대사 일괄 변환</Button>
          <Button
            onClick={() => {
              setLayer("배경");
              setStep(3);
            }}
          >
            3. 완성!
          </Button>
          <Button
            className="ml-16"
            onClick={() => {
              const canvas = fabricRef.current;
              canvas.remove(...canvas.getObjects());
              setBoxes([]);
            }}
            danger
          >
            대사 일괄 삭제
          </Button>
          {/* <Button
            onClick={() => {
              console.log("boxes", boxes);
            }}
          >
            디버그
          </Button> */}
        </div>
      </div>

      <div className="flex">
        <div
          className="border mx-auto p-0"
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
        <div
          className="border overflow-x-hidden mr-4"
          style={{
            width: auto ? 0 : 520,
          }}
        >
          <Divider>대사 목록</Divider>
          {(boxes.length > 0 &&
            boxes
              .filter((box) => (layer === "배경" ? true : box.layer === layer))
              .map((box, i) => (
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
                layer: layer === "배경" ? "대사" : layer,
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
