import React, { useRef, useEffect, useState } from "react";
import { message, Divider, Checkbox, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { fabric } from "fabric";
import Box from "./components/Box";
import "./Editor.css";

const Editor = ({ background, typical, typicalFile }) => {
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);

  useEffect(() => {
    const initFabric = () => {
      fabricRef.current = new fabric.Canvas(canvasRef.current);
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

  const [prevTypical, setPrevTypical] = useState(null);
  const [backChecked, setBackChecked] = useState(true);
  const [typicalChecked, setTypicalChecked] = useState(true);
  const onBackChanged = (e) => {
    setBackChecked(e.target.checked);
  };
  useEffect(() => {
    if (prevTypical !== null) fabricRef.current?.remove(prevTypical);
    setPrevTypical(typical);
  }, [typical]);
  useEffect(() => {
    const back = backChecked ? background : null;
    fabricRef.current?.setBackgroundImage(back, () => {
      fabricRef.current?.renderAll();
    });
  }, [backChecked, background]);

  const onTypicalChanged = (e) => {
    setTypicalChecked(e.target.checked);
  };
  useEffect(() => {
    if (typical !== null) {
      typical.selectable = false;
      typical.evented = false;
      fabricRef.current?.add(typical);
    }
  }, [typical]);
  useEffect(() => {
    if (typical !== null) {
      typical.visible = typicalChecked;
      fabricRef.current?.renderAll();
    }
  }, [typicalChecked]);

  const [OCRLoading, setOCRLoading] = useState(false);
  const reqOCR = () => {
    setOCRLoading(true);

    const formData = new FormData();
    formData.append("file", typicalFile);

    fetch("http://49.50.160.104:30002/txt_extraction/", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const { ocr_result, font_result } = data;
        for (let i = 0; i < ocr_result.length; i++) {
          const [p1, p2, text] = ocr_result[i];
          const [x1, y1] = p1;
          const [x2, y2] = p2;
          addBox(x1, y1, x2 - x1, y2 - y1, text, font_result[i]);
        }
        message.success("OCR에 성공했습니다.");
      })
      .catch((error) => {
        console.error(error);
        message.error("OCR에 실패했습니다.");
      })
      .finally(() => {
        setOCRLoading(false);
      });
  };

  const [boxes, setBoxes] = useState([]);
  const idRef = useRef(0);
  const addBox = (left, top, width, height, text, font = "NanumGothic") => {
    const box = new fabric.Rect({
      top,
      left,
      width,
      height,
      fill: "rgba(0, 0, 0, 0.1)",
      stroke: "red",
      strokeWidth: 1,
    });
    box.textKor = text;
    box.textEng = "";
    box.fontFamily = font;
    box.fontSize = 40;
    box.id = idRef.current++;

    fabricRef.current.add(box);

    setBoxes([...boxes, box]);
  };
  const delBox = (box) => {
    setBoxes(boxes.filter((b) => b.id !== box.id));
    fabricRef.current.remove(box);
  };

  useEffect(() => {
    console.log("boxes", boxes);
    boxes.forEach((box) => {
      console.log(box.get("type"));
    });
  }, [boxes]);

  const convertBox = (box) => {
    console.log("onConvertBox", box);
    const { textKor, textEng, top, left, width, height, fontFamily } = box;
    const textbox = new fabric.Textbox(textEng, {
      top,
      left,
      width,
      height,
      fontFamily,
    });
    textbox.textKor = textKor;
    textbox.textEng = textEng;
    textbox.id = box.id;
    textbox.refresh = box.refresh;
    textbox.setSelected = box.setSelected;
    fabricRef.current.add(textbox);
    fabricRef.current.remove(box);
    return textbox;
  };

  const onConvert = (box) => {
    const textbox = convertBox(box);
    setBoxes(boxes.map((b) => (b.id === box.id ? textbox : b)));
  };

  const onConvertAll = () => {
    console.log("onConvertAll");
    const textboxes = boxes.map((box) => convertBox(box));
    setBoxes(textboxes);
    setTypicalChecked(false);
  };

  return (
    <div>
      <div
        style={{
          padding: 10,
        }}
      >
        <Checkbox onChange={onBackChanged} checked={backChecked}>
          배경 보이기
        </Checkbox>
        <Checkbox onChange={onTypicalChanged} checked={typicalChecked}>
          대사 보이기
        </Checkbox>
        <Button onClick={reqOCR} loading={OCRLoading}>
          OCR 수행
        </Button>
        <Button onClick={onConvertAll}>대사 일괄 변환</Button>
        <Button
          onClick={() => {
            const data = fabricRef.current.toDataURL({ format: "png" });
            const a = document.createElement("a");
            a.href = data;
            a.download = "result.png";
            a.click();
          }}
        >
          {" "}
          다운로드
        </Button>
      </div>

      <div className="red">
        <div className="item">
          <canvas
            ref={canvasRef}
            width={800}
            height={800}
            style={{
              border: "1px solid black",
            }}
          />
        </div>
        <div className="item">
          <Divider>대사 목록</Divider>
          {(boxes.length > 0 &&
            boxes.map((box, i) => (
              <Box
                key={box.id}
                i={i}
                rect={box}
                delBox={() => {
                  delBox(box);
                }}
                convertBox={() => {
                  onConvert(box);
                }}
              />
            ))) || <div style={{ margin: 50 }}>대사가 없습니다</div>}
          <Button
            onClick={() => {
              addBox(0, 0, 100, 100, "");
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
