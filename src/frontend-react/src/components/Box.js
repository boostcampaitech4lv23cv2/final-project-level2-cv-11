import { useState, useEffect, useContext, useRef } from "react";
import { Input, Select, Button, message, Typography, InputNumber } from "antd";
import { RightOutlined } from "@ant-design/icons";
import FontList from "../FontList.json";
import { GlobalContext } from "../GlobalContext";

const { TextArea } = Input;
const { Option } = Select;
const { Text } = Typography;

const FontSelect = ({
  font,
  setFont,
  fontSize,
  setFontSize,
  onFocus,
  recFonts,
  rect,
  color,
  setColor,
}) => {
  const recFontNames = recFonts ? recFonts.map(({ name }) => name) : [];
  const [f, setF] = useState(font);
  return (
    <div>
      폰트
      <div>
        <style>
          {`.box-${rect.id} .ant-select-selection-item { font-family: ${f}; }`}
        </style>
        <Select
          className={`w-60 box-${rect.id}`}
          // showSearch
          // filterOption={(input, option) => {
          //   return (option?.children ?? "").toLowerCase().includes(input.toLowerCase())
          // }}
          value={font}
          onSelect={(value) => {
            setFont(value);
            setF(value);
          }}
          onFocus={onFocus}
        >
          {recFonts && (
            <Select.OptGroup label="추천 폰트">
              {recFonts.map(({ name, prob }) => {
                const p =
                  typeof prob === "number"
                    ? `${Math.round(prob * 100)}%`
                    : prob;
                return (
                  <Option key={name} name={name} value={name}>
                    <Text type="success" strong>{`${p} `}</Text>
                    {name}
                  </Option>
                );
              })}
            </Select.OptGroup>
          )}
          <Select.OptGroup label="기본 폰트">
            {FontList.filter(({ name }) => !recFontNames.includes(name)).map(
              ({ name }) => {
                return (
                  <Option key={name} value={name} style={{ fontFamily: name }}>
                    {name}
                  </Option>
                );
              }
            )}
          </Select.OptGroup>
        </Select>
        <InputNumber
          className="w-24 h-8 translate-y-[-4px]"
          value={rect.get("type") === "textbox" ? fontSize : 0}
          onChange={(value) => {
            if (rect.get("type") === "textbox") setFontSize(value);
          }}
          onFocus={onFocus}
        />
        <input
          className="w-8 h-8 translate-y-[6px]"
          type="color"
          onChange={(e) => {
            console.log("onchange", e);
            setColor(e.target.value);
          }}
          value={color}
        />
      </div>
      {/* <Checkbox
        onClick={(e) => {
          const bold = e.target.checked ? "bold" : "normal";
          rect.fontWeight = bold;
          rect.canvas.renderAll();
        }}
      >
        굵게(임시)
      </Checkbox>
      <Checkbox
        onClick={(e) => {
          if (e.target.checked) {
            rect.stroke = "red";
            rect.strokeWidth = 1;
          } else {
            rect.stroke = null;
            rect.strokeWidth = 0;
          }
          rect.canvas.renderAll();
        }}
      >
        외곽선(임시)
      </Checkbox> */}
    </div>
  );
};

const Box = ({ i, box, delBox, convertBox, invisible, boxContainerRef }) => {
  const self = useRef(null);
  const { backendHost } = useContext(GlobalContext);
  const [textKor, setTextKor] = useState(box.textKor);
  const [textEng, setTextEng] = useState(box.textEng);
  const [font, setFont] = useState(box.fontFamily);
  const [fontSize, setFontSize] = useState(box.fontSize);
  const [color, setColor] = useState(box.color);

  const [x, setX] = useState(0);
  const [selected, setSelected] = useState(false);

  useEffect(() => {
    if (selected) {
      self.current?.scrollIntoView({
        behavior: "smooth",
        block: "center",
        inline: "center",
      });
    }
  }, [selected]);

  box.setFontSize = setFontSize;
  box.setSelected = (f) => {
    setSelected(f);
  };
  box.refresh = ({ text }) => {
    setX((x) => x + 1);
    setTextEng(text);
  };
  useEffect(() => {
    box.textKor = textKor;
    box.textEng = textEng;
    box.set("fontFamily", font);
    box.set("fontSize", fontSize);
    box.set("text", textEng);
    if (box.get("type") == "textbox") box.set("fill", color);
    box.canvas?.renderAll();
  }, [textKor, textEng, font, fontSize, color]);

  useEffect(() => {
    if (textKor !== "" && textEng.match(/^-?$/)) onTranslate();
  }, []);

  const [tLoading, setTLoading] = useState(false);
  const onTranslate = () => {
    setTLoading(true);
    fetch(
      `${backendHost}mt/?` +
        new URLSearchParams({
          text: textKor,
        }),
      {
        method: "POST",
      }
    )
      .then((res) => res.json())
      .then((res) => {
        setTextEng(res);
        setTLoading(false);
      })
      .catch((err) => {
        console.error(err);
        message.error("번역에 실패했습니다.");
        setTLoading(false);
      });
  };

  const select = () => {
    box.canvas?.setActiveObject(box);
    box.canvas?.renderAll();
  };

  return (
    <div
      className={`box ${
        invisible
          ? "absolute overflow-x-hidden h-0 m-0 p-0"
          : "m-2.5 p-1.25 text-center"
      }`}
      style={
        invisible
          ? {}
          : { border: selected ? "1px solid black" : "1px solid #d9d9d9" }
      }
      ref={self}
    >
      <div>
        대사 #{i}
        <div>
          {/* <Button disabled>인식(미구현)</Button> */}
          <Button onClick={onTranslate} loading={tLoading}>
            번역
          </Button>
          {box.get("type") === "rect" && (
            <Button onClick={convertBox}>변환</Button>
          )}
          <Button onClick={delBox} danger>
            삭제
          </Button>
        </div>
      </div>
      <div className="flex justify-center">
        <div className="p-1.25 w-full ml-2">
          한국어 대사
          <TextArea
            onChange={(event) => {
              setTextKor(event.target.value);
            }}
            value={textKor}
            autoSize
            onFocus={select}
          />
        </div>
        <div className="flex items-center mt-5">
          <RightOutlined />
        </div>
        <div className="p-1.25 w-full mr-2">
          영어 대사
          <TextArea
            onChange={(event) => {
              setTextEng(event.target.value);
            }}
            value={textEng}
            autoSize
            onFocus={select}
          />
        </div>
      </div>
      <FontSelect
        font={font}
        setFont={setFont}
        fontSize={fontSize}
        setFontSize={setFontSize}
        onFocus={select}
        recFonts={box.recFonts}
        rect={box}
        color={color}
        setColor={setColor}
      />
      {/* <div>
        x: {box.left};
        y: {box.top};
        w: {box.width * box.scaleX};
        h: {box.height * box.scaleY};
      </div>
      <Button
        onClick={() => {
          box.height = 100;
          box.width = 200;
          box.canvas.renderAll();
        }}
      >
        테스트
      </Button> */}
    </div>
  );
};

export default Box;
