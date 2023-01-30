import { useState, useEffect } from "react";
import { Input, Select, Button, message, Typography, Checkbox } from "antd";
import { RightOutlined } from "@ant-design/icons";
import FontList from "../FontList.json";

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
}) => {
  const recFontNames = recFonts ? recFonts.map(({ name }) => name) : [];
  return (
    <div>
      폰트
      <div>
        <Select
          style={{
            width: 240,
          }}
          // showSearch
          // filterOption={(input, option) => {
          //   return (option?.children ?? "").toLowerCase().includes(input.toLowerCase())
          // }}
          value={font}
          onSelect={(value) => {
            setFont(value);
          }}
          onFocus={onFocus}
        >
          {recFonts && (
            <Select.OptGroup label="추천 폰트">
              {recFonts.map(({ name, prob }) => {
                return (
                  <Option key={name} name={name} value={name}>
                    <Text type="success" strong>{`${Math.round(
                      prob * 100
                    )}% `}</Text>
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
                  <Option key={name} value={name}>
                    {name}
                  </Option>
                );
              }
            )}
          </Select.OptGroup>
        </Select>
        <Select
          style={{
            width: 100,
          }}
          value={fontSize}
          onSelect={(value) => {
            setFontSize(value);
          }}
          onFocus={onFocus}
        >
          {[32, 36, 40, 44, 48, 52].map((value) => {
            return (
              <Option key={value} value={value}>
                {value}
              </Option>
            );
          })}
        </Select>
      </div>
      <Checkbox
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
      </Checkbox>
      <input
        type="color"
        onChange={(e) => {
          console.log("onchange", e);
          rect.fill = e.target.value;
          rect.canvas.renderAll();
        }}
      />
    </div>
  );
};

const Box = ({ i, box, delBox, convertBox }) => {
  const [textKor, setTextKor] = useState(box.textKor);
  const [textEng, setTextEng] = useState(box.textEng);
  const [font, setFont] = useState(box.fontFamily);
  const [fontSize, setFontSize] = useState(box.fontSize);

  const [x, setX] = useState(0);
  const [selected, setSelected] = useState(false);

  box.setSelected = (f) => {
    setSelected(f);
  };
  box.refresh = ({ text }) => {
    setX((x) => x + 1);
    setTextEng(text);
  };
  useEffect(() => {
    box.textKor = textKor;
    box.text = box.textEng = textEng;
    box.fontFamily = font;
    box.fontSize = fontSize;
    box.canvas?.renderAll();
  }, [textKor, textEng, font, fontSize]);

  useEffect(() => {
    if (textKor !== "") onTranslate();
  }, []);

  const [tLoading, setTLoading] = useState(false);
  const onTranslate = () => {
    setTLoading(true);
    select();
    fetch(
      "http://49.50.160.104:30002/mt/?" +
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
      style={{
        margin: 10,
        padding: 5,
        border: selected ? "1px solid black" : "1px solid #d9d9d9",
      }}
    >
      <div
        style={{
          textAlign: "center",
        }}
      >
        대사 #{i}
        <div
          style={{
            top: 0,
            right: 0,
            margin: "0 0 0 10",
          }}
        >
          <Button disabled>인식(미구현)</Button>
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
      <div
        style={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            padding: 5,
            width: "100%",
          }}
        >
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
        <div
          style={{
            marginTop: 21,
            display: "flex",
            alignItems: "center",
          }}
        >
          <RightOutlined />
        </div>
        <div
          style={{
            padding: 5,
            width: "100%",
          }}
        >
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
      />
    </div>
  );
};

export default Box;
