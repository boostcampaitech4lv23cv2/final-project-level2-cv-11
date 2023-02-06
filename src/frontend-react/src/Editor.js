import React, { useRef, useEffect, useState, useContext } from "react";
import { message, Button, Segmented } from "antd";
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
  const boxContainerRef = useRef(null);

  const [boxes, setBoxes] = useState([]);

  const { result, setResult, step, setStep, idRef, width, height, urls } =
    useContext(GlobalContext);

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

  const [originObj, setOriginObj] = useState(null);
  const [backgroundObj, setBackgroundObj] = useState(null);
  const [typicalObj, setTypicalObj] = useState(null);
  const [untypicalObj, setUntypicalObj] = useState(null);

  const [layer, setLayer] = useState("배경");

  useEffect(() => {
    const initFabric = () => {
      fabricRef.current = new fabric.Canvas(canvasRef.current);

      if (!auto && result.boxes) {
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
          case "origin":
            setOriginObj(obj);
            break;
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
    let obj = null;
    if (layer === "배경") obj = backgroundObj;
    else if (layer === "대사") obj = typicalObj;
    else if (layer === "전체") obj = originObj;
    else obj = untypicalObj;
    fabricRef.current?.setBackgroundImage(obj, () => {
      fabricRef.current.renderAll();
    });
  }, [originObj, backgroundObj, typicalObj, layer]);

  const convertAll = () => {
    setLayer("배경");
    console.log("convertAll", boxes);
    const canvas = fabricRef.current;
    const textboxes = [];
    for (const box of boxes) {
      const textbox = rect2textbox(box);
      canvas.remove(box);
      canvas.add(textbox);
      textboxes.push(textbox);
    }
    setBoxes(textboxes);
    canvas.renderAll();
    if (Math.floor(step / 10) == 2) setStep(21);
  };

  useEffect(() => {
    setResult({ ...result, boxes });
    document.onkeydown = handleKeyDown;
  }, [boxes]);

  useEffect(() => {
    if (step == 10) {
      setLayer("전체");
    } else if (step == 20) {
      const rects = boxes.filter((box) => box.textEng === "-");
      if (rects.length > 0) setStep(23);
      else convertAll();
    } else if (step == 23) {
      setTimeout(() => {
        setStep(20);
      }, 1000);
    } else if (step == 21) {
      const rects = boxes.filter((box) => box.get("type") === "rect");
      if (rects.length > 0) setStep(22);
      else setStep(3);
    } else if (step == 22) {
      setTimeout(() => {
        setStep(21);
      }, 1000);
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
    <div className="text-center flex">
      <div className="w-full">
        <div
          className={`flex justify-center py-2.5 sticky top-0 z-10 bg-white border-b ${
            auto && "invisible h-0"
          }`}
        >
          <div>
            <h1 className="text-sm">레이어</h1>
            <Segmented
              options={["배경", "대사", "효과음"]}
              value={layer}
              onChange={(e) => {
                setLayer(e);
              }}
            />
          </div>
          <div className="mt-5 ml-8">
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
          </div>
          <div className="mt-5 ml-8">
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
              대사 추가
            </Button>
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
          </div>
        </div>

        <div className="mx-auto p-0 flex justify-center">
          <canvas
            className="border"
            ref={canvasRef}
            width={width}
            height={height}
          />
        </div>
      </div>

      <div
        className="inline-block border overflow-x-hidden mr-4 sticky right-4 top-0"
        style={{
          minWidth: auto ? 0 : 520,
          width: auto ? 0 : 520,
          height: "100vh",
        }}
        ref={boxContainerRef}
      >
        <div className="py-4 sticky top-0 z-10 bg-white">대사 목록</div>
        <div>
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
                invisible={
                  layer !== "배경" && layer !== "전체" && box.layer !== layer
                }
                boxContainerRef={boxContainerRef}
              />
            ))) || <div className="m-12">대사가 없습니다</div>}
        </div>
      </div>
    </div>
  );
};

export default Editor;
