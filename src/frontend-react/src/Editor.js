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

function calculateFontSize(text, width, height, fontFamily = "arial") {
  let fontSize = 1;
  let textbox = new fabric.Textbox(text, {
    width: width,
    fontSize: fontSize,
    fontFamily,
    textAlign: "center",
  });

  while (textbox.height < height && textbox.width < width * 1.3) {
    fontSize += 1;
    textbox = new fabric.Textbox(text, {
      width: width,
      fontSize: fontSize,
      fontFamily,
      textAlign: "center",
    });
  }

  return fontSize - 1;
}

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
  box.color = "black";
  for (const key in props) {
    box[key] = props[key];
  }
  return box;
};

const rect2textbox = (rect) => {
  if (rect.get("type") === "textbox") return rect;
  const fontsz = calculateFontSize(
    rect.textEng,
    rect.width * rect.scaleX,
    rect.height * rect.scaleY,
    rect.fontFamily
  );
  rect.setFontSize(fontsz);
  const textbox = new fabric.Textbox(rect.textEng, {
    width: rect.width * rect.scaleX,
    fontFamily: rect.fontFamily,
    fontSize: fontsz,
    textAlign: "center",
  });
  for (const key of [
    "id",
    "top",
    "left",
    // "width",
    // "height",
    // "fontFamily",
    // "fontSize",
    "textKor",
    "textEng",
    "recFonts",
    "layer",
    "color",
  ]) {
    textbox[key] = rect[key];
  }
  return textbox;
};

const OCRButton = ({ boxes, setBoxes, canvas, idRef }) => {
  const { files, step, setStep, backendHost } = useContext(GlobalContext);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (files.typical && files.untypical && step == 10) onClick();
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
          const { x1, y1, w, h, text, fonts, color } = data[i];
          const box = newRect({
            left: x1,
            top: y1,
            width: w,
            height: h,
            textKor: text,
            recFonts: fonts,
            fontFamily: fonts[0]["name"],
            id: idRef.current++,
            layer: "대사",
            color,
          });
          boxes.push(box);
        }
      });

    const boxes_untypical = [];
    const untypicalFormData = new FormData();
    untypicalFormData.append("file", files.untypical);
    const p2 = fetch(`${backendHost}untypical/txt_extraction/v2`, {
      method: "POST",
      body: untypicalFormData,
    })
      .then((response) => response.json())
      .then((data) => {
        for (let i = 0; i < data.length; i++) {
          const { x1, y1, w, h, text, fonts, color } = data[i];
          const box = newRect({
            left: x1,
            top: y1,
            width: w,
            height: h,
            textKor: text,
            recFonts: fonts,
            fontFamily: fonts[0]["name"],
            id: idRef.current++,
            layer: "효과음",
            color,
          });
          boxes_untypical.push(box);
        }

        const ref_fonts = boxes_untypical.map((box) => box.fontFamily + ".ttf");

        const body = JSON.stringify({
          classified_font: ref_fonts,
          en_list: Array(ref_fonts.length).fill(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
          ),
        });

        if (step == 10) setStep(11);
        return fetch(`${backendHost}untypical/generation/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body,
        });
      })
      .then((res) => res.json())
      .then((uris) => {
        if (uris.length != boxes_untypical.length) {
          console.error(
            `폰트 개수 (${boxes_untypical.length})와 uri 개수 (${uris.length})가 일치하지 않습니다.))`
          );
        }
        const fs = [];
        for (
          let i = 0;
          i < Math.min(uris.length, boxes_untypical.length);
          i++
        ) {
          const uri = uris[i].replace(/^"/, "").replace(/"$/, "");
          const f = fetch(uri)
            .then((res) => res.blob())
            .then((blob) => blob.arrayBuffer())
            .then((ab) => {
              const name = `exp-font-${idRef.current++}`;
              const font = new FontFace(name, ab);
              console.log("font added", name);
              font
                .load()
                .then((e) => {
                  document.fonts.add(font);
                })
                .catch((e) => {
                  console.error("error", font.family, e);
                });
              console.log("set", i, boxes_untypical);
              boxes_untypical[i].fontFamily = name;
              boxes_untypical[i].recFonts.push({ name, prob: "생성" });
            })
            .catch((e) => {
              console.error("error", e);
            });
          fs.push(f);
        }
        return Promise.all(fs);
      })
      .then(() => {
        console.log("boxes_untypical", boxes_untypical);
        boxes.push(...boxes_untypical);
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
        if (Math.floor(step / 10) == 1)
          setTimeout(() => {
            setStep(20);
          }, 1000);
      })
      .catch((e) => {
        console.error(e);
        message.error("OCR에 실패했습니다.");
        if (step != 0) setStep(-1);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <>
      <Button id="ocr-button" loading={loading} onClick={onClick}>
        1. OCR 수행
      </Button>
    </>
  );
};

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
      setStep(0);
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
            idRef={idRef}
          />
          <Button onClick={convertAll}>2. 대사 일괄 변환</Button>
          <Button
            onClick={() => {
              setLayer("배경");
              setStep(3);
              // const data = fabricRef.current.toDataURL({ format: "png" });
              // setResult({ data, boxes });
              // navigate("/result");
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
        <div
          className="border overflow-x-hidden"
          style={{
            height: height,
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
                layer: layer,
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
